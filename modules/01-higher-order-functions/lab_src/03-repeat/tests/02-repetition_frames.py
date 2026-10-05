from scimigo import _frame_count, _frame
before=_frame_count()
assert repeat(lambda x:x-3,4)(20)==8
assert _frame_count()-before==4, "For a small demo, record one frame after each application."
for i,value in enumerate([17,14,11,8]):
    objects=_frame(before+i)
    fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==[value], "Draw the actual intermediate result."

