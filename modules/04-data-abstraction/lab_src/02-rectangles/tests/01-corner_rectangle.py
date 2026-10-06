import random
show_read = lambda *args: None
show_report = lambda *args: None
rng = random.Random(23)
corners = [((2, 1), (9, 4)), ((9, 4), (2, 1)), ((2, 4), (9, 1)), ((0, 0), (0, 5)), ((-3, -2), (4, 6))]
corners += [((rng.randrange(-20, 21), rng.randrange(-20, 21)), (rng.randrange(-20, 21), rng.randrange(-20, 21))) for _ in range(30)]
for (ax, ay), (bx, by) in corners:
    r = make_rect(make_point(ax, ay), make_point(bx, by))
    got = (rect_width(r), rect_height(r))
    want = (abs(ax - bx), abs(ay - by))
    assert got == want, f"Corners ({ax}, {ay}) and ({bx}, {by}) give sides {want}; rect_width and rect_height returned {got}. Corners may arrive in either order."
# The same rectangle code must work when points are stored another way.
tuple_points = (make_point, x_point, y_point)
make_point = lambda x, y: {"east": x, "north": y}
x_point = lambda p: p["east"]
y_point = lambda p: p["north"]
try:
    r = make_rect(make_point(2, 1), make_point(9, 4))
    try:
        got = (rect_width(r), rect_height(r))
    except (TypeError, KeyError, IndexError) as error:
        raise AssertionError("With points stored as dictionaries your rectangle code failed: read coordinates with x_point and y_point, never by indexing a point.")
    assert got == (7, 3), f"With points stored as dictionaries the sides should still be (7, 3); got {got}."
finally:
    make_point, x_point, y_point = tuple_points
