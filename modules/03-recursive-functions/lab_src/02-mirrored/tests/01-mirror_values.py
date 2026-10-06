saved=show_window;show_window=lambda *args:None
class Whole(list):
    def __getitem__(self,key):
        if isinstance(key,slice):raise AssertionError("Do not slice the list: move the left and right boundaries instead.")
        return list.__getitem__(self,key)
try:
    cases=[[],[5],[2,2],[2,3],[1,2,3,1],[4,7,2,7,4],[1,2,2,1],[1,2,3,2,9]]
    import random
    rng=random.Random(31)
    cases += [[rng.randrange(4) for _ in range(rng.randrange(12))] for _ in range(35)]
    for plain in cases:
        want=plain==plain[::-1]
        items=Whole(plain)
        got=mirrored(items)
        assert got is want,f"mirrored({plain}) should be {want}; got {got!r}. A matching outside pair is not enough: the inside must be mirrored too."
        assert list(items)==plain,"Do not change the supplied list."
    assert mirrored(Whole([9,1,2,1,8]),1,3) is True,"With left=1 and right=3, only the window [1, 2, 1] of [9, 1, 2, 1, 8] is examined; it is mirrored."
    assert mirrored(Whole([9,1,2,3,8]),1,3) is False,"With left=1 and right=3, the window [1, 2, 3] of [9, 1, 2, 3, 8] is not mirrored."
finally:show_window=saved
