import copy, random
show_scope = lambda *args: None
rng = random.Random(3101)
for _ in range(40):
    count = rng.randint(1, 9)
    fs = [{"bindings": {}, "parent": i - 1 if i else None} for i in range(count)]
    for f in fs:
        if rng.random() < .5: f["bindings"]["x"] = rng.choice([None, False, 0, -8, 13])
        if rng.random() < .3: f["bindings"]["y"] = rng.randrange(50)
    current = rng.randrange(count)
    name = rng.choice(["x", "y", "fresh"])
    value = rng.choice([None, 0, 41, "text"])
    before = copy.deepcopy(fs)
    result = define(fs, current, name, value)
    assert result is None, f"define returns nothing; it returned {result!r}."
    assert name in fs[current]["bindings"] and fs[current]["bindings"][name] == value, f"After define(frames, {current}, {name!r}, {value!r}) frame {current} must bind {name!r} to {value!r}; its bindings are {fs[current]['bindings']}."
    expected = copy.deepcopy(before); expected[current]["bindings"][name] = value
    assert fs == expected, f"define changes only frame {current}. A parent that binds the same name keeps its own binding; frames were changed elsewhere."
