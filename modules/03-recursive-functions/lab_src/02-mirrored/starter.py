def mirrored(items,left=0,right=None):
    if right is None:right=len(items)-1
    show_window(items,left,right,"enter",None)
    answer=True if left>=right else items[left]==items[right]
    # Matching outside values are not enough: check the inside too.
    show_window(items,left,right,"leave",answer)
    return answer
from scimigo import canvas,figure,frame,text

def show_window(items,left,right,stage,answer):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=220,
           values=list(items),indices=True,
           highlights={str(i):"current" for i in range(max(0,left),min(len(items),right+1))},
           pointers=[{"index":left,"label":"left","position":"above"},
                     {"index":right,"label":"right","position":"below"}])
    text(12,250,"left="+str(left)+"  right="+str(right)+"  "+stage,size=18)
    text(12,280,"answer="+str(answer),size=18)
    frame()

print(mirrored([4,7,2,7,4]))
