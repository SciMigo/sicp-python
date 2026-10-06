saved=show_pair;show_pair=lambda *args:None
try:
    for x,y in [(4,9),(None,False),(0,''),([],{}),('left','right')]:
        p=cons(x,y)
        assert callable(p),"Return a function representing the pair."
        assert select_first(p) is x and select_second(p) is y,"Selectors must return the original objects, preserving identity."
        calls=[]
        def choose(a,b):calls.append((a,b));return 'chosen'
        assert p(choose)=='chosen',"Apply the chooser and return its result."
        assert len(calls)==1 and calls[0][0] is x and calls[0][1] is y,"Call the chooser once with this pair's two original parts."
    a,b=cons(3,5),cons(7,11)
    assert (select_first(a),select_second(b),select_second(a))==(3,11,5),"Different pair creators keep separate captured bindings."
finally:show_pair=saved
