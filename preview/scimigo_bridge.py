"""The `scimigo` learner API and the bridge the browser lab calls.

One file serves both runtimes. The preview's worker fetches it into Pyodide and
calls the `__preview_*` wrappers, which return JSON. `tools/check_lab.py` imports
it in CPython and calls `run_program` and `run_tests`, so a lab is checked
against the same API the learner runs.

Learner API (`from scimigo import ...`):
  canvas(width, height)                   start a blank picture (default 600 x 400)
  rectangle(x, y, width, height, color=)  circle(x, y, radius, color=)  text(x, y, value, size=)
  figure(kind, x=0, y=0, width=None, height=None, **params)
                                          a straightedge diagram, drawn into its box
  frame()                                 record the picture now; the lab shows a slider
  on_click(fn(x, y)), on_key(fn(key)), on_tick(fn, milliseconds=150)
A dictionary named `state` in the program is shown live after every run and event.

Check hooks (not for learners): _snapshot, _frame_count, _frame, _dispatch_click,
_dispatch_key, _dispatch_tick.
"""

import contextlib
import difflib
import io
import json
import logging
import math
import sys
import time
import traceback
import types

DEFAULT_SIZE = (600, 400)
MAX_OBJECTS = 500
MAX_FRAMES = 300
MAX_FRAME_OBJECTS = 20000
MAX_FIGURES = 4
MAX_SVG_BYTES = 300_000
MAX_FRAME_SVG_BYTES = 8_000_000
KEYS = ("up", "down", "left", "right", "space")


class _Session:
    """Everything one Run owns: the picture, the recorded frames and the event handlers."""

    def __init__(self):
        self.scene = {"width": DEFAULT_SIZE[0], "height": DEFAULT_SIZE[1], "objects": []}
        self.frames = []
        self.frame_svg_bytes = 0
        self.click = self.key = self.tick = None
        self.tick_ms = None
        self.namespace = {"__name__": "__main__"}


_session = _Session()


# ---------------------------------------------------------------------------
# figure(): straightedge diagrams, imported only when first used


_diagrams = None


def _straightedge():
    global _diagrams
    if _diagrams is None:
        try:
            from straightedge.diagrams import registry
        except ImportError as exc:
            raise RuntimeError("figure() needs the straightedge package, which is not installed here") from exc
        # figure() raises its own message for a blank diagram; the library's log line would repeat it.
        logging.getLogger("straightedge").setLevel(logging.ERROR)
        _diagrams = registry
    return _diagrams


def _json_value(value, path):
    """A JSON-safe copy of one figure parameter; tuples become lists."""
    if value is None or isinstance(value, (bool, str, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"figure parameter {path} is {value}; use a finite number")
        return value
    if isinstance(value, (list, tuple)):
        return [_json_value(item, f"{path}[{index}]") for index, item in enumerate(value)]
    if isinstance(value, dict):
        copy = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"figure parameter {path} has key {key!r}; keys must be strings")
            copy[key] = _json_value(item, f"{path}[{key!r}]")
        return copy
    raise ValueError(f"figure parameter {path} is a {type(value).__name__}; use numbers, "
                     "strings, lists and dictionaries")


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"figure {name} must be a number")
    return value


def _figure(kind, x=0, y=0, width=None, height=None, **params):
    scene = _session.scene
    registry = _straightedge()
    if not isinstance(kind, str) or kind not in registry.DIAGRAM_REGISTRY:
        close = difflib.get_close_matches(str(kind), registry.DIAGRAM_REGISTRY, n=3)
        raise ValueError(f"figure kind {kind!r} is not an installed template"
                         + (f"; did you mean {', '.join(map(repr, close))}?" if close else ""))
    if sum(1 for obj in scene["objects"] if obj["kind"] == "figure") >= MAX_FIGURES:
        raise ValueError(f"One picture holds at most {MAX_FIGURES} figures; call canvas() "
                         "to start a new picture")
    width = scene["width"] if width is None else _number(width, "width")
    height = scene["height"] if height is None else _number(height, "height")
    if width <= 0 or height <= 0:
        raise ValueError("figure width and height must be positive")
    params = {key: _json_value(value, key) for key, value in params.items()}
    svg = registry.render_diagram({"type": kind, "params": params})
    if not svg or registry.is_blank_diagram(svg):
        findings = registry.refusal_findings(kind, params)
        raise ValueError(f"figure({kind!r}) drew nothing from parameters {sorted(params)}: "
                         + (registry.refusal_reason(findings) if findings
                            else "check their names and shapes against the template"))
    if len(svg.encode()) > MAX_SVG_BYTES:
        raise ValueError(f"figure({kind!r}) is {len(svg.encode()) // 1000} KB; the limit is "
                         f"{MAX_SVG_BYTES // 1000} KB. Draw fewer items")
    _add("figure", type=kind, x=_number(x, "x"), y=_number(y, "y"),
         width=width, height=height, params=params, svg=svg)


