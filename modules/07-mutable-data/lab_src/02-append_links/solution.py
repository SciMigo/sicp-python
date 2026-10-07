def append_in_place(first,second):
    if first is None:
        show_links(first,second,'empty')
        return second
    current=first
    show_links(first,second,current)
    while current[1] is not None:
        current=current[1]
        show_links(first,second,current)
    current[1]=second
    show_links(first,second,'linked')
    return first

from scimigo import canvas,figure,text,frame

def chain(values):
    result=None
    for value in reversed(values):result=[value,result]
    return result

def pairs_from(head):
    found=[]
    while head is not None and not any(head is p for p in found):
        found.append(head);head=head[1]
    return found

def show_links(first,second,current):
    """Draw the chain reached from first and, while it is still separate, the one from second.
    current is the pair being visited (highlighted), or the word 'linked' or 'empty'."""
    top=pairs_from(first)
    joined=second is not None and any(second is p for p in top)
    bottom=[] if joined else pairs_from(second)
    names={id(p):'p'+str(i) for i,p in enumerate(top+bottom)}
    def draw(pairs,y,label,head):
        nodes=[{'id':names[id(p)],'value':str(p[0])} for p in pairs]
        marks={names[id(p)]:'current' for p in pairs if p is current}
        pointers=[{'node':names[id(head)],'label':label}]
        if label=='first' and joined:pointers.append({'node':names[id(second)],'label':'second'})
        figure('linked_list',x=0,y=y,width=600,height=130,type='singly',nodes=nodes,
               highlights=marks,pointers=pointers,show_null=True)
    canvas(600,330)
    if top:draw(top,0,'first',first)
    if bottom:draw(bottom,150,'second',second)
    note=current if isinstance(current,str) else 'visiting '+str(current[0])
    text(15,315,note,size=18)
    frame()

x=chain(['c','d','e']);y=chain(['f','g']);alias=x
print(append_in_place(x,y) is alias)
