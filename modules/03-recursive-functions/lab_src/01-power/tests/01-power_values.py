saved_show=show_stack;show_stack=lambda *a:None
original=power
seen=[]
def watched(base,n,stack=None):
    seen.append(n)
    return original(base,n,stack)
power=watched
try:
    for base,n in [(2,0),(5,1),(3,2),(-2,5),(1,11),(2,17),(0,3)]:
        seen.clear();stack=[99]
        result=power(base,n,stack)
        assert result==base**n,f"power({base}, {n}) should be {base**n}; got {result}. Multiply base by the answer for n - 1."
        assert seen==list(range(n,-1,-1)),f"power({base}, {n}) should call power once for each exponent from {n} down to 0; the calls had n = {seen}."
        assert stack==[99],f"The caller's stack was [99] before the call and {stack} after it: pop what you append."
    assert power(7,4)==2401,"With no stack supplied, start a fresh one."
    assert power(7,4)==2401,"A second call must not see state left by the first."
finally:
    power=original;show_stack=saved_show
