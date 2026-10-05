saved=show_window;show_window=lambda *args:None
try:
    cases=[[],[5],[2,2],[2,3],[1,2,3,1],[4,7,2,7,4],[1,2,2,1],[1,2,3,2,9]]
    import random
    rng=random.Random(31)
    cases += [[rng.randrange(4) for _ in range(rng.randrange(12))] for _ in range(35)]
    for items in cases:
        before=list(items)
        assert mirrored(items)==(items==items[::-1]),"Compare all matching positions, including inside the outside pair."
        assert items==before,"Do not mutate the supplied sequence."
    assert mirrored([9,1,2,1,8],1,3) is True
    assert mirrored([9,1,2,3,8],1,3) is False
finally:show_window=saved
