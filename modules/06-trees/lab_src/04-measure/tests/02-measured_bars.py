from scimigo import _frame_count, _frame
before=_frame_count()
rows=[(n,profile(make_star(n))) for n in (9,27,81)]
show_measure(rows)
objects=_frame(before)
for n,c in rows:
    assert any(o['kind']=='text' and ('n='+str(n))==o['value'] for o in objects), "Label each measured input size."
    assert any(o['kind']=='text' and o['value'].startswith('reads='+str(c)+',') for o in objects), "Draw your actual measured count."
assert len([o for o in objects if o['kind']=='rectangle'])==3, "Draw a bar for each measured row."

