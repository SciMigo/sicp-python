from scimigo import _frame_count, _frame
def count(strategy, k):
    calls = [0]
    def g(a, b):
        calls[0] += 1
        return gcd(a, b)
    strategy(33, 77, k, g)
    return calls[0]
reads = (2, 5, 9)
rows = [(k, measure(eager, 33, 77, k)[1], measure(lazy, 33, 77, k)[1]) for k in reads]
want = [(k, count(eager, k), count(lazy, k)) for k in reads]
assert rows == want, f"At {reads} reads your (reads, eager, lazy) rows are {rows}; they do not match the calls that really happen."
before = _frame_count()
show_counts(rows)
objects = _frame(before)
bars = sum(o['kind'] == 'rectangle' for o in objects)
assert bars == 6, f"Draw two bars for each of the three rows; found {bars}."
words = [o['value'] for o in objects if o['kind'] == 'text']
for k, a, b in want:
    assert 'eager=' + str(a) in words and 'lazy=' + str(b) in words, f"The picture must label the {k}-read row with your measured counts."
