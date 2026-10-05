def recursive_sum(n,stack=None):
    if stack is None:stack=[]
    stack.append(n)
    show_stack("enter",stack,n)
    result=n  # include the smaller recursive answer
    show_stack("leave",stack,result)
    stack.pop()
    return result
from scimigo import canvas,figure,frame,text

def show_stack(stage,stack,result):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=240,
           values=list(stack),indices=False)
    text(12,275,stage+": "+str(result),size=18)
    frame()

print(recursive_sum(3))
