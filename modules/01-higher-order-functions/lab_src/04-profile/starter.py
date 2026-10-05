def profile(f,n,x):
    return x,0  # run the process and count its actual callback calls
from scimigo import canvas, rectangle, text, frame

def run_steps(f,n,x):
    for _ in range(n): x=f(x)
    return x

def show_measure(rows):
    canvas(600, 300)
    largest=max(c for n,c in rows) or 1
    for i,(n,c) in enumerate(rows):
        rectangle(120,25+75*i,430*c/largest,35,color="#276bb0")
        text(12,48+75*i,"n="+str(n),size=17)
        ratio=round(c/n,2) if n else 0
        text(125,85+75*i,"calls="+str(c)+", ratio="+str(ratio),size=17)
    frame()
rows=[(n,profile(lambda x:x+1,n,0)[1]) for n in [10,40,160]]
show_measure(rows)