# ---------------------------------------------------------------------------
# The rest of the learner API


def _add(kind, **values):
    if len(_session.scene["objects"]) >= MAX_OBJECTS:
        raise ValueError(f"This picture has reached the {MAX_OBJECTS}-shape limit")
    _session.scene["objects"].append(dict(kind=kind, **values))


def _canvas(width, height):
    if not (isinstance(width, int) and isinstance(height, int)
            and 1 <= width <= 1200 and 1 <= height <= 800):
        raise ValueError("canvas width and height must be whole numbers, at most 1200 x 800")
    _session.scene.update(width=width, height=height, objects=[])


def _circle(x, y, radius, color="blue"):
    _add("circle", x=x, y=y, radius=radius, color=color)


def _rectangle(x, y, width, height, color="blue"):
    _add("rectangle", x=x, y=y, width=width, height=height, color=color)


def _text(x, y, value, *, size=20, color="#1f2430"):
    _add("text", x=x, y=y, value=str(value)[:200], size=size, color=color)


def _handler(callback, name):
    if not callable(callback):
        raise TypeError(f"{name} needs a function")
    return callback


def _on_click(callback):
    _session.click = _handler(callback, "on_click")


def _on_key(callback):
    _session.key = _handler(callback, "on_key")


def _on_tick(callback, milliseconds=150):
    _handler(callback, "on_tick")
    if not (isinstance(milliseconds, int) and 50 <= milliseconds <= 2000):
        raise ValueError("on_tick milliseconds must be a whole number from 50 to 2000")
    _session.tick, _session.tick_ms = callback, milliseconds


def _frame():
    """Record a copy of the picture as it is now."""
    frames, objects = _session.frames, _session.scene["objects"]
    if len(frames) >= MAX_FRAMES:
        raise ValueError(f"This program recorded more than {MAX_FRAMES} frames; record fewer steps")
    if sum(len(f) for f in frames) + len(objects) > MAX_FRAME_OBJECTS:
        raise ValueError("These frames hold too many shapes; draw fewer shapes per frame")
    svg_bytes = sum(len(obj["svg"]) for obj in objects if obj["kind"] == "figure")
    if _session.frame_svg_bytes + svg_bytes > MAX_FRAME_SVG_BYTES:
        raise ValueError("These frames hold too much figure data; record fewer frames or smaller figures")
    _session.frame_svg_bytes += svg_bytes
    frames.append(json.loads(json.dumps(objects)))


def _snapshot():
    return json.loads(json.dumps(_session.scene))


def _frame_count():
    return len(_session.frames)


def _frame_at(index):
    return json.loads(json.dumps(_session.frames[index]))


def _dispatch_click(x, y):
    if _session.click is None:
        raise RuntimeError("Register a click handler with on_click(handler), press Run, then click again")
    _session.click(x, y)


def _dispatch_key(key):
    if key not in KEYS:
        raise ValueError("Keys are " + ", ".join(KEYS))
    if _session.key is None:
        raise RuntimeError("Register a key handler with on_key(handler), press Run, then press a key again")
    _session.key(key)


def _dispatch_tick():
    if _session.tick is None:
        raise RuntimeError("Register a tick handler with on_tick(handler, 150), then press Run")
    _session.tick()


