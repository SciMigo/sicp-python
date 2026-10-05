def define(frames, current, name, value):
    """Bind name to value in the frame at index current."""
    frames[current]["bindings"][name] = value

def assign(frames, current, name, value):
    """Rebind name in the nearest frame that already binds it; return that frame's index."""
    while current is not None:
        show_scope(frames, current, name)
        bindings = frames[current]["bindings"]
        if name in bindings:
            bindings[name] = value
            return current
        current = frames[current]["parent"]
    raise NameError(name)

from scimigo import canvas, figure, frame, text

def show_scope(frames, current, name):
    canvas(360, 480)
    shown = [{"id": str(i), "label": "Frame " + str(i),
              "parent": str(f["parent"]) if f["parent"] is not None else None,
              "bindings": [{"name": k, "value": str(v)} for k, v in f["bindings"].items()]}
             for i, f in enumerate(frames)]
    figure("environment_diagram", x=0, y=0, width=360, height=440,
           frames=shown, frame_width=240, frame_padding=16, row_height=22,
           highlights={"frames": {str(current): "current"}})
    text(12, 465, "Looking for " + name + " in frame " + str(current), size=16)
    frame()

frames = [{"bindings": {"rate": 80}, "parent": None},
          {"bindings": {"rate": 6}, "parent": 0},
          {"bindings": {"reading": 3}, "parent": 1}]
define(frames, 2, "unit", "cm")
try:
    print("rate was rebound in frame", assign(frames, 2, "rate", 7))
except NameError:
    print("assign found no frame that binds rate")
print([f["bindings"] for f in frames])
