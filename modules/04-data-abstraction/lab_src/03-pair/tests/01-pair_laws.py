show_pair = lambda *args: None
first = lambda z: z(lambda p, q: p)
second = lambda z: z(lambda p, q: q)
for x, y in [(4, 9), (None, False), (0, ''), ([], {}), ('left', 'right')]:
    calls = []
    z = cons(x, y)
    assert callable(z), f"cons({x!r}, {y!r}) must return a function; got {z!r}."
    def choose(a, b):
        calls.append((a, b))
        return 'chosen'
    got = z(choose)
    assert len(calls) == 1, f"A pair calls the function it is given exactly once; it called it {len(calls)} times."
    assert calls[0][0] is x and calls[0][1] is y, f"cons({x!r}, {y!r}) should pass its own two parts, in order; it passed {calls[0]!r}."
    assert got == 'chosen', f"A pair returns whatever the function it was given returns; it returned {got!r}."
    assert first(z) is x and second(z) is y, f"The parts of cons({x!r}, {y!r}) must come back as the same objects."
a, b = cons(3, 5), cons(7, 11)
assert (first(a), second(b), second(a), first(b)) == (3, 11, 5, 7), "Two pairs must keep their own parts: building the second changed the first."
