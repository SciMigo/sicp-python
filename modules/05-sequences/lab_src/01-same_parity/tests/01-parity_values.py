import random
show_parity = lambda *args: None
rng = random.Random(520)
cases = [(8, 3, 12, 0, 7, 8), (-3, 2, -1, 0, 5), (0,), (2, 2, 2), (1,)]
cases += [tuple(rng.randrange(-20, 21) for _ in range(rng.randrange(1, 16))) for _ in range(30)]
for values in cases:
    expected = [x for x in values if x % 2 == values[0] % 2]
    got = same_parity(*values)
    assert got == expected, f"same_parity{values} should be {expected}: every argument with the parity of {values[0]}, in order, repeats kept. Got {got!r}."
