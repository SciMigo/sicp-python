from scimigo import _frame_count,_frame
expected=[]
def oracle(k):
    value=0 if k<0 else 1 if k==0 else oracle(k-1)+oracle(k-3)
    expected.append((k,value))
    return value
assert oracle(4)==3 and len(expected)==11
before=_frame_count();assert route_trace(4)==3
assert _frame_count()-before==11,"Include all eleven call occurrences, even repeated base calls."
for j,(n,value) in enumerate(expected):
    fig=next(o for o in _frame(before+j) if o['kind']=='figure')
    assert fig['params']['values']==[n,value],"Record each actual completed remainder and answer in postorder."
