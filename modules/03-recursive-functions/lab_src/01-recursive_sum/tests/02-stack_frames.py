from scimigo import _frame_count,_frame
before=_frame_count();assert recursive_sum(3)==6
expected=[('enter',[3],3),('enter',[3,2],2),('enter',[3,2,1],1),('enter',[3,2,1,0],0),('leave',[3,2,1,0],0),('leave',[3,2,1],1),('leave',[3,2],3),('leave',[3],6)]
assert _frame_count()-before==len(expected)
for j,(stage,stack,value) in enumerate(expected):
    objects=_frame(before+j);fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==stack,"Draw the actual active argument stack."
    assert any(o['kind']=='text' and o['value']==stage+': '+str(value) for o in objects),"Draw the value at this entry or return."
