def find_path(t, target, path=(), whole=None):
    whole = t if whole is None else whole
    show_try(whole, path, target)
    return None

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

def show_try(t, path, target):
    canvas(600, 360)
    node = t
    for i in path:
        node = branches(node)[i]
    name = "root" if not path else ".".join(map(str, path))
    figure("tree", x=0, y=0, width=600, height=280, root=drawing(t), node_radius=32,
           node_spacing_x=100, node_spacing_y=95,
           highlights={name + ":" + str(label(node)): "current"})
    text(15, 325, "Looking for " + str(target) + " at " + name, size=18)
    frame()

sample = tree(4, [tree(7), tree(0, [tree(9), tree(9)]), tree(-3)])
print(find_path(sample, 9))
