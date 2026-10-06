def parallel(r1, r2):
    result = div_interval(mul_interval(r1, r2), add_interval(r1, r2))
    show_parallel(r1, r2, result)
    return result

from scimigo import canvas, rectangle, text, frame

def make_interval(low, high):
    return (low, high)

def lower_bound(i):
    return i[0]

def upper_bound(i):
    return i[1]

def make_center_percent(center, percent):
    half = abs(center) * percent / 100
    return make_interval(center - half, center + half)

def add_interval(x, y):
    return make_interval(lower_bound(x) + lower_bound(y), upper_bound(x) + upper_bound(y))

def mul_interval(x, y):
    products = [a * b for a in (lower_bound(x), upper_bound(x)) for b in (lower_bound(y), upper_bound(y))]
    return make_interval(min(products), max(products))

def div_interval(x, y):
    if lower_bound(y) <= 0 <= upper_bound(y):
        raise ValueError("cannot divide by an interval that contains zero")
    return mul_interval(x, make_interval(1 / upper_bound(y), 1 / lower_bound(y)))

def show_parallel(r1, r2, result):
    canvas(600, 330)
    rows = [("R1", r1, "#276bb0"), ("R2", r2, "#276bb0"), ("together", result, "#763aed")]
    top = max(upper_bound(i) for name, i, color in rows) or 1
    for n, (name, i, color) in enumerate(rows):
        y = 20 + 100 * n
        low, high = lower_bound(i), upper_bound(i)
        text(12, y + 22, name, size=18)
        rectangle(110 + 460 * low / top, y, max(2, 460 * (high - low) / top), 30, color=color)
        text(110, y + 58, str(round(low, 3)) + " to " + str(round(high, 3)) + " ohms", size=16)
    frame()

r1 = make_center_percent(6.8, 10)
r2 = make_center_percent(4.7, 5)
together = parallel(r1, r2)
print(round(lower_bound(together), 3), round(upper_bound(together), 3))
