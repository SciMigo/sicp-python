def horner(x,coefficients):
    result=0
    show_horner(-1,0,result)
    return result
from scimigo import canvas,figure,frame,text

def show_horner(index,coefficient,result):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=220,
           values=[index,coefficient,result],indices=False)
    text(12,260,"index / coefficient / completed suffix value",size=17)
    frame()

print(horner(3,[2,-1,3,0,1]))
