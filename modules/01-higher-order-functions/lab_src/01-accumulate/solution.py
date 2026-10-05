def accumulate(combiner, null_value, term, a, next, b):
    result = null_value
    xs, terms = [], []
    show(xs, terms, result)
    while a <= b:
        value = term(a)
        result = combiner(result, value)
        xs.append(a)
        terms.append(value)
        show(xs, terms, result)
        a = next(a)
    return result

from scimigo import canvas, figure, frame, text

def show(xs, terms, result):
    canvas(600, 360)
    if terms:
        figure("array_state", x=0, y=0, width=600, height=290, values=list(terms), indices=False)
    points = ", ".join(str(x) for x in xs) if xs else "none"
    text(15, 335, "visited x = " + points + "   result = " + str(result), size=18)
    frame()

def inc(x):
    return x + 1

def identity(x):
    return x

def times(result, term):
    return result * term

print(accumulate(times, 1, identity, 1, inc, 5))
