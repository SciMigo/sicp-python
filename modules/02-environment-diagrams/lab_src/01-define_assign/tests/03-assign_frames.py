from scimigo import _frame_count, _frame
fs = [{"bindings": {"x": 1}, "parent": None},
      {"bindings": {"x": 0}, "parent": 0},
      {"bindings": {}, "parent": 1},
      {"bindings": {"x": 5}, "parent": 0},
      {"bindings": {}, "parent": 2}]
before = _frame_count()
try:
    owner = assign(fs, 4, "x", 9)
except NameError:
    raise AssertionError("From frame 4 the chain is 4, 2, 1, 0, and frame 1 binds x (to 0), so assign must not raise NameError.")
assert owner == 1, f"The nearest binding of x from frame 4 is in frame 1; assign returned {owner!r}."
recorded = _frame_count() - before
assert recorded == 3, f"assign visits frames 4, 2 and 1 and then stops, so it records 3 pictures; it recorded {recorded}. Call show_scope once per visited frame, before testing it."
for j, current in enumerate([4, 2, 1]):
    fig = next(o for o in _frame(before + j) if o["kind"] == "figure")["params"]
    assert fig["highlights"]["frames"] == {str(current): "current"}, f"Picture {j + 1} must highlight frame {current}, the frame being tested; it highlights {fig['highlights']['frames']}."
    shown = fig["frames"][1]["bindings"]
    assert shown == [{"name": "x", "value": "0"}], f"Picture {j + 1} is taken before the write, so frame 1 must still show x = 0; it shows {shown}."
assert fs[1]["bindings"]["x"] == 9 and fs[0]["bindings"]["x"] == 1 and fs[3]["bindings"]["x"] == 5, "After the walk, x is 9 in frame 1 and unchanged in frames 0 and 3."
