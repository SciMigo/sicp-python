from scimigo import _frame_count,_frame
before=_frame_count()
assert power(2,3)==8,"power(2, 3) should be 8."
expected=[('enter',[3],3),('enter',[3,2],2),('enter',[3,2,1],1),('enter',[3,2,1,0],0),('leave',[3,2,1,0],1),('leave',[3,2,1],2),('leave',[3,2],4),('leave',[3],8)]
recorded=_frame_count()-before
assert recorded==len(expected),f"power(2, 3) makes 4 calls, each with an enter and a leave frame: 8 frames; recorded {recorded}."
for j,(stage,stack,value) in enumerate(expected):
    objects=_frame(before+j);fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==stack,f"Frame {j+1} should show the waiting exponents {stack}; it shows {fig['params']['values']}."
    assert any(o['kind']=='text' and o['value']==stage+': '+str(value) for o in objects),f"Frame {j+1} should read '{stage}: {value}'."
