from scimigo import _frame_count,_frame
before=_frame_count();assert mirrored([4,7,2,7,4]) is True
expected=[(0,4,'enter',None),(1,3,'enter',None),(2,2,'enter',None),(2,2,'leave',True),(1,3,'leave',True),(0,4,'leave',True)]
assert _frame_count()-before==len(expected),"Record entry and return for every window."
for j,(left,right,stage,answer) in enumerate(expected):
    objects=_frame(before+j)
    fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==[4,7,2,7,4]
    assert fig['params']['highlights']=={str(i):'current' for i in range(left,right+1)}
    assert [p['index'] for p in fig['params']['pointers']]==[left,right]
    words=[o['value'] for o in objects if o['kind']=='text']
    assert 'left='+str(left)+'  right='+str(right)+'  '+stage in words
    assert 'answer='+str(answer) in words
