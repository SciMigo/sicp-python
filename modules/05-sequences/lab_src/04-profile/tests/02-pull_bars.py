from scimigo import _frame_count,_frame
rows=[(n,profile(eager,list(range(1,n+1)),3)[1],profile(lazy,list(range(1,n+1)),3)[1]) for n in (16,40,80)]
assert rows==[(16,16,12),(40,40,12),(80,80,12)],"Measure how far each solver reads to find its requested prefix."
before=_frame_count();show_pulls(rows)
assert _frame_count()-before==1,"Draw one comparison picture."
objects=_frame(before);bars=[o for o in objects if o['kind']=='rectangle'];words=[o['value'] for o in objects if o['kind']=='text']
assert len(bars)==6,"Draw one eager and one lazy bar per size."
for n,a,b in rows:
    assert 'input size='+str(n) in words and 'eager pulls='+str(a) in words and 'lazy pulls='+str(b) in words,"Use the actual measured counts as labels."
