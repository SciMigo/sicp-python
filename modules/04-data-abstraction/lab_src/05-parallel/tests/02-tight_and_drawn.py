import random
def exact(a_low, a_high, b_low, b_high):
    par = lambda a, b: a * b / (a + b)
    return par(a_low, b_low), par(a_high, b_high)   # increasing in both resistances
rng = random.Random(214)
cases = [(6.12, 7.48, 4.465, 4.935), (10, 10, 10, 10), (1, 2, 1, 2), (100, 101, 0.5, 9)]
cases += [(a, a + rng.uniform(0, 6), b, b + rng.uniform(0, 6)) for a, b in [(rng.uniform(0.5, 60), rng.uniform(0.5, 60)) for _ in range(25)]]
from scimigo import _frame_count, _frame
saved = show_parallel
show_parallel = lambda *args: None
try:
    for a_low, a_high, b_low, b_high in cases:
        result = parallel(make_interval(a_low, a_high), make_interval(b_low, b_high))
        low, high = lower_bound(result), upper_bound(result)
        want_low, want_high = exact(a_low, a_high, b_low, b_high)
        allowed = 1.01 * (want_high - want_low) + 1e-9 * (1 + abs(want_high))
        assert high - low <= allowed, f"R1 in [{a_low:.3f}, {a_high:.3f}] with R2 in [{b_low:.3f}, {b_high:.3f}] really spans {want_high - want_low:.4f} ohms; your interval spans {high - low:.4f}. It includes resistances the pair can never have."
finally:
    show_parallel = saved
r1, r2 = make_interval(6.12, 7.48), make_interval(4.465, 4.935)
before = _frame_count()
result = parallel(r1, r2)
recorded = _frame_count() - before
assert recorded == 1, f"Call show_parallel once per call of parallel; recorded {recorded} frames."
objects = _frame(before)
bars = [o for o in objects if o['kind'] == 'rectangle']
assert len(bars) == 3, f"The picture has three bars: R1, R2 and the pair; found {len(bars)}."
label = str(round(lower_bound(result), 3)) + " to " + str(round(upper_bound(result), 3)) + " ohms"
assert any(o['kind'] == 'text' and o['value'] == label for o in objects), f"The third bar must be labelled with the interval you return: '{label}'. Pass show_parallel your result."
