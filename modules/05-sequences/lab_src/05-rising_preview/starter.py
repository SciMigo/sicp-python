def rising_preview(readings,k):
    values=list(readings)
    pairs=[(a,b) for a,b in zip(values,values[1:]) if b>a]
    result=pairs[:k]
    show_preview(result)
    return result
from scimigo import canvas,figure,frame,text

def show_preview(result):
    canvas(600,300)
    if result:
        previous,current=result[-1]
        figure("array_state",x=0,y=0,width=600,height=220,
               values=[previous,current],indices=False)
    text(12,255,"rising pairs returned="+str(len(result)),size=18)
    text(12,285,"last returned adjacent pair shown",size=17)
    frame()

print(rising_preview(iter([5,2,4,4,1,3,8]),3))
