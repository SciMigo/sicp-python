"""Check and build the written lessons in modules/<id>/lesson.md.

    .venv/bin/python tools/lessons.py check [prefix ...]          # run every Python block; render every figure
    .venv/bin/python tools/lessons.py build OUT_DIR [prefix ...]  # write OUT_DIR/<module id>.html

A lesson is the readable half of a module, free and public: it teaches the ideas with its own
worked examples and carries no lab exercise, check or solution. Each lesson's Python blocks run in
order in one namespace, so the asserts in them are the lesson's own tests (as in Build with Python).

On top of plain markdown, a lesson may use:
- ```figure fences holding JSON {"type": <straightedge template>, "params": {...}, "caption": "..."},
  rendered to inline SVG at build time. A figure that renders blank is an error, not a gap.
- $...$ and $$...$$, converted to MathML at build time (the site strips scripts, so no KaTeX).
- `??? predict "Predict: ..."` blocks (pymdownx.details) for a question whose answer is folded,
  and `!!! invariant "Invariant"` call-outs.

The page is plain HTML with one <h1> and an <h2> per section, so the course site can render it on
the module page with its outline beside it.

Needs .venv (markdown, pymdown-extensions, latex2mathml, straightedge); see README.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r"^```python\n(.*?)^```", re.S | re.M)
FIGURE = re.compile(r"^```figure\n(.*?)^```", re.S | re.M)
CODE = re.compile(r"(```.*?```|`[^`\n]+`)", re.S)
MATH = re.compile(r"\$\$(.+?)\$\$|(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$(?!\d)", re.S)


def lessons(prefixes: list[str]) -> list[Path]:
    paths = sorted(ROOT.glob("modules/*/lesson.md"))
    return [p for p in paths if not prefixes or p.parent.name.startswith(tuple(prefixes))]


def render_figure(spec_json: str) -> str:
    from straightedge.diagrams import render_diagram
    from straightedge.diagrams.registry import is_blank_diagram

    spec = json.loads(spec_json)
    svg = render_diagram({"type": spec["type"], "params": spec.get("params", {})})
    if not svg or "<svg" not in svg or is_blank_diagram(svg):
        raise ValueError(f"figure {spec['type']!r} rendered nothing: check its params")
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    caption = spec.get("caption", "")
    cap = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
    return f'\n<figure class="lesson-figure">{svg}{cap}</figure>\n'


def check(prefixes: list[str]) -> int:
    failed = 0
    paths = lessons(prefixes)
    for path in paths:
        source = path.read_text(encoding="utf-8")
        bad = 0
        if not source.startswith("# "):
            print(f"FAIL {path.parent.name}: a lesson starts with '# Title'")
            bad += 1
        namespace: dict = {"__name__": "__lesson__"}
        blocks = BLOCK.findall(source)
        for number, block in enumerate(blocks, start=1):
            try:
                exec(compile(block, f"{path.parent.name}:block{number}", "exec"), namespace)
            except Exception as exc:  # noqa: BLE001
                bad += 1
                print(f"FAIL {path.parent.name} block {number}: {type(exc).__name__}: {exc}")
        figures = FIGURE.findall(source)
        for number, spec in enumerate(figures, start=1):
            try:
                render_figure(spec)
            except Exception as exc:  # noqa: BLE001
                bad += 1
                print(f"FAIL {path.parent.name} figure {number}: {exc}")
        failed += bad
        print(f"{'ok  ' if not bad else 'FAIL'} {path.parent.name}: {len(blocks)} blocks, {len(figures)} figures")
    print(f"{len(paths)} lessons, {failed} failures")
    return 1 if failed else 0


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · SICP in Python</title>
<meta name="description" content="{description}">
<style>
body {{ margin: 0 auto; max-width: 46rem; padding: 2rem 1.25rem 4rem; font: 17px/1.65 system-ui, sans-serif; color: #1f1b2e; }}
h1 {{ font-size: 2rem; line-height: 1.2; margin: 0 0 1rem; }}
h2 {{ font-size: 1.3rem; margin: 2.2rem 0 .6rem; }}
code {{ font: .9em ui-monospace, SFMono-Regular, Menlo, monospace; background: #f3f0fa; border-radius: 4px; padding: .1em .3em; }}
pre {{ background: #1e1733; color: #f1edfb; border-radius: 10px; padding: 1rem 1.1rem; overflow-x: auto; line-height: 1.5; }}
pre code {{ background: none; padding: 0; color: inherit; }}
table {{ border-collapse: collapse; width: 100%; font-size: .92em; margin: 1rem 0; }}
th, td {{ border: 1px solid #e3def0; padding: .45rem .6rem; text-align: left; vertical-align: top; }}
th {{ background: #f6f4fb; }}
math[display="block"] {{ display: block; margin: 1rem 0; overflow-x: auto; }}
.lesson-figure {{ margin: 1.4rem 0; text-align: center; }}
.lesson-figure svg {{ max-width: 100%; height: auto; background: #fff; border-radius: 12px; }}
.lesson-figure figcaption {{ font-size: .9rem; color: #5b5670; margin-top: .5rem; }}
.admonition {{ margin: 1.2rem 0; padding: .7rem 1rem; border-left: 4px solid #7c3aed; background: #f6f2ff; border-radius: 6px; }}
.admonition-title {{ font-weight: 700; margin: 0 0 .3rem; }}
details {{ margin: 1.2rem 0; padding: .7rem 1rem; border: 1px solid #e3def0; border-left: 4px solid #0f766e; border-radius: 6px; }}
details > summary {{ cursor: pointer; font-weight: 700; }}
@media (prefers-color-scheme: dark) {{
body {{ background: #121721; color: #e8edf5; }}
code {{ background: #252d3c; }}
th {{ background: #252d3c; }}
th, td, details {{ border-color: #4a5669; }}
.admonition {{ background: #252d3c; border-color: #bba4ff; }}
.lesson-figure figcaption, .attribution {{ color: #c4cede; }}
a {{ color: #99caff; }}
}}
.attribution {{ margin-top: 3rem; font-size: .85rem; color: #5b5670; }}
</style>
</head>
<body>
{body}
<p class="attribution">{attribution}</p>
</body>
</html>
"""


