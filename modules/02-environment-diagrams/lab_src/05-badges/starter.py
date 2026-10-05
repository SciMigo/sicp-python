def prepare_badges(prefixes):
    badges=[]
    for prefix in prefixes:
        def badge(reading):
            return prefix,reading
        badges.append(badge)
    return badges
from scimigo import canvas,figure,frame,text

def show_badges(badges,reading):
    actual=[badge(reading)[0] for badge in badges]
    canvas(600,280)
    figure("array_state",x=0,y=0,width=600,height=230,values=actual,indices=True)
    text(12,260,"Reported prefixes for reading "+str(reading),size=18)
    frame()

badges=prepare_badges([4,9,2])
show_badges(badges,7)
