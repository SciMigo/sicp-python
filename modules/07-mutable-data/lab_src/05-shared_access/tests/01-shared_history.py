show_state=lambda *args:None
for initial in (0,23,80):
    account=supplied_account(initial,'a')
    program=[('join','g','owner','a','b'),('use','g','b','deposit',9),('use','owner','a','withdraw',3),('join','h','g','b','c'),('use','h','c','withdraw',2),('join','bad','g','no','d'),('use','g','wrong','deposit',99),('use','owner','a','withdraw',0)]
    want=['Joined',initial+9,initial+6,'Joined',initial+4,'Incorrect password','Incorrect password',initial+4]
    got=run_access(account,program)
    assert got==want, f'Expected one shared history {want}; got {got!r}'
a=supplied_account(30,'a');g=connect(a,'a','b');h=connect(g,'b','c');saved=h('c','withdraw')
a('a','deposit')(8);got=saved(4)
assert got==34, f'Saved operation through nested access should see 34; got {got!r}'
assert g('a','check') is False and g('b','check') is True, f'New route should accept only b; got old={g("a","check")!r}, new={g("b","check")!r}'
requests=[]
def spy(pw,request):
    requests.append((pw,request))
    if request=='check':return pw=='ok'
    raise AssertionError(f'Join should only query check; got {request!r}')
connect(spy,'ok','next')
assert requests==[('ok','check')], f'Expected one authorization query; got {requests}'
try:connect(spy,'bad','next')
except ValueError:pass
else:raise AssertionError('Expected invalid join to raise ValueError; got normal return')
