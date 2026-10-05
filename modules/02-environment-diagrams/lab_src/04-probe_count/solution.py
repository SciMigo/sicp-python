def measured_lookup(frames,current,name):
    probes=0
    while current is not None:
        bindings=frames[current]["bindings"]
        probes+=1
        if name in bindings:return bindings[name],probes
        current=frames[current]["parent"]
    return None,probes
from scimigo import canvas,rectangle,text,frame

def show_probes(rows):
    canvas(600,300)
    largest=max(c for d,c in rows) or 1
    for i,(depth,calls) in enumerate(rows):
        rectangle(120,25+75*i,430*calls/largest,35,color="#276bb0")
        text(12,48+75*i,"depth="+str(depth),size=17)
        text(125,85+75*i,"probes="+str(calls),size=17)
    frame()

rows=[]
for depth in [2,5,9]:
    frames=[{"bindings":{},"parent":i-1 if i else None} for i in range(depth)]
    frames[0]["bindings"]["key"]=42
    rows.append((depth,measured_lookup(frames,depth-1,"key")[1]))
show_probes(rows)
