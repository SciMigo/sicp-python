def repeat(f,n):
    def run(x):
        value=x
        for i in range(n):
            value=f(value)
            if n<=12: show_step(i+1,value)
        if n==0: show_step(0,value)
        return value
    return run
from scimigo import canvas, figure, frame, text

def show_step(step,value):
    canvas(600, 320)
    figure("array_state", x=0, y=0, width=600, height=250, values=[value], indices=False)
    text(15, 295, "After "+str(step)+" applications: "+str(value), size=18)
    frame()
print(repeat(lambda x:x+2,5)(3))
