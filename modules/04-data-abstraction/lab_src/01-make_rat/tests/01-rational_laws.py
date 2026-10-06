import ast
for node in ast.walk(ast.parse(__source__)):
    names = [a.name for a in node.names] if isinstance(node, (ast.Import, ast.ImportFrom)) else []
    module = getattr(node, 'module', '') or ''
    assert 'fractions' not in names and module != 'fractions', "Build the constructor yourself: do not import the fractions module."
from math import gcd as _gcd
import random
show_gcd = lambda *args: None
show_rat = lambda *args: None
rng = random.Random(204)
cases = [(0, 7), (0, -7), (-8, -12), (8, -12), (-8, 12), (27, 9), (5, 1), (-5, -1)]
cases += [(rng.randrange(-150, 151), rng.choice([i for i in range(-30, 31) if i])) for _ in range(45)]
for n, d in cases:
    result = make_rat(n, d)
    assert isinstance(result, tuple) and len(result) == 2, f"make_rat({n}, {d}) must return a (numerator, denominator) tuple; got {result!r}."
    a, b = numer(result), denom(result)
    assert isinstance(a, int) and isinstance(b, int), f"make_rat({n}, {d}) gave {result!r}: both parts must stay integers (use // rather than /)."
    assert a * d == n * b, f"make_rat({n}, {d}) gave {a}/{b}, which is a different number from {n}/{d}."
    assert b > 0, f"make_rat({n}, {d}) gave {a}/{b}: keep the denominator positive and carry the sign on the numerator."
    assert _gcd(a, b) == 1, f"make_rat({n}, {d}) gave {a}/{b}, which is not in lowest terms."
try:
    make_rat(5, 0)
except ZeroDivisionError:
    pass
else:
    raise AssertionError("make_rat(5, 0) must raise ZeroDivisionError: no rational number has denominator zero.")
