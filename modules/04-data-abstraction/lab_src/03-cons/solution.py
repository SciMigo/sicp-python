def cons(x,y):
    def dispatch(choose):
        return choose(x,y)
    return dispatch
from scimigo import canvas,figure,frame,text

def select_first(p):return p(lambda x,y:x)
def select_second(p):return p(lambda x,y:y)

def show_pair(p):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=220,
           values=[str(select_first(p)),str(select_second(p))],cell_width=100,indices=False)
    text(12,260,"first selector / second selector",size=18)
    frame()

p=cons("east","west")
show_pair(p)
