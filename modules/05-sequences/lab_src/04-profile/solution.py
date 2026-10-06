def profile(solver,items,k):
    original=globals()["source"]
    pulls=0
    def counted(values):
        nonlocal pulls
        for item in original(values):
            pulls+=1
            yield item
    globals()["source"]=counted
    try:
        answer=solver(items,k)
        return answer,pulls
    finally:
        globals()["source"]=original
from itertools import islice
from scimigo import canvas,rectangle,text,frame

def source(items):
    yield from items

def eager(items,k):
    values=[x+10 for x in source(items) if x%4==0]
    return values[:k]

def lazy(items,k):
    return list(islice((x+10 for x in source(items) if x%4==0),k))

def show_pulls(rows):
    canvas(600,370)
    largest=max([1]+[count for n,a,b in rows for count in (a,b)])
    for i,(n,a,b) in enumerate(rows):
        y=i*115
        text(12,y+20,"input size="+str(n),size=18)
        rectangle(145,y+25,400*a/largest,20,color="#276bb0")
        text(145,y+64,"eager pulls="+str(a),size=17)
        rectangle(145,y+72,400*b/largest,20,color="#763aed")
        text(145,y+110,"lazy pulls="+str(b),size=17)
    frame()

rows=[]
for n in (16,40,80):
    items=list(range(1,n+1))
    rows.append((n,profile(eager,items,3)[1],profile(lazy,items,3)[1]))
show_pulls(rows)
