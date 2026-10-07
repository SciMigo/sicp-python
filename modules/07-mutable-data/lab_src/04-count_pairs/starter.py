def count_pairs(root,fields):
    show_state('pairs counted',[0])
    return 0

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
    """n pairs; both fields of each pair point to the pair below it."""
    p=None
    for _ in range(n):p=[p,p]
    return p

def naive_encounters(root):
    """The count SICP exercise 3.16 complains about: every path to a pair counts again."""
    if not isinstance(root,list):return 0
    return 1+naive_encounters(root[0])+naive_encounters(root[1])

rows=[]
for n in (3,5,7):
    p=shared_stack(n)
    rows.append((n,naive_encounters(p),count_pairs(p,pair_fields)))
print(rows)
show_state('7 stacked pairs: paths counted / pairs counted',[rows[-1][1],rows[-1][2]])
