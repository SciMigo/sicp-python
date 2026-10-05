def nested_total(node,path=()):
    if isinstance(node,int):
        answer=node
    else:
        answer=sum(child for child in node if isinstance(child,int))
        # Nested children contribute too; visit each one separately.
    show_node(path,node,answer)
    return answer
from scimigo import canvas,figure,frame,text

def show_node(path,node,answer):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=220,
           values=["integer" if isinstance(node,int) else "list",answer],
           cell_width=110,indices=False)
    text(12,260,"completed path="+str(path),size=18)
    frame()

print(nested_total([3,[2,[],[5]],1]))
