import copy, random
show_call = lambda *args: None
rng = random.Random(3201)
for _ in range(40):
    count = rng.randint(2, 8)
    fs = [{"bindings": {"g": i}, "parent": rng.randrange(i) if i else None} for i in range(count)]
    env = rng.randrange(count)
    caller = rng.choice([i for i in range(count) if i != env])
    n = rng.randrange(0, 4)
    fn = {"params": ["p" + str(i) for i in range(n)], "env": env}
    args = [rng.randrange(-20, 21) for _ in range(n)]
    want = dict(zip(fn["params"], args))
    old_fs, old_fn, old_args = copy.deepcopy(fs), copy.deepcopy(fn), list(args)
    a = call_frame(fs, fn, args, caller)
    assert a == count and len(fs) == count + 1, f"A call appends exactly one frame and returns its index: expected index {count} in a list of {count + 1}, got {a!r} with {len(fs)} frames."
    assert fs[:count] == old_fs, "Existing frames, including the caller's, must not change."
    assert fs[a]["bindings"] == want, f"The new frame binds each parameter to its argument: expected {want}, got {fs[a]['bindings']}."
    assert fs[a]["parent"] == env, f"The function was defined in frame {env} and called from frame {caller}. The new frame's parent must be {env}; it is {fs[a]['parent']!r}."
    b = call_frame(fs, fn, args, caller)
    assert b == count + 1 and fs[b] is not fs[a] and fs[b]["bindings"] is not fs[a]["bindings"], "Every call gets a frame and a bindings dictionary of its own, even with the same function and arguments."
    assert fn == old_fn and args == old_args, "Do not change the function record or the argument list."
