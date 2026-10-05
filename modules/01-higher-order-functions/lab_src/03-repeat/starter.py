def repeat(f,n):
    def run(x):
        value=f(x)  # currently applies f once, even when n is zero
        show_step(1,value)
        return value
    return run
from scimigo import canvas, figure, frame, text

def show_step(step,value):
    canvas(600, 320)
    figure("array_state", x=0, y=0, width=600, height=250, values=[value], indices=False)
    text(15, 295, "After "+str(step)+" applications: "+str(value), size=18)
    frame()
print(repeat(lambda x:x+2,5)(3))
