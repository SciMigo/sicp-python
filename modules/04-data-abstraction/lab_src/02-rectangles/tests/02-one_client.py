show_read = lambda *args: None
show_report = lambda *args: None
r = make_rect(make_point(2, 1), make_point(9, 4))
got = report(r, rect_width, rect_height)
assert got == (21, 20), f"For corners (2, 1) and (9, 4), report should return (21, 20); got {got!r}."
# A rectangle stored as a centre and two half-sides, with its own selectors.
for w, h in [(7, 3), (0, 8), (4, 4), (2.5, 1.5), (13, 2)]:
    other = {"centre": (10, 10), "half": (w / 2, h / 2)}
    seen = []
    def width(rect):
        seen.append("width")
        return 2 * rect["half"][0]
    def height(rect):
        seen.append("height")
        return 2 * rect["half"][1]
    try:
        got = report(other, width, height)
    except (TypeError, KeyError, IndexError):
        raise AssertionError("report failed on a rectangle stored a different way: use only the width and height selectors it is given.")
    assert got == (w * h, 2 * (w + h)), f"A {w} by {h} rectangle has area {w * h} and perimeter {2 * (w + h)}; report returned {got!r}."
    assert seen == ["width", "height"], f"report should call width once and then height once; it called {seen}."
