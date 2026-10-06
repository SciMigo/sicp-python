show_state=lambda *args:None
for n in (0,1,4,6,8):
    p=shared_stack(n)
    for strategy,want in [(naive,(2**n-1,2**n-1)),(distinct,(n,n))]:
        got=measure(strategy,p,pair_fields)
        assert got==want, f'{strategy.__name__} on {n} distinct pairs: expected {want}; got {got!r}'
seen=[]
def custom(p):seen.append(p);return 7,8
def unusual(root,fields):
    a=fields(root);b=fields(root);return a,b
p=[1,2];got=measure(unusual,p,custom)
assert got==(((7,8),(7,8)),2) and len(seen)==2 and all(x is p for x in seen), f'Expected two delegated calls and unchanged results; got {got!r}, calls {len(seen)}'
p=[None,None];p[0]=p
got=measure(distinct,p,pair_fields)
assert got==(1,1), f'One self-linked pair should expand once; got {got!r}'
def broken(p):raise ValueError('bad fields')
try:measure(unusual,p,broken)
except ValueError:pass
else:raise AssertionError('Expected field exception to propagate; got normal return')
got=measure(distinct,p,pair_fields)
assert got==(1,1), f'Fresh measurement after failure expected (1,1); got {got!r}'
