from scimigo import _frame_count,_frame
change,read,reset=make_box(7);before=_frame_count()
assert [change(4),change(-2),read(),reset(),read()]==[11,9,9,7,7]
assert _frame_count()-before==5
for j,(operation,total) in enumerate([('change',11),('change',9),('read',9),('reset',7),('read',7)]):
    objects=_frame(before+j);fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['frames'][0]['bindings']==[{'name':'start','value':'7'},{'name':'total','value':str(total)}]
    assert any(o['kind']=='text' and o['value']==operation+': total='+str(total) for o in objects)