def to_html(source: str) -> str:
    import markdown
    from latex2mathml.converter import convert

    source = FIGURE.sub(lambda m: render_figure(m.group(1)), source)
    maths: list[str] = []

    def keep(m: re.Match) -> str:
        tex, display = (m.group(1), "block") if m.group(1) is not None else (m.group(2), "inline")
        maths.append(convert(tex.strip(), display=display))
        return f"\x00M{len(maths) - 1}\x00"

    parts = CODE.split(source)
    parts[::2] = [MATH.sub(keep, part) for part in parts[::2]]      # never inside code
    body = markdown.markdown("".join(parts), extensions=[
        "fenced_code", "tables", "admonition", "md_in_html", "pymdownx.details"],
        output_format="html")
    return re.sub(r"\x00M(\d+)\x00", lambda m: maths[int(m.group(1))], body)


def build(out_dir: Path, prefixes: list[str]) -> int:
    course = json.loads((ROOT / "course.json").read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in lessons(prefixes):
        source = path.read_text(encoding="utf-8")
        title = source.splitlines()[0].lstrip("# ").strip()
        first = next(p for p in source.split("\n\n")[1:] if p.strip() and not p.startswith(("```", "#")))
        description = re.sub(r"[`*$]", "", first.replace("\n", " "))[:300]
        module = json.loads((path.parent / "module.json").read_text(encoding="utf-8"))
        page = PAGE.format(title=html.escape(title), description=html.escape(description, quote=True),
                           body=to_html(source), attribution=html.escape(module.get("sourceAttribution", course["sourceAttribution"])))
        (out_dir / f"{path.parent.name}.html").write_text(page, encoding="utf-8")
        print(f"built {path.parent.name}.html")
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["check"]:
        raise SystemExit(check(sys.argv[2:]))
    if sys.argv[1:2] == ["build"] and len(sys.argv) >= 3:
        raise SystemExit(build(Path(sys.argv[2]), sys.argv[3:]))
    raise SystemExit(__doc__)
