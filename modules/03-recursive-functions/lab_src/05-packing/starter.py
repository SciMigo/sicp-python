def packing_plans(n,sizes,modulus):
    def solve(k):
        if k==0:return 1%modulus
        total=0
        for size in sizes:
            if size<=k:
                total=combine(total,solve(k-size),modulus)
        return total
    return solve(n)
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
