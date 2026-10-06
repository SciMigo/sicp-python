def append_in_place(first,second):
    if first is None:
        show_links(first,second,'empty')
        return second
    current=first
    while current[1] is not None:
        show_links(first,second,current[0])
        current=current[1]
    show_links(first,second,current[0])
    current[1]=second
    show_links(first,second,'linked')
    return first

from scimigo import canvas,figure,text,frame

def chain(values):
    result=None
    for value in reversed(values):result=[value,result]
    return result

def pair_rows(first,second):
    nodes=[]
    def visit(p):
        if p is None or any(p is old for old in nodes):return
        nodes.append(p);visit(p[1])
    visit(first);visit(second)
    def name(p):
        if p is None:return '-'
        return 'p'+str(next(i for i,x in enumerate(nodes) if p is x))
    return [f'{name(p)}:{p[0]}->{name(p[1])}' for p in nodes]

def show_links(first,second,current):
    rows=pair_rows(first,second)
    # At most eight nodes in pictured inputs; keep each row readable.
    canvas(600,430)
    text(15,30,'first / second references; current='+str(current),size=19)
    for i,row in enumerate(rows):text(25,70+i*42,row,size=19)
    figure('array_state',x=340,y=70,width=250,height=120,
           values=[len(rows)],indices=False,caption='pair identities')
    frame()

x=chain(['c','d','e']);y=chain(['f','g']);alias=x
print(append_in_place(x,y) is alias)
