def deep_reverse(t):
    return tree(label(t))

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

def show_tree(t, caption):
    canvas(600, 360)
    figure("tree", x=0, y=0, width=600, height=280, root=drawing(t), node_radius=32,
           node_spacing_x=100, node_spacing_y=95)
    text(15, 325, caption, size=18)
    frame()

before = tree(4, [tree(7), tree(0, [tree(9), tree(2)]), tree(-3)])
show_tree(before, "Original")
show_tree(deep_reverse(before), "Returned by deep_reverse")
