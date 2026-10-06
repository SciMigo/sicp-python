import random
show_preview = lambda *args: None
show_step = lambda *args: None
rng = random.Random(550)
cases = [([5, 2, 4, 4, 1, 3, 8], 3), ([], 4), ([7], 3), ([4, 1, 3], 1), ([-2, -1, -1, 0], 4), ([2, 1, 0], 3), ([2, 3, 4], 0)]
cases += [([rng.randrange(-8, 9) for _ in range(rng.randrange(16))], rng.randrange(6)) for _ in range(30)]
for readings, k in cases:
    before = list(readings)
    expected = [(a, b) for a, b in zip(readings, readings[1:]) if b > a][:k]
    got = rising_preview(iter(readings), k)
    assert got == expected, f"rising_preview({before}, {k}) should be {expected}: each rise pairs a reading with the one immediately before it. Got {got!r}."
    assert readings == before, f"rising_preview changed the caller's list from {before} to {readings}."
