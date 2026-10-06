import ast
for node in ast.walk(ast.parse(__source__)):
    if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load):
        assert node.id not in {'int','float'}, "Do not convert the supplied numeric values: preserve the arithmetic meter."
show_stage=lambda *args: None
ops=[0]
class BudgetExceeded(BaseException): pass
limit=[100000]
def tick():
    ops[0]+=1
    if ops[0]>limit[0]: raise BudgetExceeded()
class Number(int):
    def __mul__(self,other): tick();return Number(int.__mul__(self,other))
    def __rmul__(self,other): tick();return Number(int.__mul__(self,other))
    def __add__(self,other): tick();return Number(int.__add__(self,other))
    def __radd__(self,other): tick();return Number(int.__add__(self,other))
spec=[(Number(1),Number((i%5)-2)) for i in range(240)]
ops[0]=0;limit[0]=4*len(spec)
try: service=make_service(spec)
except BudgetExceeded: raise AssertionError('Setup exceeds four arithmetic operations per adjustment.')
ops[0]=0;limit[0]=4*80
try:
    answers=[service(Number(x)) for x in range(80)]
except BudgetExceeded:
    raise AssertionError('Later readings repeat too much arithmetic: use no more than four operations per reading.')
assert answers==list(range(80)), "These fixed adjustments cancel; prepared readings must remain correct."

