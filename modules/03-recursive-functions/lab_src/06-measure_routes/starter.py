def measure(solver,n):
    return solver(n),0  # observe transitions rather than guessing
from scimigo import canvas,rectangle,text,frame

def transition(k):
    return k-1,k-3

def naive_routes(n):
    if n<0:return 0
    if n==0:return 1
    a,b=transition(n)
    return naive_routes(a)+naive_routes(b)

def cached_routes(n):
    cache={0:1}
    def solve(k):
        if k<0:return 0
        if k not in cache:
            a,b=transition(k)
            cache[k]=solve(a)+solve(b)
        return cache[k]
    return solve(n)

def show_expansions(rows):
    canvas(600,370)
    largest=max(a for n,a,b in rows) or 1
    for i,(n,naive,cached) in enumerate(rows):
        y=20+110*i
        text(12,y+22,"n="+str(n),size=18)
        rectangle(120,y,420*naive/largest,22,color="#276bb0")
        text(125,y+43,"naive="+str(naive),size=17)
        rectangle(120,y+55,420*cached/largest,22,color="#7c3aed")
        text(125,y+98,"cached="+str(cached),size=17)
    frame()

rows=[]
for n in [5,9,13]:
    rows.append((n,measure(naive_routes,n)[1],measure(cached_routes,n)[1]))
show_expansions(rows)
