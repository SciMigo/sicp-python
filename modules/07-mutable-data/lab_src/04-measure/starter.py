def measure(strategy,root,fields):
    show_state('measurement not implemented',[0])
    return strategy(root,fields),0

from scimigo import canvas,figure,text,frame

def show_state(label,values):
    canvas(600,260)
    text(15,35,label,size=19)
    figure('array_state',x=0,y=65,width=600,height=160,
           values=list(values) or ['empty'],indices=False,cell_width=110)
    frame()

def pair_fields(pair):
    return pair[0],pair[1]

def shared_stack(n):
    p=None
    for _ in range(n):p=[p,p]
    return p

def naive(root,fields):
    if not isinstance(root,list):return 0
    left,right=fields(root)
    return 1+naive(left,fields)+naive(right,fields)

def distinct(root,fields):
    seen=set();todo=[root]
    while todo:
        p=todo.pop()
        if not isinstance(p,list) or id(p) in seen:continue
        seen.add(id(p));left,right=fields(p);todo.extend((left,right))
    return len(seen)

for n in (3,5,7):
    p=shared_stack(n)
    repeated=measure(naive,p,pair_fields)
    unique=measure(distinct,p,pair_fields)
    print(repeated,unique)
    show_state('n='+str(n)+': naive / distinct expansions',[repeated[1],unique[1]])
