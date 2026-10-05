show = lambda *args: None
assert count_leaves(tree(1, [tree(0), tree(-9)])) == 2, "Internal label 1 is not a leaf; labels 0 and -9 are."
assert count_leaves(tree(77)) == 1, "A single node is one leaf, whatever its label."
import random
rng = random.Random(206)
def generate(depth):
    return tree(rng.randrange(-2, 3), [generate(depth-1) for _ in range(rng.randrange(4))] if depth else [])
def oracle(t):
    pending=[t]; total=0
    while pending:
        node=pending.pop()
        if not node['children']: total+=1
        pending.extend(node['children'])
    return total
for _ in range(40):
    t=generate(4)
    assert count_leaves(t)==oracle(t), "Leaf count must depend on shape, including repeated labels."

