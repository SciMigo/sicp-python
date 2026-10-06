from scimigo import _frame_count,_frame
coefficients=[4,0,-2,1];x=2;before=_frame_count();answer=horner(x,coefficients)
assert answer==4,"Compute all powers in the demo polynomial, including the zero coefficient."
assert _frame_count()-before==len(coefficients),"Record one suffix-combination step per coefficient."
result=0
for offset,index in enumerate(range(len(coefficients)-1,-1,-1)):
    result=coefficients[index]+x*result
    fig=next(o for o in _frame(before+offset) if o['kind']=='figure')
    assert fig['params']['values']==[index,coefficients[index],result],"Each frame must show this coefficient combined with the already completed higher terms."
