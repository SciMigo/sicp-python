import random
saved=show_preview;show_preview=lambda *args:None
try:
    rng=random.Random(550)
    cases=[([5,2,4,4,1,3,8],3),([],4),([7],3),([4,1,3],1),([-2,-1,-1,0],4),([2,1,0],3),([2,3,4],0)]
    cases += [([rng.randrange(-8,9) for _ in range(rng.randrange(16))],rng.randrange(6)) for _ in range(30)]
    for readings,k in cases:
        before=list(readings);expected=[(a,b) for a,b in zip(readings,readings[1:]) if b>a][:k]
        assert rising_preview(iter(readings),k)==expected,"Pairs must be consecutive in the original source; each rise uses the immediately preceding reading."
        assert readings==before,"Do not mutate the caller's collection."
finally:show_preview=saved
