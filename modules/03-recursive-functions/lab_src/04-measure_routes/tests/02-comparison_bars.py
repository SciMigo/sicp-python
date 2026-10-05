from scimigo import _frame_count,_frame
rows=[(n,measure(naive_routes,n)[1],measure(cached_routes,n)[1]) for n in [5,9,13]]
assert rows==[(5,8,5),(9,40,9),(13,188,13)]
before=_frame_count();show_expansions(rows)
objects=_frame(before)
assert len([o for o in objects if o['kind']=='rectangle'])==6
for n,a,b in rows:
    for label in ['n='+str(n),'naive='+str(a),'cached='+str(b)]:
        assert any(o['kind']=='text' and o['value']==label for o in objects),"Draw the measured values, not expected constants."
