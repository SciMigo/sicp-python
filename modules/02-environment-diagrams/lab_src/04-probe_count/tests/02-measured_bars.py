from scimigo import _frame_count,_frame
rows=[]
for depth in [2,5,9]:
    fs=[{'bindings':{},'parent':i-1 if i else None} for i in range(depth)]
    fs[0]['bindings']['key']=42
    rows.append((depth,measured_lookup(fs,depth-1,'key')[1]))
before=_frame_count();show_probes(rows)
objects=_frame(before);bars=[o for o in objects if o['kind']=='rectangle']
assert rows==[(2,2),(5,5),(9,9)]
assert len(bars)==3
for bar,(_,count) in zip(bars,rows):assert abs(bar['width']-430*count/9)<1e-8
for count in [2,5,9]:assert any(o['kind']=='text' and o['value']=='probes='+str(count) for o in objects)
