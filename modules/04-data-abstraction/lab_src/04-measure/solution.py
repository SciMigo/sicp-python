def measure(strategy, n, d, k):
    calls = 0
    def counted(a, b):
        nonlocal calls
        calls += 1
        return gcd(a, b)
    answer = strategy(n, d, k, counted)
    return answer, calls

from scimigo import canvas, rectangle, text, frame

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a

def eager(n, d, k, gcd):
    """Reduce once, when the fraction is built; then read both parts k times."""
    g = gcd(n, d)
    stored = (n // g, d // g)
    return [(stored[0], stored[1]) for _ in range(k)]

def lazy(n, d, k, gcd):
    """Store the raw parts; reduce every time a part is read."""
    stored = (n, d)
    def numer():
        return stored[0] // gcd(stored[0], stored[1])
    def denom():
        return stored[1] // gcd(stored[0], stored[1])
    return [(numer(), denom()) for _ in range(k)]

def show_counts(rows):
    canvas(600, 370)
    largest = max([1] + [count for k, a, b in rows for count in (a, b)])
    for i, (k, a, b) in enumerate(rows):
        y = i * 115
        text(12, y + 20, "reads=" + str(k), size=18)
        rectangle(145, y + 25, 400 * a / largest, 20, color="#276bb0")
        text(145, y + 64, "eager=" + str(a), size=17)
        rectangle(145, y + 72, 400 * b / largest, 20, color="#763aed")
        text(145, y + 110, "lazy=" + str(b), size=17)
    frame()

rows = []
for k in (0, 3, 12):
    rows.append((k, measure(eager, 21, 35, k)[1], measure(lazy, 21, 35, k)[1]))
show_counts(rows)
