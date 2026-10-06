show_step = lambda *args: None
calls = []
def f(x):
    calls.append(x)
    return x + 2
h = repeated(f, 5)
assert callable(h), "repeated must return a function."
assert calls == [], f"Building the repeated function must not call f; it called f on {calls}."
got = h(3)
assert got == 13, f"Five applications of 'add 2' to 3 give 13; got {got}."
assert calls == [3, 5, 7, 9, 11], f"Each application takes the previous result: expected f called on [3, 5, 7, 9, 11], saw {calls}."
calls.clear()
got = h(0)
assert got == 10 and calls == [0, 2, 4, 6, 8], f"A second call starts again from its own input: expected 10 via [0, 2, 4, 6, 8], got {got} via {calls}."
def never(x):
    raise AssertionError("With n = 0 the function f must not be called.")
marker = object()
assert repeated(never, 0)(marker) is marker, "Zero applications return the input itself."
got = repeated(lambda x: x * x, 2)(5)
assert got == 625, f"repeated(square, 2)(5) squares twice: 625; got {got}."
got = repeated(lambda s: s + '!', 3)('a')
assert got == 'a!!!', f"The input need not be a number: three applications of 'append !' to 'a' give 'a!!!'; got {got!r}."
try:
    got = repeated(lambda x: x + 1, 3000)(0)
except RecursionError:
    raise AssertionError("3000 applications overflowed Python's call stack. Apply f in a loop instead of nesting 3000 calls.")
assert got == 3000, f"3000 applications of 'add 1' to 0 give 3000; got {got}."
