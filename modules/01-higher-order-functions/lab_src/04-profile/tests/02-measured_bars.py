from scimigo import _frame_count, _frame
before=_frame_count()
rows=[(n,profile(lambda x:x+1,n,0)[1]) for n in [8,24,72]]
show_measure(rows)
objects=_frame(before)
assert len([o for o in objects if o['kind']=='rectangle'])==3, "Draw three measured bars."
for n,c in rows:
    assert any(o['kind']=='text' and o['value']==f'n={n}' for o in objects)
    assert any(o['kind']=='text' and o['value'].startswith(f'calls={c},') for o in objects), "Draw your measured callback counts."

