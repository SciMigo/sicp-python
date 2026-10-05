from scimigo import _frame_count,_frame
before=_frame_count()
assert nested_total([3,[2,[],[5]],1])==11,"[3, [2, [], [5]], 1] totals 11."
expected=[((0,),3,3),((1,0),2,2),((1,1),[],0),((1,2,0),5,5),((1,2),[5],5),((1,),[2,[],[5]],7),((2,),1,1),((),[3,[2,[],[5]],1],11)]
recorded=_frame_count()-before
assert recorded==len(expected),f"This input has 8 nodes (4 integers and 4 lists, one of them empty): 8 frames; recorded {recorded}."
for j,(path,node,answer) in enumerate(expected):
    objects=_frame(before+j);fig=next(o for o in objects if o['kind']=='figure')
    assert any(o['kind']=='text' and o['value']=='completed path='+str(path) for o in objects),f"Frame {j+1} should complete the node at path {path}: children finish before their parent, left to right."
    assert fig['params']['values']==['integer' if isinstance(node,int) else 'list',answer],f"Frame {j+1}: the node at path {path} has total {answer}."
