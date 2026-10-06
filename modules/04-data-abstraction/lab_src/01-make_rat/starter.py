def make_rat(n, d):
    result = (0, 1)
    show_rat(n, d, result)
    return result

from scimigo import canvas, figure, frame, text

def numer(r):
    return r[0]

def denom(r):
    return r[1]

def show_gcd(a, b):
    canvas(600, 300)
    figure("array_state", x=0, y=0, width=600, height=220, values=[a, b], indices=False)
    text(12, 260, "Euclid: gcd(" + str(a) + ", " + str(b) + ")", size=18)
    frame()

def show_rat(n, d, result):
    canvas(600, 300)
    figure("array_state", x=0, y=0, width=600, height=220,
           values=[n, d, numer(result), denom(result)], indices=False)
    text(12, 260, str(n) + "/" + str(d) + " is stored as " + str(numer(result)) + "/" + str(denom(result)), size=18)
    frame()

print(make_rat(-8, -12))
