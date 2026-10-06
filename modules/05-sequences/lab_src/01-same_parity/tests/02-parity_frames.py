from scimigo import _frame_count, _frame
values = [5, 2, 9, 9, 0]
before = _frame_count()
result = same_parity(*values)
assert result == [5, 9, 9], f"same_parity(5, 2, 9, 9, 0) should be [5, 9, 9]; got {result!r}."
recorded = _frame_count() - before
assert recorded == len(values), f"Five arguments need five frames, one after each; recorded {recorded}."
for i in range(len(values)):
    prefix = values[:i + 1]
    kept = [x for x in prefix if x % 2 == 1]
    rows = [o['params']['values'] for o in _frame(before + i) if o['kind'] == 'figure']
    assert len(rows) == 2, f"Frame {i + 1} should have two rows, visited and kept; it has {len(rows)}."
    assert rows[0] == prefix and rows[1] == kept, f"Frame {i + 1} should show visited {prefix} and kept {kept}; it shows {rows[0]} and {rows[1]}."
