def measure(solver,n,d,k):
    original=globals()["gcd"]
    calls=0
    def counted(a,b):
        nonlocal calls
        calls+=1
        return original(a,b)
    globals()["gcd"]=counted
    try:
        answer=solver(n,d,k)
        return answer,calls
    finally:
        globals()["gcd"]=original
from math import gcd
from scimigo import canvas,rectangle,text,frame

def normalize(n,d):
    g=gcd(n,d)
    return n//g,d//g

def eager(n,d,k):
    top,bottom=normalize(n,d)
    return [(top,bottom) for _ in range(k)]

def lazy(n,d,k):
    return [(normalize(n,d)[0],normalize(n,d)[1]) for _ in range(k)]

def show_counts(rows):
    canvas(600,370)
    largest=max([1]+[count for k,a,b in rows for count in (a,b)])
    for i,(k,a,b) in enumerate(rows):
        y=i*115
        text(12,y+20,"selections="+str(k),size=18)
        rectangle(145,y+25,400*a/largest,20,color="#276bb0")
        text(145,y+64,"eager="+str(a),size=17)
        rectangle(145,y+72,400*b/largest,20,color="#763aed")
        text(145,y+110,"lazy="+str(b),size=17)
    frame()

rows=[]
for k in (3,7,12):
    rows.append((k,measure(eager,21,35,k)[1],measure(lazy,21,35,k)[1]))
show_counts(rows)
