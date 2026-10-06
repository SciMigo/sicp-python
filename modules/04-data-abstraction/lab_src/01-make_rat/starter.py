def make_rat(n,d):
    result=(0,1)
    show_rat(n,d,result)
    return result
from math import gcd
from scimigo import canvas,figure,frame,text

def numer(r):return r[0]
def denom(r):return r[1]

def show_rat(n,d,result):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=220,
           values=[n,d,numer(result),denom(result)],indices=False)
    text(12,260,"input numerator / denominator → selected numerator / denominator",size=15)
    frame()

print(make_rat(-8,-12))