API = {
    "canvas": _canvas, "circle": _circle, "rectangle": _rectangle, "text": _text,
    "figure": _figure, "frame": _frame,
    "on_click": _on_click, "on_key": _on_key, "on_tick": _on_tick,
    "_snapshot": _snapshot, "_frame_count": _frame_count, "_frame": _frame_at,
    "_dispatch_click": _dispatch_click, "_dispatch_key": _dispatch_key,
    "_dispatch_tick": _dispatch_tick,
}


def new_session():
    """Start a fresh picture and install a fresh `scimigo` module; returns the module."""
    global _session
    _session = _Session()
    module = types.ModuleType("scimigo")
    module.__doc__ = "The browser lab's drawing and event API."
    for name, fn in API.items():
        setattr(module, name, fn)
    sys.modules["scimigo"] = module
    return module


# ---------------------------------------------------------------------------
# Running programs and checks


def _plain(value, depth=0):
    """A bounded, JSON-safe copy of one value for the live state panel."""
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else repr(value)
    if isinstance(value, str):
        return value[:160]
    if isinstance(value, (list, tuple)) and depth < 2:
        return [_plain(item, depth + 1) for item in list(value)[:40]]
    if isinstance(value, dict) and depth < 2:
        return {str(key)[:40]: _plain(item, depth + 1) for key, item in list(value.items())[:20]}
    return repr(value)[:160]


def _state_view():
    candidate = _session.namespace.get("state")
    if not isinstance(candidate, dict):
        return None
    items = list(candidate.items())[:20]
    view = {str(key)[:40]: _plain(value) for key, value in items}
    view["__sizes__"] = {str(key)[:40]: len(value) for key, value in items
                         if isinstance(value, (list, tuple, dict, set, str))}
    return view


def _result(error=None, output=""):
    return {"scene": _session.scene, "error": error, "output": output,
            "acceptsClicks": _session.click is not None,
            "acceptsKeys": _session.key is not None, "tickMs": _session.tick_ms,
            "state": _state_view(), "frames": _session.frames or None}


def _bind(namespace, fixtures):
    for fixture in fixtures or ():
        namespace[fixture["name"]] = json.loads(json.dumps(fixture["data"]))


def run_program(source, fixtures=()):
    """Run a learner program in a fresh session; the session stays live for events."""
    new_session()
    _bind(_session.namespace, fixtures)
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(compile(source, "your_program.py", "exec"), _session.namespace)
        return _result(output=output.getvalue())
    except Exception:
        return _result(error=traceback.format_exc(), output=output.getvalue())


def _event(dispatch, *args):
    try:
        _session.frames.clear()
        _session.frame_svg_bytes = 0
        dispatch(*args)
        return _result()
    except Exception:
        return _result(error=traceback.format_exc())


def run_tests(source, tests, fixtures=()):
    """Run each check against its own fresh run of `source`, with `__source__` bound.

    Returns [{"name", "passed", "error", "ms"}]. The live session, if any, is restored.
    """
    global _session
    live_session, live_module = _session, sys.modules.get("scimigo")
    results = []
    try:
        for test in tests:
            new_session()
            namespace = _session.namespace
            _bind(namespace, fixtures)
            started = time.perf_counter()
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(source, "your_program.py", "exec"), namespace)
                    namespace["__source__"] = source
                    exec(compile(test["code"], "check.py", "exec"), namespace)
                passed, error = True, ""
            except Exception:
                detail = traceback.format_exc().strip().splitlines()[-1]
                passed, error = False, "" if detail == "AssertionError" else detail
            results.append({"name": test["name"], "passed": passed, "error": error,
                            "ms": round((time.perf_counter() - started) * 1000, 1)})
    finally:
        _session = live_session
        if live_module is not None:
            sys.modules["scimigo"] = live_module
    return results


# JSON wrappers for the browser worker.

def __preview_run(source, fixtures_json="[]"):
    return json.dumps(run_program(source, json.loads(fixtures_json)))


def __preview_click(x, y):
    return json.dumps(_event(_dispatch_click, x, y))


def __preview_key(key):
    return json.dumps(_event(_dispatch_key, key))


def __preview_tick():
    return json.dumps(_event(_dispatch_tick))


def __preview_tests(source, tests_json, fixtures_json="[]"):
    return json.dumps(run_tests(source, json.loads(tests_json), json.loads(fixtures_json)))


new_session()
