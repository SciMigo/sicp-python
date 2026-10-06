import random
def exact(a_low, a_high, b_low, b_high):
    par = lambda a, b: a * b / (a + b)
    return par(a_low, b_low), par(a_high, b_high)   # increasing in both resistances
rng = random.Random(214)
cases = [(6.12, 7.48, 4.465, 4.935), (10, 10, 10, 10), (1, 2, 1, 2), (100, 101, 0.5, 9)]
cases += [(a, a + rng.uniform(0, 6), b, b + rng.uniform(0, 6)) for a, b in [(rng.uniform(0.5, 60), rng.uniform(0.5, 60)) for _ in range(25)]]
show_parallel = lambda *args: None
def run(label):
    for a_low, a_high, b_low, b_high in cases:
        try:
            result = parallel(make_interval(a_low, a_high), make_interval(b_low, b_high))
            low, high = lower_bound(result), upper_bound(result)
        except (TypeError, KeyError, IndexError):
            raise AssertionError(f"parallel failed when intervals are stored as {label}: build and read them only with make_interval, lower_bound and upper_bound.")
        want_low, want_high = exact(a_low, a_high, b_low, b_high)
        slack = 1e-9 * (1 + abs(want_high))
        assert low <= want_low + slack and high >= want_high - slack, f"R1 in [{a_low:.3f}, {a_high:.3f}] and R2 in [{b_low:.3f}, {b_high:.3f}] can combine to anything from {want_low:.4f} to {want_high:.4f}; your interval [{low:.4f}, {high:.4f}] leaves some of that out."
run("tuples")
# The same client with intervals stored as a centre and a half-width.
tuple_package = (make_interval, lower_bound, upper_bound)
make_interval = lambda low, high: {"centre": (low + high) / 2, "half": (high - low) / 2}
lower_bound = lambda i: i["centre"] - i["half"]
upper_bound = lambda i: i["centre"] + i["half"]
try:
    run("a centre and a half-width")
finally:
    make_interval, lower_bound, upper_bound = tuple_package
