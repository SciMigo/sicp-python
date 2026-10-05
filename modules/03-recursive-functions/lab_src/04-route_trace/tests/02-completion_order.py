from scimigo import _frame_count,_frame
expected=[]
def oracle(k):
    value=0 if k<0 else 1 if k==0 else oracle(k-1)+oracle(k-3)
    expected.append((k,value))
    return value
oracle(4)
before=_frame_count()
assert route_trace(4)==3,"There are 3 routes of length 4: 1+1+1+1, 1+3 and 3+1."
recorded=_frame_count()-before
assert recorded==11,f"route_trace(4) makes 11 calls, counting repeated and negative ones, and each draws one frame; recorded {recorded}."
for j,(n,value) in enumerate(expected):
    fig=next(o for o in _frame(before+j) if o['kind']=='figure')
    assert fig['params']['values']==[n,value],f"Frame {j+1} should complete remaining distance {n} with {value} routes; it shows {fig['params']['values']}. A call finishes after both of its children, and the n - 1 child goes first."
