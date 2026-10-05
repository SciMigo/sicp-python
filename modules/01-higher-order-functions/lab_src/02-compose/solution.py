def compose(f, g):
    def composed(x):
        middle = g(x)
        show_stage("g", x, middle)
        result = f(middle)
        show_stage("f", middle, result)
        return result
    return composed

from scimigo import canvas, figure, frame, text

def show_stage(name, value, result):
    canvas(600, 360)
    figure("array_state", x=0, y=0, width=600, height=290, values=[value, result], indices=False)
    text(15, 335, name + ": " + str(value) + " -> " + str(result), size=18)
    frame()

def square(x):
    return x * x

def inc(x):
    return x + 1

h = compose(square, inc)
answer = h(6)
show_stage("compose(square, inc)", 6, answer)
print(answer)
