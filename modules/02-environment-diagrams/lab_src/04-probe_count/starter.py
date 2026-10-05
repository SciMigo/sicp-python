def measured_lookup(frames, current, name):
    """Look name up from frame current; return (value, number of probes made)."""
    return None, 0

from scimigo import canvas, rectangle, text, frame

def show_probes(rows):
    canvas(600, 300)
    largest = max(count for depth, count in rows) or 1
    for i, (depth, count) in enumerate(rows):
        rectangle(120, 25 + 75 * i, 430 * count / largest, 35, color="#276bb0")
        text(12, 48 + 75 * i, "depth=" + str(depth), size=17)
        text(125, 85 + 75 * i, "probes=" + str(count), size=17)
    frame()

rows = []
for depth in [2, 5, 9]:
    frames = [{"bindings": {}, "parent": i - 1 if i else None} for i in range(depth)]
    frames[0]["bindings"]["key"] = 42
    rows.append((depth, measured_lookup(frames, depth - 1, "key")[1]))
show_probes(rows)
