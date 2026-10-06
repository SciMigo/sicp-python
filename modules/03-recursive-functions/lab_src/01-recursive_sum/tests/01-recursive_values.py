saved_show=show_stack;show_stack=lambda *a:None
original=recursive_sum
seen=[]
def watched(n,stack=None):
    seen.append(n)
    return original(n,stack)
recursive_sum=watched
for n in [0,1,2,6,11,17]:
    seen.clear();stack=[99]
    result=recursive_sum(n,stack)
    assert result==n*(n+1)//2,"Add the completed smaller sum."
    assert seen==list(range(n,-1,-1)),"Call the same function once per decreasing argument, including zero."
    assert stack==[99],"Restore the caller's supplied stack."
recursive_sum=original;show_stack=saved_show
