import random
rng=random.Random(2002)
assert prepare_badges([])==[]
for _ in range(40):
    prefixes=[rng.randrange(-20,21) for _ in range(rng.randrange(1,25))]
    original=list(prefixes)
    first=prepare_badges(prefixes);second=prepare_badges([80,-3])
    assert len(first)==len(original) and all(callable(b) for b in first)
    prefixes[:]=[999]
    for reading in [0,-7,13]:
        assert [b(reading) for b in first]==[(p,reading) for p in original],"Each deferred callback must retain its own original panel prefix."
        assert [b(reading) for b in second]==[(80,reading),(-3,reading)],"Separate configurations must not share state."
