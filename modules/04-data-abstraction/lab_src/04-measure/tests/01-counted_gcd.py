original=gcd
for k in (0,1,4,9):
    expected=[(3,5)]*k
    assert measure(eager,21,35,k)==(expected,1),"Eager construction performs one gcd even if nothing is later selected."
    assert measure(lazy,21,35,k)==(expected,2*k),"Each lazy pair selection computes two gcd calls."
    assert gcd is original,"Restore the original gcd after measuring."
def unusual(n,d,k):
    for _ in range(5):gcd(n,d)
    return 'done'
assert measure(unusual,12,18,3)==('done',5),"Measure actual operations; do not infer a count from k or the solver name."
def broken(n,d,k):
    gcd(n,d)
    raise ValueError('expected')
raised=False
try:measure(broken,4,6,2)
except ValueError:raised=True
assert raised and gcd is original,"Propagate the solver error and still restore gcd."
