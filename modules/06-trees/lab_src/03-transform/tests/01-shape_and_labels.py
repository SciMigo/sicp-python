show=lambda *args: None
import copy, random
rng=random.Random(603)
def make(depth):
    return tree(rng.randrange(-4,5), [make(depth-1) for _ in range(rng.randrange(4))] if depth else [])
def verify(a,b,f):
    assert a is not b and branches(a) is not branches(b), "Construct fresh nodes and child lists."
    assert label(b)==f(label(a)), "Transform every label, including leaves and the root."
    assert len(branches(a))==len(branches(b)), "Preserve every ordered child position."
    for x,y in zip(branches(a),branches(b)): verify(x,y,f)
for _ in range(30):
    a=make(4); original=copy.deepcopy(a); calls=[]
    f=lambda v: calls.append(v) or (v*v+2)
    b=transform(a,f)
    assert a==original, "Leave the original hierarchy unchanged."
    def size(t): return 1+sum(size(c) for c in branches(t))
    assert len(calls)==size(a), "Apply f exactly once per node."
    verify(a,b,lambda v:v*v+2)

