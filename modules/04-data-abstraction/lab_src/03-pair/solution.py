def cons(x, y):
    return lambda choose: choose(x, y)

def cdr(z):
    return z(lambda p, q: q)

from scimigo import canvas, figure, frame, text

def car(z):
    return z(lambda p, q: p)

def show_pair(z):
    canvas(600, 300)
    figure("array_state", x=0, y=0, width=600, height=220,
           values=[str(car(z)), str(cdr(z))], cell_width=110, indices=False)
    text(12, 260, "car / cdr", size=18)
    frame()

show_pair(cons("east", "west"))
