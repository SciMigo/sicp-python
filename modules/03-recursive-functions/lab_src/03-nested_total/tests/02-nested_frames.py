from scimigo import _frame_count,_frame
before=_frame_count();assert nested_total([3,[2,[],[5]],1])==11
expected=[((0,),3,3),((1,0),2,2),((1,1),[],0),((1,2,0),5,5),((1,2),[5],5),((1,),[2,[],[5]],7),((2,),1,1),((),[3,[2,[],[5]],1],11)]
assert _frame_count()-before==len(expected),"Draw every leaf and container, including empty containers."
for j,(path,node,answer) in enumerate(expected):
    objects=_frame(before+j);fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==['integer' if isinstance(node,int) else 'list',answer],"Draw this node and its own completed answer."
    assert any(o['kind']=='text' and o['value']=='completed path='+str(path) for o in objects)
