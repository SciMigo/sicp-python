from scimigo import _frame_count, _frame
before = _frame_count()
assert totals(sample) == 15, "This hierarchy has a label sum of 15."
expected=[((0,),0),((1,0),5),((1,1),5),((1,),11),((2,),-2),((),15)]
assert _frame_count()-before == len(expected), "Record one completion frame for each node."
for offset,(path,value) in enumerate(expected):
    objects=_frame(before+offset)
    f=[o for o in objects if o['kind']=='figure'][0]
    assert f['type']=='tree', "Draw the hierarchy in each completion frame."
    node=sample
    for i in path: node=branches(node)[i]
    name='root' if not path else '.'.join(map(str,path))
    assert f['params']['highlights']=={name+':'+str(label(node)):'current'}, "Highlight the completed node, using its position."
    assert any(o['kind']=='text' and o['value']=='Completed '+name+': '+str(value) for o in objects), "Show the true label sum for this completed subtree."

