from scimigo import _frame_count, _frame
before = _frame_count()
assert height(sample) == 3, "The demo hierarchy has height 3: root, child 1, and one of its children."
expected = [((0,), 1), ((1, 0), 1), ((1, 1), 1), ((1,), 2), ((2,), 1), ((), 3)]
recorded = _frame_count() - before
assert recorded == len(expected), f"Record one completion frame per node: 6 nodes, {recorded} frames."
for offset, (path, value) in enumerate(expected):
    objects = _frame(before + offset)
    figures = [o for o in objects if o['kind'] == 'figure']
    assert figures and figures[0]['type'] == 'tree', "Draw the hierarchy in each completion frame (call show)."
    node = sample
    for i in path: node = branches(node)[i]
    name = 'root' if not path else '.'.join(map(str, path))
    assert figures[0]['params']['highlights'] == {name + ':' + str(label(node)): 'current'}, f"Frame {offset + 1} should highlight {name}: children complete before their parent, left to right."
    assert any(o['kind'] == 'text' and o['value'] == 'Completed ' + name + ': ' + str(value) for o in objects), f"Frame {offset + 1} should show height {value} for the subtree at {name}."
