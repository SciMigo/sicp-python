saved=show_route;show_route=lambda *a:None
expected=[1,1,1,2,3,4,6,9,13,19]
for n,value in enumerate(expected):assert route_trace(n)==value,"Include both possible final jumps."
assert route_trace(-1)==route_trace(-2)==0
show_route=saved
