from scimigo import _frame_count,_frame
before=_frame_count()
assert memo_routes(4)==3,"memo_routes(4) should be 3."
recorded=_frame_count()-before
assert recorded==4,f"memo_routes(4) has four positive states, each recorded once when first computed: 4 frames; recorded {recorded}."
for j,value in enumerate([1,1,2,3]):
    fig=next(o for o in _frame(before+j) if o['kind']=='figure')
    assert fig['params']['values']==[j+1,value],f"Frame {j+1} should store state {j+1} with {value} routes; it shows {fig['params']['values']}."
