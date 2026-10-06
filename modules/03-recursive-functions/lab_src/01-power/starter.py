def power(base, n, stack=None):
    if stack is None:
        stack = []
    stack.append(n)
    show_stack("enter", stack, n)
    # Your code goes here.
    return 1
from scimigo import canvas,figure,frame,text

def show_stack(stage,stack,result):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=240,
           values=list(stack),indices=False)
    text(12,275,stage+": "+str(result),size=18)
    frame()

print(power(2,3))
