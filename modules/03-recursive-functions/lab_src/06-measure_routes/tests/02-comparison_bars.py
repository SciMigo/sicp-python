from scimigo import _frame_count,_frame
rows=[(n,measure(naive_routes,n)[1],measure(cached_routes,n)[1]) for n in [6,10,14]]
want=[(6,12,6),(10,59,10),(14,276,14)]
assert rows==want,f"For n = 6, 10, 14 the measured (n, naive, cached) rows should be {want}; got {rows}."
before=_frame_count();show_expansions(rows)
objects=_frame(before)
bars=len([o for o in objects if o['kind']=='rectangle'])
assert bars==6,f"Draw one naive bar and one cached bar per size: 6 bars; found {bars}."
for n,a,b in rows:
    for label in ['n='+str(n),'naive='+str(a),'cached='+str(b)]:
        assert any(o['kind']=='text' and o['value']==label for o in objects),f"The chart should carry the label '{label}'."
