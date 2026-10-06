from scimigo import _frame_count,_frame
before=_frame_count();result=make_rat(15,-25)
assert result==(-3,5),"Normalize the demo ratio before drawing."
assert _frame_count()-before==1,"Record one completed construction."
fig=next(o for o in _frame(before) if o['kind']=='figure')
assert fig['params']['values']==[15,-25,numer(result),denom(result)],"Draw input parts and this returned fraction's selected parts."
