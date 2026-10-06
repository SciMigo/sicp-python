def charges(t):
    result={}
    def visit(node,path):
        result[path]=terminal_charge(node)
        for i,c in enumerate(branches(node)):
            visit(c,path+(i,))
    visit(t,())
    return result

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
    node = t
    for i in path:
        node = branches(node)[i]
    name = "root" if not path else ".".join(map(str, path))
    figure("tree", x=0, y=0, width=600, height=280, root=drawing(t), node_radius=32,
           node_spacing_x=100, node_spacing_y=95,
           highlights={name + ":" + str(label(node)): "current"})
    text(15, 325, "Completed " + name + ": " + str(answer), size=18)
    frame()

sample = tree(4, [tree(7), tree(0, [tree(9), tree(9)]), tree(-3)])
def terminal_charge(t):
    if not branches(t):
        return label(t)
    return sum(terminal_charge(c) for c in branches(t))
report=charges(sample)
show(sample, (), report[()])
