This is SICP's exercise 2.3: rectangles in the plane, with area and perimeter that do not care how a rectangle is stored. There are two layers to write.

Below the barrier: `make_rect(corner, opposite)` builds a rectangle with sides parallel to the axes from two opposite corner points, given in either order. `rect_width(r)` and `rect_height(r)` return its two side lengths, never negative. Reach the coordinates only through `x_point` and `y_point`; the checks swap in points that are not tuples.

Above the barrier: `report(rect, width, height)` returns `(area, perimeter)` for any rectangle, using only the two selectors it is handed. Call `width(rect)` once and then `height(rect)` once. After each read call `show_read("width", w)` or `show_read("height", h)`, and finish with `show_report(w, h, area, perimeter)`. The checks hand `report` a rectangle stored a completely different way.

Answer the question before you run the demo.