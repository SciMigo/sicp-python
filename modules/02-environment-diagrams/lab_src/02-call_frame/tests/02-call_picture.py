from scimigo import _frame_count, _frame
fs = [{"bindings": {"k": 1}, "parent": None},
      {"bindings": {"k": 2}, "parent": 0},
      {"bindings": {"k": 3}, "parent": 0},
      {"bindings": {"k": 4}, "parent": 2}]
before = _frame_count()
new = call_frame(fs, {"params": ["reading"], "env": 1}, [7], 3)
recorded = _frame_count() - before
assert recorded == 1, f"Call show_call exactly once per call; {recorded} pictures were recorded."
objects = _frame(before)
fig = next(o for o in objects if o["kind"] == "figure")["params"]
ids = [f["id"] for f in fig["frames"]]
assert ids == ["0", "1", "4"], f"The picture shows the new frame under its lookup path. The function was defined in frame 1, so the path is frame 4, then 1, then 0; the picture shows frames {ids} (top to bottom)."
assert fig["highlights"]["frames"] == {"4": "current"}, f"Pass the new frame's index to show_call so that it is the one highlighted; highlighted: {fig['highlights']['frames']}."
assert fig["frames"][2]["bindings"] == [{"name": "reading", "value": "7"}], f"The new frame must show reading = 7; it shows {fig['frames'][2]['bindings']}."
assert any(o["kind"] == "text" and o["value"] == "Caller: frame 3. New: frame 4" for o in objects), "Pass the caller's index as the third argument of show_call, so the caption can name it."
