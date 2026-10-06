show_tree = lambda *args: None
import copy

import random
rng = random.Random(634)
def make(depth):
    return tree(rng.randrange(-4, 5), [make(depth - 1) for _ in range(rng.randrange(4))] if depth else [])

def nodes(t):
    found, pending = [], [t]
    while pending:
        node = pending.pop()
        found.append(node)
        pending.extend(node["children"])
    return found
for _ in range(20):
    t = make(4)
    original = copy.deepcopy(t)
    result = deep_reverse(t)
    assert t == original, "Leave the input unchanged: build new nodes instead of reversing its child lists in place."
    old = {id(n) for n in nodes(t)} | {id(n["children"]) for n in nodes(t)}
    assert all(id(n) not in old and id(n["children"]) not in old for n in nodes(result)), "The result must not share nodes or child lists with the input."
    assert deep_reverse(result) == original, "Mirroring twice must give back the original shape and labels."
