from scimigo import _frame_count, _frame
golden = lambda x: 1 + 1 / x
def count(tolerance):
    calls, guess = 0, 1.0
    while True:
        new = golden(guess); calls += 1
        if abs(new - guess) < tolerance:
            return calls
        guess = new
tolerances = (0.001, 0.00001, 0.0000001)
rows = [(t, measure(golden, 1.0, t)[1]) for t in tolerances]
want = [(t, count(t)) for t in tolerances]
assert rows == want, f"On x -> 1 + 1/x at three new tolerances your counts {[c for _, c in rows]} do not match the calls that really happen."
before = _frame_count()
show_measure(rows)
objects = _frame(before)
bars = [o for o in objects if o['kind'] == 'rectangle']
assert len(bars) == 3, f"Draw one bar per tolerance; found {len(bars)}."
for t, calls in want:
    assert any(o['kind'] == 'text' and o['value'] == 'calls = ' + str(calls) for o in objects), f"The picture must show your measured count for tolerance {t}: 'calls = {calls}'."
