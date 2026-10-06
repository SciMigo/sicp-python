import random
rng = random.Random(2002)
assert prepare_badges([]) == [], "With no prefixes, return an empty list."
for _ in range(40):
    prefixes = [rng.randrange(-20, 21) for _ in range(rng.randrange(1, 25))]
    original = list(prefixes)
    first = prepare_badges(prefixes); second = prepare_badges([80, -3])
    assert isinstance(first, list) and len(first) == len(original) and all(callable(b) for b in first), f"Return one callable per prefix, in order: expected {len(original)} callables."
    prefixes[:] = [999]
    for reading in [0, -7, 13]:
        got = [b(reading) for b in first]
        want = [(p, reading) for p in original]
        assert got == want, f"Set up with {len(original)} prefixes starting {original[:3]}, then the caller's list was changed. For reading {reading} the first callables must return {want[:3]}; they returned {got[:3]}. Each panel keeps the prefix it was set up with."
        got2 = [b(reading) for b in second]
        assert got2 == [(80, reading), (-3, reading)], f"A second setup with [80, -3] must return [(80, {reading}), (-3, {reading})] whatever the first setup did; it returned {got2}."
