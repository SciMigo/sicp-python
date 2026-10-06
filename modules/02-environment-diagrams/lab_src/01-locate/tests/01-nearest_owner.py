import random, copy
saved=show_scope
show_scope=lambda *args:None
rng=random.Random(2205)
for _ in range(45):
    count=rng.randint(1,18)
    fs=[{"bindings":{},"parent":i-1 if i else None} for i in range(count)]
    for i in range(count):
        if rng.random()<.4: fs[i]["bindings"]["x"]=rng.choice([None,False,0,-8,13])
    snapshot=copy.deepcopy(fs)
    owners=[i for i in range(count) if "x" in fs[i]["bindings"]]
    if owners:
        owner=max(owners)
        assert locate(fs,count-1,"x")== (fs[owner]["bindings"]["x"],owner), "Follow parents and stop at the nearest present binding."
    else:
        try:locate(fs,count-1,"x")
        except NameError:pass
        else:raise AssertionError("Missing names must raise NameError.")
    assert fs==snapshot,"Lookup must not change bindings."
branched=[{'bindings':{'x':4},'parent':None},{'bindings':{'x':99},'parent':0},{'bindings':{},'parent':0}]
assert locate(branched,2,'x')==(4,0), 'Follow the supplied parent, not adjacent list indices.'
show_scope=saved
