from scimigo import _frame_count, _frame
before = _frame_count(); show_badges(prepare_badges([6, -1, 6]), 4)
recorded = _frame_count() - before
assert recorded == 1, f"show_badges draws one picture; {recorded} were recorded. Do not draw inside prepare_badges."
fig = next(o for o in _frame(before) if o["kind"] == "figure")
assert fig["params"]["values"] == [6, -1, 6], f"Set up with [6, -1, 6], the picture must show the prefixes 6, -1, 6 that the three callables return; it shows {fig['params']['values']}."
