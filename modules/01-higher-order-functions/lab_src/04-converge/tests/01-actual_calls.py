show_measure = lambda *args: None
import math
def search(f, guess, tolerance):
    for _ in range(100000):
        new = f(guess)
        if abs(new - guess) < tolerance:
            return new
        guess = new
cases = [(math.cos, 1.0, 1e-3), (lambda x: 1 + 1 / x, 1.0, 1e-5),
         (lambda y: (y + 10 / y) / 2, 1.0, 1e-7), (lambda x: (x + 3) / 2, 0.0, 1e-4)]
for f, guess, tolerance in cases:
    seen = []
    def watched(x, f=f):
        seen.append(x)
        return f(x)
    want_answer = search(f, guess, tolerance)
    result = measure(watched, guess, tolerance)
    assert isinstance(result, tuple) and len(result) == 2, "measure returns a pair: (answer, calls)."
    answer, reported = result
    assert answer is not None and abs(answer - want_answer) < 1e-12, f"Return the answer fixed_point found ({want_answer}); got {answer}."
    assert reported == len(seen), f"f was really called {len(seen)} times during your run but you reported {reported}."
    assert len(seen) > 0, "Your run never called f: pass a function that calls it to fixed_point."
# A search that wastes one call per step. An honest count follows it.
def wasteful(f, guess, tolerance):
    for _ in range(100000):
        f(guess)
        new = f(guess)
        if abs(new - guess) < tolerance:
            return new
        guess = new
fixed_point = wasteful
seen = []
def watched(x):
    seen.append(x)
    return math.cos(x)
answer, reported = measure(watched, 1.0, 1e-3)
plain = []
search(lambda x: plain.append(x) or math.cos(x), 1.0, 1e-3)
assert len(seen) == 2 * len(plain), f"Use the supplied fixed_point, not your own loop: with the wasteful search swapped in, f should be called {2 * len(plain)} times, but it was called {len(seen)} times."
assert reported == len(seen), f"The wasteful search called f {len(seen)} times and you reported {reported}: count calls as they happen instead of deriving the number."
