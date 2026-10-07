show_links=lambda *args:None
def walk(head,limit):
    seen=[]
    while head is not None and len(seen)<=limit:
        seen.append(head);head=head[1]
    return seen
for xs,ys in [([],[]),([],['q']),(['q'],[]),(['q'],['q','r']),(['a','b','c'],['d']),(['m','m'],['m'])]:
    a=chain(xs);b=chain(ys)
    want=walk(a,len(xs))+walk(b,len(ys))
    got=append_in_place(a,b)
    seen=walk(got,len(want))
    assert len(seen)==len(want), f'append_in_place({xs}, {ys}) should give a chain of {len(want)} pairs ending in None; yours has {"more than " if len(seen)>len(want) else ""}{min(len(seen),len(want)+1)}'
    assert all(x is y for x,y in zip(seen,want)), f'append_in_place({xs}, {ys}) must reuse the original pairs in order; it built or reordered pairs'
    values=[p[0] for p in seen]
    assert values==xs+ys, f'append_in_place({xs}, {ys}) should read {xs+ys}; it reads {values}'
    if xs:
        assert got is a, f'append_in_place({xs}, {ys}) should return the first chain itself'
