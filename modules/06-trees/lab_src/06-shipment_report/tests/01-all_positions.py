show=lambda *args: None
import random
rng=random.Random(760)
def make(depth):
    return tree(rng.randrange(-3,15),[make(depth-1) for _ in range(rng.randrange(4))] if depth else [])
def expected(t,path=(),out=None):
    out={} if out is None else out
    children=t['children']
    value=t['value'] if not children else sum(expected(c,path+(i,),out)[path+(i,)] for i,c in enumerate(children))
    out[path]=value
    return out
for _ in range(35):
    t=make(4)
    assert charges(t)==expected(t), "Include every position, charge only terminal records, and preserve equal-labelled positions."
assert charges(tree(90,[tree(2),tree(3)]))[()]==5, "Container labels are not additional charges."
assert charges(tree(-6))=={(): -6}, "A manifest with one terminal record reports that record's own charge at ()."
