def chain(f,g):
    def run(x):
        middle=g(x)
        show_stage("g", x, middle)
        result=f(middle)
        show_stage("f", middle, result)
        return result
    return run
from scimigo import canvas, figure, frame, text

def show_stage(name, value, result):
    canvas(600, 360)
    figure("array_state", x=0, y=0, width=600, height=290,
           values=[value,result], indices=False)
    text(15, 335, name+": "+str(value)+" -> "+str(result), size=18)
    frame()
h=chain(lambda x:x-4, lambda x:3*x)
print(h(2))
