original=transition
for n in [0,1,4,7,11]:
    def expansions(k):return 0 if k<=0 else 1+expansions(k-1)+expansions(k-3)
    table=[1]+[0]*n
    for k in range(1,n+1):table[k]=table[k-1]+(table[k-3] if k>=3 else 0)
    got=measure(naive_routes,n)
    assert got==(table[n],expansions(n)),f"measure(naive_routes, {n}) should be ({table[n]}, {expansions(n)}): the answer and the number of transition calls; got {got}."
    assert transition is original,"Put the original transition back after measuring."
    got=measure(cached_routes,n)
    assert got==(table[n],n),f"measure(cached_routes, {n}) should be ({table[n]}, {n}); got {got}. Each measurement starts its count from zero."
def odd_solver(n):
    for _ in range(n+2):transition(1)
    return 77
got=measure(odd_solver,3)
assert got==(77,5),f"A solver that calls transition 5 times and returns 77 should measure as (77, 5); got {got}. Count the calls that happen; do not compute them from n."
def raises(n):
    transition(1)
    raise ValueError('deliberate')
try:measure(raises,1)
except ValueError:pass
else:raise AssertionError("When the solver raises, measure should let the error through.")
assert transition is original,"Put the original transition back even when the solver raises."
