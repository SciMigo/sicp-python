show_counts = lambda *args: None
real_gcd = gcd
seen = []
def gcd(a, b):
    seen.append((a, b))
    return real_gcd(a, b)
try:
    for k in (0, 1, 4, 9):
        for strategy, want_calls in ((eager, 1), (lazy, 2 * k)):
            seen.clear()
            got = measure(strategy, 21, 35, k)
            assert isinstance(got, tuple) and len(got) == 2, f"measure returns a pair (result, calls); got {got!r}."
            result, calls = got
            assert result == [(3, 5)] * k, f"measure must return the strategy's own result; for {k} reads of 21/35 that is {[(3, 5)] * k}, got {result!r}."
            assert len(seen) == want_calls, f"{strategy.__name__} with {k} reads should reach the supplied gcd {want_calls} time(s) through your function; it reached it {len(seen)} time(s). Your function must do the real gcd work by calling gcd."
            assert calls == len(seen), f"{strategy.__name__} with {k} reads really made {len(seen)} gcd call(s); you reported {calls}."
    def unusual(n, d, k, g):
        assert g(12, 18) == 6, "The function you hand to a strategy must return what gcd returns."
        for _ in range(4):
            g(n, d)
        return 'done'
    seen.clear()
    got = measure(unusual, 12, 18, 3)
    assert got == ('done', 5), f"A strategy that calls its gcd five times should measure as ('done', 5); got {got!r}. Count calls as they happen; do not work them out from k or from the strategy."
    first = measure(lazy, 21, 35, 2)[1]
    second = measure(lazy, 21, 35, 2)[1]
    assert first == second == 4, f"Each measurement starts from zero: two identical runs gave {first} and {second}."
finally:
    gcd = real_gcd
