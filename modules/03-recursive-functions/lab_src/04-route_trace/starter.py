def route_trace(n):
    result=0
    # Your code goes here: work out this call's result.
    show_route(n,result)
    return result
from scimigo import canvas,figure,frame,text

def show_route(n,result):
    canvas(600,280)
    figure("array_state",x=0,y=0,width=600,height=230,
           values=[n,result],indices=False)
    text(12,260,"Completed remaining="+str(n)+", ways="+str(result),size=18)
    frame()

print(route_trace(4))
