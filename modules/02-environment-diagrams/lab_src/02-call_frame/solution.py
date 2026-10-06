def call_frame(frames, function, arguments, caller):
    """Create the frame in which this call's body runs; return its index."""
    created = {"bindings": dict(zip(function["params"], arguments)), "parent": function["env"]}
    frames.append(created)
    new = len(frames) - 1
    show_call(frames, new, caller)
    return new

from scimigo import canvas, figure, frame, text

def lookup(frames, current, name):
    while current is not None:
        if name in frames[current]["bindings"]:
            return frames[current]["bindings"][name]
        current = frames[current]["parent"]
    raise NameError(name)

def show_call(frames, new, caller):
    path, index = [], new
    while index is not None and len(path) < len(frames):
        path.append(index)
        index = frames[index]["parent"]
    canvas(360, 420)
    shown = [{"id": str(i), "label": "Frame " + str(i),
              "parent": str(frames[i]["parent"]) if frames[i]["parent"] is not None else None,
              "bindings": [{"name": k, "value": str(v)} for k, v in frames[i]["bindings"].items()]}
             for i in reversed(path)]
    figure("environment_diagram", x=0, y=0, width=360, height=370,
           frames=shown, frame_width=240, frame_padding=16, row_height=22,
           highlights={"frames": {str(new): "current"}})
    text(12, 400, "Caller: frame " + str(caller) + ". New: frame " + str(new), size=16)
    frame()

frames = [{"bindings": {"rate": 6}, "parent": None},
          {"bindings": {"rate": 80, "reading": 3}, "parent": 0}]
add_rate = {"params": ["reading"], "env": 0}
new = call_frame(frames, add_rate, [3], 1)
print(lookup(frames, new, "reading") + lookup(frames, new, "rate"))
