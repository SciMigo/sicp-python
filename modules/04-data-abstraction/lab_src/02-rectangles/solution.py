def make_rect(corner, opposite):
    return (corner, opposite)

def rect_width(r):
    return abs(x_point(r[0]) - x_point(r[1]))

def rect_height(r):
    return abs(y_point(r[0]) - y_point(r[1]))

def report(rect, width, height):
    w = width(rect)
    show_read("width", w)
    h = height(rect)
    show_read("height", h)
    answer = (w * h, 2 * (w + h))
    show_report(w, h, *answer)
    return answer

from scimigo import canvas, figure, frame, text

def make_point(x, y):
    return (x, y)

def x_point(p):
    return p[0]

def y_point(p):
    return p[1]

def show_read(name, value):
    canvas(600, 300)
    figure("array_state", x=0, y=0, width=600, height=220, values=[value], indices=False)
    text(12, 260, "the client asked for " + name + " and was told " + str(value), size=18)
    frame()

def show_report(w, h, area, perimeter):
    canvas(600, 300)
    figure("array_state", x=0, y=0, width=600, height=220, values=[w, h, area, perimeter], indices=False)
    text(12, 260, "width / height / area / perimeter", size=18)
    frame()

rect = make_rect(make_point(2, 1), make_point(9, 4))
print(report(rect, rect_width, rect_height))
