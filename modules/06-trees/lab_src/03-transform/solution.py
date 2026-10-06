def transform(t, f):
    return tree(f(label(t)), [transform(child, f) for child in branches(t)])

from scimigo import canvas, figure, frame, text

def tree(value, children=None):
    return {"value": value, "children": list(children or [])}
def label(t):
    return t["value"]
def branches(t):
    return t["children"]
def is_leaf(t):
    return not branches(t)

def drawing(t, path=()):
    name = "root" if not path else ".".join(map(str, path))
    return {"value": name + ":" + str(label(t)),
            "children": [drawing(b, path + (i,)) for i, b in enumerate(branches(t))]}

def show(t, path, answer):
    canvas(600, 360)
    view = drawing(t)
    node = t
    for i in path:
        node = branches(node)[i]
    name = "root" if not path else ".".join(map(str, path))
    figure("tree", x=0, y=0, width=600, height=280, root=view, node_radius=32, node_spacing_x=100, node_spacing_y=95,
           highlights={name + ":" + str(label(node)): "current"})
    text(15, 325, "Completed " + name + ": " + str(answer), size=18)
    frame()

sample = tree(6, [tree(0), tree(1, [tree(5), tree(5)]), tree(-2)])
result=transform(sample, lambda v:v+10)
show(result, (), label(result))
