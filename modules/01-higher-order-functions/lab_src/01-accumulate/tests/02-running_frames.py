from scimigo import _frame_count, _frame
before = _frame_count()
got = accumulate(lambda r, t: r + t, 0, lambda x: x * x, 2, lambda x: x + 1, 5)
assert got == 54, f"4 + 9 + 16 + 25 is 54; your fold returned {got}."
recorded = _frame_count() - before
assert recorded == 5, f"Four points need one frame before the first point and one after each: 5 frames, recorded {recorded}."
xs, terms, results = [2, 3, 4, 5], [4, 9, 16, 25], [0, 4, 13, 29, 54]
for i in range(5):
    objects = _frame(before + i)
    figures = [o for o in objects if o['kind'] == 'figure']
    if i == 0:
        assert not figures, "The first frame shows the state before any point: no terms yet."
    else:
        assert figures and figures[0]['params']['values'] == terms[:i], f"Frame {i + 1} must show the terms folded in so far, {terms[:i]}."
    points = ", ".join(str(x) for x in xs[:i]) if i else "none"
    label = "visited x = " + points + "   result = " + str(results[i])
    assert any(o['kind'] == 'text' and o['value'] == label for o in objects), f"Frame {i + 1} must read '{label}': pass show the points visited so far and the running result."
