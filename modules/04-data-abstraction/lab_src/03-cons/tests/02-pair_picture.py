from scimigo import _frame_count,_frame
p=cons('near','far');before=_frame_count();show_pair(p)
assert _frame_count()-before==1,"Draw one selector observation."
fig=next(o for o in _frame(before) if o['kind']=='figure')
assert fig['params']['values']==['near','far'],"The picture must show the values recovered from this pair."
