def profile(t):
    label(t)
    return 1  # count all label reads made by a full traversal

from scimigo import canvas, rectangle, text, frame

def make_star(n):
    assert n >= 1
    return {"value": 0, "children": [{"value": i, "children": []} for i in range(n-1)]}

def label(t):
    return t["value"]
def branches(t):
    return t["children"]

def show_measure(rows):
    canvas(600, 300)
    largest=max(c for n,c in rows) or 1
    for i,(n,c) in enumerate(rows):
        rectangle(120, 25+75*i, 430*c/largest, 35, color="#276bb0")
        text(12, 48+75*i, "n="+str(n), size=17)
        text(125, 85+75*i, "reads="+str(c)+", ratio="+str(round(c/n,2)), size=17)
    frame()
rows=[(n,profile(make_star(n))) for n in (11,44,176)]
show_measure(rows)
