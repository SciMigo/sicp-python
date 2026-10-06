show = lambda *args: None
import random
rng = random.Random(132)
for _ in range(40):
    start = rng.randrange(-6, 7)
    step = rng.randrange(1, 4)
    stop = start + rng.randrange(-2, 12)
    points = list(range(start, stop + 1, step))
    term_calls, next_calls, pairs = [], [], []
    def term(x):
        term_calls.append(x)
        return x * x - 3
    def step_by(x):
        next_calls.append(x)
        return x + step
    def keep(result, value):
        assert isinstance(result, list), "Call combiner(result, term): the running result first, the new term second."
        pairs.append((tuple(result), value))
        return result + [value]
    got = accumulate(keep, [], term, start, step_by, stop)
    want = [x * x - 3 for x in points]
    assert got == want, f"From {start} to {stop} in steps of {step} the terms are {want}; your fold returned {got}."
    assert term_calls == points, f"Call term once per point, in order: expected {points}, saw {term_calls}."
    assert next_calls == points, f"Call next once per visited point to find the following one: expected {points}, saw {next_calls}."
    assert pairs == [(tuple(want[:i]), want[i]) for i in range(len(want))], "Call combiner(result, term) with the running result first and the new term second, once per point."
assert accumulate(lambda r, t: r + t, 0, lambda x: x, 1, lambda x: x + 1, 10) == 55, "With + and 0 this is the sum of 1..10, which is 55."
assert accumulate(lambda r, t: r * t, 1, lambda x: x, 1, lambda x: x + 1, 6) == 720, "With * and 1 this is 6 factorial, 720."
def never(*args):
    raise AssertionError("An empty range must not call term, next or combiner.")
marker = object()
assert accumulate(never, marker, never, 5, never, 4) is marker, "An empty range (a > b) returns null_value itself."
