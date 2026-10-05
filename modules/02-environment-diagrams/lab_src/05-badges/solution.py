def prepare_badges(prefixes):
    def prepare_one(prefix):
        def badge(reading):
            return prefix,reading
        return badge
    return [prepare_one(prefix) for prefix in prefixes]
from scimigo import canvas,figure,frame,text

def show_badges(badges,reading):
    actual=[badge(reading)[0] for badge in badges]
    canvas(600,280)
    figure("array_state",x=0,y=0,width=600,height=230,values=actual,indices=True)
    text(12,260,"Reported prefixes for reading "+str(reading),size=18)
    frame()

badges=prepare_badges([4,9,2])
show_badges(badges,7)
