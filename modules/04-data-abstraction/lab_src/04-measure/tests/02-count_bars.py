from scimigo import _frame_count,_frame
rows=[(k,measure(eager,21,35,k)[1],measure(lazy,21,35,k)[1]) for k in (3,7,12)]
assert rows==[(3,1,6),(7,1,14),(12,1,24)],"Measure both strategies before drawing."
before=_frame_count();show_counts(rows)
assert _frame_count()-before==1,"Draw one comparison frame."
objects=_frame(before)
assert sum(o['kind']=='rectangle' for o in objects)==6,"Draw two measured bars for each selection count."
words=[o['value'] for o in objects if o['kind']=='text']
for k,a,b in rows:
    assert 'selections='+str(k) in words and 'eager='+str(a) in words and 'lazy='+str(b) in words,"Label bars with the actual counted values."
