show_measure=lambda *args: None
for n in [0,7,23,67,211]:
    calls=[]
    f=lambda v:calls.append(v) or (v+3)
    result,reported=profile(f,n,-2)
    assert result==-2+3*n, "Return the actual final value."
    assert reported==len(calls)==n, "Reported counts must match actual supplied callback calls on fresh sizes."
# The meter must still observe a deliberately wasteful run_steps.
def wasteful(f,n,x):
    for _ in range(n):
        f(x)
        x=f(x)
    return x
run_steps=wasteful
calls=[]
result,reported=profile(lambda v:calls.append(v) or (v+1),9,0)
assert result==9 and reported==len(calls)==18, "Instrument real calls, including wasted calls; do not return n as the count."

