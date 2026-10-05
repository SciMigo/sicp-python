def measure(f, guess, tolerance):
    return None, 0

import math
from scimigo import canvas, rectangle, text, frame

def fixed_point(f, guess, tolerance):
    for _ in range(100000):
        new = f(guess)
        if abs(new - guess) < tolerance:
            return new
        guess = new
    raise ValueError("no fixed point found after 100000 steps")

def show_measure(rows):
    canvas(600, 300)
    largest = max(calls for label, calls in rows) or 1
    for i, (label, calls) in enumerate(rows):
        rectangle(170, 25 + 90 * i, 380 * calls / largest, 35, color="#276bb0")
        text(12, 48 + 90 * i, "tolerance " + str(label), size=17)
        text(175, 85 + 90 * i, "calls = " + str(calls), size=17)
    frame()

rows = [(tolerance, measure(math.cos, 1.0, tolerance)[1]) for tolerance in (0.01, 0.0001, 0.000001)]
show_measure(rows)
