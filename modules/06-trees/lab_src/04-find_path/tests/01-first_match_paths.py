show_try = lambda *args: None
assert find_path(tree(6), 6) == [6], "When the root matches, the path is the one-element list holding the root's label."
assert find_path(tree(6), 7) is None, "Return None when no node carries the target."
assert find_path(tree(1, [tree(0, [tree(0)])]), 0) == [1, 0], "A label of 0 is a real match; stop at the first one."
got = find_path(tree(1, [tree(2, [tree(5)]), tree(5)]), 5)
assert got == [1, 2, 5], f"Depth first, left to right: the 5 under child 0 comes before the root's own second child. Got {got}."
assert find_path(tree(1, [tree(2), tree(3, [tree(4)])]), 4) == [1, 3, 4], "After a child's subtree fails, continue with the next child."

import random
rng = random.Random(645)
def make(depth):
    return tree(rng.randrange(-4, 5), [make(depth - 1) for _ in range(rng.randrange(4))] if depth else [])

def oracle(t, target):
    if t["value"] == target: return [t["value"]]
    for c in t["children"]:
        found = oracle(c, target)
        if found is not None: return [t["value"]] + found
    return None
for _ in range(60):
    t = make(4); target = rng.randrange(-5, 6)
    got = find_path(t, target)
    assert got == oracle(t, target), f"On a random hierarchy with repeated labels, looking for {target}: expected {oracle(t, target)}, got {got}."
