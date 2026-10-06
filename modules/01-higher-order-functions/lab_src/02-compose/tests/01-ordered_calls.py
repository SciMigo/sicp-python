show_stage = lambda *args: None
calls = []
def f(x):
    calls.append(('f', x))
    return x - 4
def g(x):
    calls.append(('g', x))
    return 3 * x
h = compose(f, g)
assert callable(h), "compose must return a function."
assert calls == [], f"Building the composition must not call f or g; it called {calls}."
got = h(2)
assert got == 2, f"g(2) is 6 and f(6) is 2; your function returned {got}."
assert calls == [('g', 2), ('f', 6)], f"Call g on the input, then f on g's result: expected [('g', 2), ('f', 6)], saw {calls}."
calls.clear()
got = h(-3)
assert got == -13 and calls == [('g', -3), ('f', -9)], f"A second call starts from its own input: expected -13 via [('g', -3), ('f', -9)], got {got} via {calls}."
k = compose(g, f)
assert (h(5), k(5)) == (11, 3), "Two compositions built from the same functions in different orders must stay independent: f(g(5)) is 11 and g(f(5)) is 3."
