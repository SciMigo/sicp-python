from scimigo import _frame_count, _frame
r = make_rect(make_point(1, 1), make_point(10, 3))
before = _frame_count()
got = report(r, rect_width, rect_height)
assert got == (18, 22), f"For corners (1, 1) and (10, 3), report should return (18, 22); got {got!r}."
recorded = _frame_count() - before
assert recorded == 3, f"report records three frames: the width read, the height read, then the report; recorded {recorded}."
def values(index):
    figures = [o for o in _frame(index) if o['kind'] == 'figure']
    return figures[0]['params']['values'] if figures else None
def words(index):
    return [o['value'] for o in _frame(index) if o['kind'] == 'text']
assert values(before) == [9] and any('width' in t for t in words(before)), f"Frame 1 should show the width read, 9; it shows {values(before)}."
assert values(before + 1) == [2] and any('height' in t for t in words(before + 1)), f"Frame 2 should show the height read, 2; it shows {values(before + 1)}."
assert values(before + 2) == [9, 2, 18, 22], f"Frame 3 should show width, height, area and perimeter: [9, 2, 18, 22]; it shows {values(before + 2)}."
