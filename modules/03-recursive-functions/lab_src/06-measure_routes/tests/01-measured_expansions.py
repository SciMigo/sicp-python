original=transition
for n in [0,1,4,7,11]:
    def expansions(k):return 0 if k<=0 else 1+expansions(k-1)+expansions(k-3)
    table=[1]+[0]*n
    for k in range(1,n+1):table[k]=table[k-1]+(table[k-3] if k>=3 else 0)
    assert measure(naive_routes,n)==(table[n],expansions(n))
    assert transition is original,"Restore the original helper after measuring."
    assert measure(cached_routes,n)==(table[n],n)
def odd_solver(n):
    for _ in range(n+2):transition(1)
    return 77
assert measure(odd_solver,3)==(77,5),"Report actual events, not a guessed formula in n."
def raises(n):
    transition(1)
    raise ValueError('deliberate')
try:measure(raises,1)
except ValueError:pass
else:raise AssertionError('Propagate solver errors.')
assert transition is original,"Restore instrumentation even after an error."
