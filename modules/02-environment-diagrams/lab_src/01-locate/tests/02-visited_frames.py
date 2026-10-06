from scimigo import _frame_count,_frame
fs=[{"bindings":{"x":0},"parent":None},{"bindings":{},"parent":0},{"bindings":{},"parent":1}]
before=_frame_count()
assert locate(fs,2,"x")== (0,0)
assert _frame_count()-before==3,"Draw exactly one frame per visited scope."
for j,current in enumerate([2,1,0]):
    objects=_frame(before+j)
    fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['highlights']['frames']=={str(current):'current'},"Highlight the scope actually being probed."
    actual=fig['params']['frames']
    assert [f['parent'] for f in actual]==[None,'0','1'],"Draw the supplied parent links."
    assert actual[0]['bindings']==[{'name':'x','value':'0'}],"Preserve actual binding values."
