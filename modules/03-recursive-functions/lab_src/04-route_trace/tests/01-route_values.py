saved=show_route;show_route=lambda *a:None
try:
    expected=[1,1,1,2,3,4,6,9,13,19]
    for n,value in enumerate(expected):
        got=route_trace(n)
        why="A remaining distance of 0 is one finished route." if n==0 else "A route ends with a 1-jump or a 3-jump, so add both smaller counts."
        assert got==value,f"route_trace({n}) should be {value}; got {got}. {why}"
    assert route_trace(-1)==0 and route_trace(-2)==0,"A negative remaining distance has no routes."
finally:show_route=saved
