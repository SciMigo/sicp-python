from scimigo import _frame_count,_frame
before=_frame_count()
assert mirrored([4,7,2,7,4]) is True,"[4, 7, 2, 7, 4] is mirrored."
expected=[(0,4,'enter',None),(1,3,'enter',None),(2,2,'enter',None),(2,2,'leave',True),(1,3,'leave',True),(0,4,'leave',True)]
recorded=_frame_count()-before
assert recorded==len(expected),f"Three windows are visited, each with an enter and a leave frame: 6 frames; recorded {recorded}."
for j,(left,right,stage,answer) in enumerate(expected):
    objects=_frame(before+j)
    fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==[4,7,2,7,4],f"Frame {j+1}: draw the original list in every frame."
    assert [p['index'] for p in fig['params']['pointers']]==[left,right],f"Frame {j+1} should be the {stage} frame of window {left}..{right}."
    assert fig['params']['highlights']=={str(i):'current' for i in range(left,right+1)},f"Frame {j+1}: highlight exactly positions {left} to {right}."
    words=[o['value'] for o in objects if o['kind']=='text']
    assert 'left='+str(left)+'  right='+str(right)+'  '+stage in words,f"Frame {j+1} should be labelled left={left} right={right} {stage}."
    assert 'answer='+str(answer) in words,f"Frame {j+1} should show answer={answer}."
before=_frame_count()
assert mirrored([1,2,3,1]) is False,"[1, 2, 3, 1] is not mirrored: the inside pair differs."
recorded=_frame_count()-before
assert recorded==4,f"[1, 2, 3, 1] visits two windows and stops at the mismatch: 4 frames; recorded {recorded}."
