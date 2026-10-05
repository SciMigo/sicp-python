def memo_routes(n):
    cache={0:1}
    def solve(k):
        if k<0:return 0
        if k not in cache:
            left,right=transition(k)
            cache[k]=solve(left)+solve(right)
            record_state(k,cache[k])
        return cache[k]
    return solve(n)
from scimigo import canvas,figure,frame,text

def transition(k):
    return k-1,k-3

def record_state(k,value):
    canvas(600,280)
    figure("array_state",x=0,y=0,width=600,height=230,
           values=[k,value],indices=False)
    text(12,260,"Stored state "+str(k)+": "+str(value),size=18)
    frame()

print(memo_routes(4))
