from scimigo import _frame_count,_frame
before=_frame_count();show_badges(prepare_badges([6,-1,6]),4)
assert _frame_count()-before==1
fig=next(o for o in _frame(before) if o['kind']=='figure')
assert fig['params']['values']==[6,-1,6],"Draw the callbacks' results, preserving order and duplicates."
