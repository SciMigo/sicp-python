show_pulls = lambda *args: None
original = source
for items, k in [(list(range(1, 18)), 2), ([3, 4, 4, 7, 8], 2), ([], 0), ([1, 2], 5), ([4, 8], 0)]:
    matches = [x + 10 for x in items if x % 4 == 0][:k]
    needed = accepted = 0
    if k:
        for x in items:
            needed += 1
            if x % 4 == 0:
                accepted += 1
                if accepted == k:
                    break
    got = profile(eager, items, k)
    assert got == (matches, len(items)), f"eager on {len(items)} items with k={k} returns {matches} after pulling all {len(items)}; profile gave {got!r}."
    got = profile(lazy, items, k)
    assert got == (matches, needed), f"lazy on {items if len(items) < 9 else str(len(items)) + ' items'} with k={k} returns {matches} after pulling {needed}; profile gave {got!r}. Count items as they are yielded, including rejected ones."
    assert source is original, "Leave the supplied source as it is: hand the strategy a new function instead."
def unusual(items, k, read_source):
    return list(islice(read_source(items), 2))
got = profile(unusual, [7, 8, 9], 0)
assert got == ([7, 8], 2), f"A strategy that pulls two items should measure as ([7, 8], 2); got {got!r}. Count what happens rather than working it out from k."
first, second = profile(lazy, [4, 8, 12], 2)[1], profile(lazy, [4, 8, 12], 2)[1]
assert first == second == 2, f"Each measurement starts from zero: two identical runs gave {first} and {second}."
def broken(items, k, read_source):
    next(read_source(items))
    raise ValueError('expected')
try:
    profile(broken, [1], 1)
except ValueError:
    pass
else:
    raise AssertionError("If the strategy raises, profile should let the error through.")
