from scimigo import _frame_count, _frame
before=_frame_count()
assert chain(lambda x:x-4,lambda x:3*x)(2)==2
assert _frame_count()-before==2, "Record two actual callback stages."
for i,(name,a,b) in enumerate([('g',2,6),('f',6,2)]):
    objects=_frame(before+i)
    fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==[a,b], "The two cells must show this stage's input and output."
    assert any(o['kind']=='text' and o['value']==f'{name}: {a} -> {b}' for o in objects), "Label the callback that actually ran."

