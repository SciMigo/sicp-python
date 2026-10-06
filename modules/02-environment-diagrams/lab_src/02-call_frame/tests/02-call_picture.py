from scimigo import _frame_count,_frame
before=_frame_count();a=call_frame({'params':['reading'],'parent':4},9,[7])
assert _frame_count()-before==1
fig=next(o for o in _frame(before) if o['kind']=='figure')
f=fig['params']['frames']
assert f[0]['label']=='Definition environment 4',"The diagram must name the defining environment."
assert f[1]['parent']=='owner' and f[1]['bindings']==[{'name':'reading','value':'7'}]
