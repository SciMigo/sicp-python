from scimigo import _frame_count, _frame
h = repeated(lambda x: x - 3, 4)
before = _frame_count()
got = h(20)
assert got == 8, f"Four applications of 'subtract 3' to 20 give 8; got {got}."
recorded = _frame_count() - before
assert recorded == 5, f"n = 4 needs the input frame and one frame per application: 5 frames, recorded {recorded}."
for i, value in enumerate([20, 17, 14, 11, 8]):
    objects = _frame(before + i)
    fig = next((o for o in objects if o['kind'] == 'figure'), None)
    assert fig and fig['params']['values'] == [value], f"Frame {i + 1} must show the value after {i} applications, {value}."
    assert any(o['kind'] == 'text' and o['value'] == f'After {i} applications: {value}' for o in objects), f"Frame {i + 1} must read 'After {i} applications: {value}'."
before = _frame_count()
repeated(lambda x: x, 0)(7)
recorded = _frame_count() - before
assert recorded == 1, f"With n = 0 there is only the input frame; recorded {recorded}."
before = _frame_count()
repeated(lambda x: x + 1, 40)(0)
recorded = _frame_count() - before
assert recorded == 0, f"For n above 12 draw nothing; n = 40 recorded {recorded} frames."
