from scimigo import _frame_count, _frame
before = _frame_count()
got = totals(sample)
assert got == 26, f"The six labels 4, 7, 0, 9, 9 and -3 sum to 26; totals returned {got}."
expected = [((0,), 7), ((1, 0), 9), ((1, 1), 9), ((1,), 18), ((2,), -3), ((), 26)]
recorded = _frame_count() - before
assert recorded == len(expected), f"Record one completion frame per node: 6 nodes, {recorded} frames."
for offset, (path, value) in enumerate(expected):
    objects = _frame(before + offset)
    figures = [o for o in objects if o['kind'] == 'figure']
    assert figures and figures[0]['type'] == 'tree', "Draw the hierarchy in each completion frame (call show)."
    node = sample
    for i in path: node = branches(node)[i]
    name = 'root' if not path else '.'.join(map(str, path))
    assert figures[0]['params']['highlights'] == {name + ':' + str(label(node)): 'current'}, f"Frame {offset + 1} should highlight {name}: a node completes only after all of its children."
    assert any(o['kind'] == 'text' and o['value'] == 'Completed ' + name + ': ' + str(value) for o in objects), f"Frame {offset + 1} should show the subtree sum {value} at {name}."
