show_stage=lambda *args: None
import random
rng=random.Random(1401)
def oracle(spec,x):
    for a,b in spec: x=a*x+b
    return x
for _ in range(40):
    spec=[(rng.randrange(-2,3),rng.randrange(-5,6)) for _ in range(rng.randrange(9))]
    f=make_service(spec)
    assert callable(f), "Setup must return behavior for later readings."
    for x in [-7,0,3,11]: assert f(x)==oracle(spec,x), "Apply settings in their original order."
    original=oracle(spec,5)
    spec[:]=[(999,999)]
    assert f(5)==original, "Prepared behavior must not change when the source settings change."
a=make_service([(2,1)]);b=make_service([(3,-2)])
assert a(4)==9 and b(4)==10 and a(0)==1, "Each prepared service keeps its own settings."
assert make_service([])(7)==7, "No adjustments preserve the input."

