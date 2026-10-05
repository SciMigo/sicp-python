def packing_plans(n,sizes,modulus):
    counts=[1%modulus]+[0]*n
    for units in range(1,n+1):
        total=0
        for size in sizes:
            if size<=units:
                total=combine(total,counts[units-size],modulus)
        counts[units]=total
    return counts[n]
from scimigo import canvas,figure,frame,text

def combine(a,b,modulus):
    return (a+b)%modulus

def show_packing(n,result):
    canvas(600,280)
    figure("array_state",x=0,y=0,width=600,height=230,
           values=[n,result],indices=False)
    text(12,260,"Requested units / reported residue",size=18)
    frame()

show_packing(8,packing_plans(8,[1,4,6],97))
