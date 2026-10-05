import ast
for node in ast.walk(ast.parse(__source__)):
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        assert node.id not in {'int', 'float'}, "Do not convert the supplied numbers with int() or float(): the check counts arithmetic on them."
show_stage = lambda *args: None
ops = [0]
class BudgetExceeded(BaseException): pass
limit = [100000]
def tick():
    ops[0] += 1
    if ops[0] > limit[0]: raise BudgetExceeded()
class Number(int):
    # Every arithmetic result stays a Number, so the count cannot be shed by a detour through -, abs or .real.
    def __mul__(self, other): tick(); return Number(int.__mul__(self, other))
    def __rmul__(self, other): tick(); return Number(int.__mul__(self, other))
    def __add__(self, other): tick(); return Number(int.__add__(self, other))
    def __radd__(self, other): tick(); return Number(int.__add__(self, other))
    def __sub__(self, other): tick(); return Number(int.__sub__(self, other))
    def __rsub__(self, other): tick(); return Number(int.__rsub__(self, other))
    def __neg__(self): tick(); return Number(int.__neg__(self))
    def __pos__(self): return self
    def __abs__(self): tick(); return Number(int.__abs__(self))
    real = property(lambda self: self)
    numerator = property(lambda self: self)
spec = [(Number(1), Number((i % 5) - 2)) for i in range(240)]
ops[0] = 0; limit[0] = 4 * len(spec)
try:
    service = make_service(spec)
except BudgetExceeded:
    raise AssertionError('Setup used more than four arithmetic operations per record (240 records, budget 960).')
ops[0] = 0; limit[0] = 4 * 80
try:
    answers = [service(Number(x)) for x in range(80)]
except BudgetExceeded:
    raise AssertionError('80 readings used more than 320 arithmetic operations: each reading is redoing work that depends on the number of records.')
assert answers == list(range(80)), "These 240 records cancel out, so every reading should come back unchanged."
