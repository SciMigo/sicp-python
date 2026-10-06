from scimigo import _frame_count, _frame
before = _frame_count()
answer = run_trace([2, 3, 5, 6, 9], 2)
assert answer == [103, 106], f"run_trace([2, 3, 5, 6, 9], 2) should return [103, 106]; got {answer!r}."
recorded = _frame_count() - before
assert recorded == len(events), f"Every event draws one frame: {len(events)} events, {recorded} frames. Use emit for outputs rather than drawing yourself."
seen, made = [], []
for i, (kind, value) in enumerate(events):
    if kind == 'pull':
        seen.append(value)
    if kind == 'output':
        made.append(value)
    objects = _frame(before + i)
    rows = [o['params']['values'] for o in objects if o['kind'] == 'figure']
    expected = ([list(seen)] if seen else []) + ([list(made)] if made else [])
    assert rows == expected, f"Frame {i + 1} ({kind}: {value}) should show pulled {seen} and outputs {made}; it shows {rows}."
    assert any(o['kind'] == 'text' and o['value'] == kind + ': ' + str(value) for o in objects), f"Frame {i + 1} should be labelled '{kind}: {value}'."
