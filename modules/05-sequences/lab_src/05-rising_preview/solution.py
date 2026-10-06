def rising_preview(readings,k):
    result=[]
    if k:
        iterator=iter(readings)
        try:previous=next(iterator)
        except StopIteration:previous=None
        if previous is not None:
            for current in iterator:
                if current>previous:
                    result.append((previous,current))
                    if len(result)==k:break
                previous=current
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
