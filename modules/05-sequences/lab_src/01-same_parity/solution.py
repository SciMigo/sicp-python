def same_parity(first,*rest):
    result=[]
    visited=[]
    for item in (first,)+rest:
        visited.append(item)
        if item%2==first%2:result.append(item)
        show_parity(visited,result)
    return result
from scimigo import canvas,figure,frame,text

def show_parity(visited,result):
    canvas(600,360)
    figure("array_state",x=0,y=0,width=600,height=140,
           values=list(visited) if visited else ["not visited"],cell_width=110,indices=False)
    figure("array_state",x=0,y=160,width=600,height=140,
           values=list(result) if result else ["none retained"],cell_width=110,indices=False)
    text(12,330,"visited above / retained below",size=18)
    frame()

print(same_parity(8,3,12,0,7,8))
