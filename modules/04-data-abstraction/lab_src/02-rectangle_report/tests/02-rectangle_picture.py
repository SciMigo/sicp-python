from scimigo import _frame_count,_frame
before=_frame_count();result=rectangle_report(rectangle(9,2))
assert result==(18,22),"Return area and perimeter in that order."
assert _frame_count()-before==1,"Draw one completed rectangle report."
fig=next(o for o in _frame(before) if o['kind']=='figure')
assert fig['params']['values']==[9,2,18,22],"Draw the actual selected dimensions and computed answers."
