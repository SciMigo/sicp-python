show = lambda *args: None
assert height(tree(0)) == 1, "A single node has height 1, even when its label is 0."
assert height(tree(1, [tree(0)])) == 2, "A node with one child has height 2, whatever the labels are."
assert height(tree(5, [tree(5), tree(5), tree(5), tree(5)])) == 2, "Four children side by side add width, not height."
assert height(tree(1, [tree(2), tree(3, [tree(4, [tree(5)])])])) == 4, "The longest path may run through a later child: take the largest child answer, not the first."

import random
rng = random.Random(611)
def make(depth):
    return tree(rng.randrange(-4, 5), [make(depth - 1) for _ in range(rng.randrange(4))] if depth else [])

def oracle(t):
    best, pending = 0, [(t, 1)]
    while pending:
        node, depth = pending.pop()
        best = max(best, depth)
        pending.extend((c, depth + 1) for c in node["children"])
    return best
for _ in range(40):
    t = make(rng.randrange(5))
    got = height(t)
    assert got == oracle(t), f"Expected height {oracle(t)} for a random hierarchy, got {got}: combine the child answers with max, then count this node."
