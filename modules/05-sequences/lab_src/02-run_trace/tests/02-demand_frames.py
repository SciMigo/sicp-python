from scimigo import _frame_count,_frame
before=_frame_count();answer=run_trace([2,3,5,6,9],2)
assert answer==[103,106],"The first two accepted source values are 3 and 6."
assert _frame_count()-before==len(events),"Record exactly one picture per logged event."
seen=[];made=[]
for i,(kind,value) in enumerate(events):
    if kind=='pull':seen.append(value)
    if kind=='output':made.append(value)
    objects=_frame(before+i);figs=[o for o in objects if o['kind']=='figure']
    expected=([list(seen)] if seen else [])+([list(made)] if made else [])
    assert [o['params']['values'] for o in figs]==expected,"Draw only source values actually pulled and outputs actually delivered so far."
    assert any(o['kind']=='text' and o['value']==kind+': '+str(value) for o in objects),"Name the event responsible for this frame."
