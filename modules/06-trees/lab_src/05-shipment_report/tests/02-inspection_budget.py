show=lambda *args: None
original_branches=branches
reads=[0]
class BudgetExceeded(BaseException): pass
def metered(node):
    reads[0]+=1
    if reads[0]>6*127: raise BudgetExceeded()
    return original_branches(node)
t=tree(2)
for _ in range(126): t=tree(99,[t])
branches=metered
try:
    result=charges(t)
except BudgetExceeded:
    raise AssertionError("Too many record inspections: avoid recomputing a completed descendant's charge.")
assert len(result)==127 and all(v==2 for v in result.values()), "Every enclosing position must include the terminal fee."
assert reads[0]<=6*127, "Stay within six child-list inspections per record."

