import random
saved=show_box;show_box=lambda *a:None
rng=random.Random(620)
for _ in range(25):
    starts=[rng.randrange(-30,31),rng.randrange(-30,31)]
    boxes=[make_box(s) for s in starts];expected=starts[:]
    for _ in range(25):
        i=rng.randrange(2);op=rng.randrange(3);change,read,reset=boxes[i]
        if op==0:
            delta=rng.randrange(-10,11);expected[i]+=delta
            assert change(delta)==expected[i],"Changes must accumulate in one shared binding."
        elif op==1:assert read()==expected[i],"Reads must see the current shared value."
        else:
            expected[i]=starts[i];assert reset()==expected[i],"Reset must restore the original start."
        assert boxes[1-i][1]()==expected[1-i],"Separate factory calls must stay independent."
show_box=saved
