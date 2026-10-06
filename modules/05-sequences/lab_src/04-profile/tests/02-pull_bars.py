from scimigo import _frame_count, _frame
def count(strategy, items, k):
    pulls = [0]
    def reading(values):
        for item in source(values):
            pulls[0] += 1
            yield item
    strategy(items, k, reading)
    return pulls[0]
sizes = (10, 30, 70)
rows = [(n, profile(eager, list(range(1, n + 1)), 2)[1], profile(lazy, list(range(1, n + 1)), 2)[1]) for n in sizes]
want = [(n, count(eager, list(range(1, n + 1)), 2), count(lazy, list(range(1, n + 1)), 2)) for n in sizes]
assert rows == want, f"For two results from sources of {sizes} items, your (size, eager, lazy) rows are {rows}; they do not match the pulls that really happen."
before = _frame_count()
show_pulls(rows)
recorded = _frame_count() - before
assert recorded == 1, f"show_pulls draws one picture; recorded {recorded}."
objects = _frame(before)
bars = [o for o in objects if o['kind'] == 'rectangle']
words = [o['value'] for o in objects if o['kind'] == 'text']
assert len(bars) == 6, f"Three sizes need an eager bar and a lazy bar each; found {len(bars)}."
for n, a, b in want:
    assert 'eager pulls=' + str(a) in words and 'lazy pulls=' + str(b) in words, f"The picture should label the {n}-item row with your measured counts."
