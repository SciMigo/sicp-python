show_links=lambda *args:None
for xs,ys in [([],[]),([],['q']),(['q'],[]),(['q'],['q','r']),(['a','b','c'],['d'])]:
    a=chain(xs);b=chain(ys);old=[];p=a
    while p is not None:old.append(p);p=p[1]
    oldb=[];p=b
    while p is not None:oldb.append(p);p=p[1]
    got=append_in_place(a,b);want=old+oldb;seen=[];p=got
    for _ in range(len(want)+1):
        if p is None:break
        seen.append(p);p=p[1]
    assert len(seen)==len(want) and all(x is y for x,y in zip(seen,want)) and p is None, f'Expected original {len(want)} pair identities in order with null tail; got {len(seen)} encounters, terminal {p!r}'
    values=[p[0] for p in seen]
    assert values==xs+ys, f'Expected values {xs+ys}; got {values}'
