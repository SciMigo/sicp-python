show=lambda *args: None
import random
rng=random.Random(101)
for _ in range(40):
    values=[rng.randrange(-8,9) for _ in range(rng.randrange(10))]
    calls=[]
    def rule(v):
        calls.append(v)
        return v*v+3
    assert total_terms(values,rule)==sum(v*v+3 for v in values), "Sum the caller's rule results, including duplicates and negative inputs."
    assert calls==values, "Apply the rule exactly once per value, in input order."
assert total_terms([],lambda v: (_ for _ in ()).throw(AssertionError('called on empty input'))) == 0

