from scimigo import _frame_count, _frame
before=_frame_count()
values=[4,-1,3]
assert total_terms(values,lambda v:v*v)==26, "The final square total must include all three inputs."
assert _frame_count()-before==3, "Record one frame after each processed input."
for i,total in enumerate([16,17,26]):
    objects=_frame(before+i)
    fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==values, "Draw the actual input values."
    assert fig['params']['brackets']==[{'from':0,'to':i,'label':'processed'}], "The bracket must cover exactly the processed prefix."
    assert any(o['kind']=='text' and o['value']==f'Processed={i+1}, total={total}' for o in objects), "Show the true total for this prefix."

