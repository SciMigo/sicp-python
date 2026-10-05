show_tree = lambda *args: None
assert deep_reverse(tree(8)) == tree(8), "A single node mirrors to a single node with the same label."
got = deep_reverse(tree(1, [tree(2, [tree(3), tree(4)]), tree(5)]))
assert got != tree(1, [tree(5), tree(2, [tree(3), tree(4)])]), "Only the root's children were reversed: reverse the children of every node."
assert got == tree(1, [tree(5), tree(2, [tree(4), tree(3)])]), "Expected root children 5 then 2, and inside 2 the children 4 then 3."

import random
rng = random.Random(633)
def make(depth):
    return tree(rng.randrange(-4, 5), [make(depth - 1) for _ in range(rng.randrange(4))] if depth else [])

def oracle(t):
    return {"value": t["value"], "children": [oracle(c) for c in reversed(t["children"])]}
for _ in range(30):
    t = make(4)
    assert deep_reverse(t) == oracle(t), "On a random hierarchy some level was not mirrored, or a label or child was lost."
