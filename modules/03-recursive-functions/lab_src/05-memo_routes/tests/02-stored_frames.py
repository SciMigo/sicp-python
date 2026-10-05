from scimigo import _frame_count,_frame
before=_frame_count();assert memo_routes(4)==3
assert _frame_count()-before==4,"A stored answer must not be drawn as a new computation twice."
for j,value in enumerate([1,1,2,3]):
    fig=next(o for o in _frame(before+j) if o['kind']=='figure')
    assert fig['params']['values']==[j+1,value]
