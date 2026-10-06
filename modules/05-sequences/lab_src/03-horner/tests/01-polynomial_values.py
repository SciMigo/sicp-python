import random
show_horner = lambda *args: None
show_nothing_yet = lambda *args: None
rng = random.Random(534)
cases = [(3, [2, -1, 3, 0, 1]), (0, [8, 2, 9]), (-2, [1, 0, 3]), (5, []), (7, [0]), (2, [9])]
cases += [(rng.randrange(-3, 4), [rng.randrange(-5, 6) for _ in range(rng.randrange(12))]) for _ in range(30)]
for x, coefficients in cases:
    before = list(coefficients)
    expected = sum(c * x ** i for i, c in enumerate(coefficients))
    got = horner(x, coefficients)
    assert got == expected, f"horner({x}, {before}) should be {expected}: coefficients run from the constant term upward. Got {got!r}."
    assert coefficients == before, f"horner changed the caller's list from {before} to {coefficients}."
