show = lambda *args: None
assert totals(tree(3, [tree(4, [tree(-10)])])) == -3, "Include descendants at every depth: 3 + 4 - 10 = -3."
assert totals(tree(0)) == 0, "Zero is a valid label; a single node sums to its own label."

import random
rng = random.Random(622)
def make(depth):
    return tree(rng.randrange(-4, 5), [make(depth - 1) for _ in range(rng.randrange(4))] if depth else [])

def oracle(t):
    total, pending = 0, [t]
    while pending:
        node = pending.pop()
        total += node["value"]
        pending.extend(node["children"])
    return total
for _ in range(30):
    t = make(4)
    got = totals(t)
    assert got == oracle(t), f"Expected label sum {oracle(t)} on a random hierarchy, got {got}."
