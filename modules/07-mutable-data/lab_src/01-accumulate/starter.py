def make_accumulator(initial):
    def add(value):
        show_state('accumulator not implemented',[initial])
        return initial
    return add

def make_monitored(f):
    return lambda value: 0

from scimigo import canvas,figure,text,frame

def show_state(label,values):
    canvas(600,260)
    text(15,35,label,size=19)
    figure('array_state',x=0,y=65,width=600,height=160,
           values=list(values) or ['empty'],indices=False,cell_width=110)
    frame()

a=make_accumulator(7)
b=make_accumulator(-2)
tracked=make_monitored(a)
for value in (4,-3,9):
    print(tracked(value))
print(tracked('how-many-calls?'))
tracked('reset-count')
print(tracked(2))
print(b(5))
