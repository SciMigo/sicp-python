import random
saved=show_parity;show_parity=lambda *args:None
try:
    rng=random.Random(520)
    cases=[(8,3,12,0,7,8),(-3,2,-1,0,5), (0,), (2,2,2), (1,)]
    cases += [tuple(rng.randrange(-20,21) for _ in range(rng.randrange(1,16))) for _ in range(30)]
    for values in cases:
        expected=[x for x in values if x%2==values[0]%2]
        assert same_parity(*values)==expected,"Preserve matching values, their order and their repeated occurrences."
finally:show_parity=saved
