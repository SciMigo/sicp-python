import copy, random
show_scope = lambda *args: None
rng = random.Random(3102)
def nearest(fs, current, name):
    while current is not None:
        if name in fs[current]["bindings"]: return current
        current = fs[current]["parent"]
    return None
for _ in range(60):
    count = rng.randint(1, 12)
    fs = [{"bindings": {"other": i}, "parent": rng.randrange(i) if i else None} for i in range(count)]
    for f in fs:
        if rng.random() < .35: f["bindings"]["x"] = rng.choice([None, False, 0, -8, 13])
    current = rng.randrange(count)
    owner = nearest(fs, current, "x")
    before = copy.deepcopy(fs)
    try:
        result = assign(fs, current, "x", 77)
    except NameError:
        assert owner is None, f"Frame {owner} binds x (to {before[owner]['bindings']['x']!r}), so assign from frame {current} must change it, not raise NameError. A binding to None, False or 0 is still a binding."
        assert fs == before, "When no frame binds the name, assign raises NameError and changes nothing."
        continue
    assert owner is not None, f"No frame on the chain from frame {current} binds x, so assign must raise NameError; it returned {result!r}. Assignment never creates a binding."
    assert result == owner, f"assign returns the index of the frame it changed: expected {owner}, got {result!r}. Follow each frame's parent link; parents are not always the previous index."
    expected = copy.deepcopy(before); expected[owner]["bindings"]["x"] = 77
    assert fs == expected, f"Only frame {owner}, the nearest frame that binds x, may change. Farther bindings of x and every other name stay as they were."
