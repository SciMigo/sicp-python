def make_box(start):
    total=start
    def change(delta):
        result=start+delta  # preserve accumulated changes instead
        show_box("change",start,result)
        return result
    def read():
        show_box("read",start,total)
        return total
    def reset():
        show_box("reset",start,start)
        return start
    return change,read,reset
from scimigo import canvas,figure,frame,text

def show_box(operation,start,total):
    canvas(360,240)
    figure("environment_diagram",x=0,y=0,width=360,height=195,frame_width=240,
           frames=[{"id":"box","label":"Captured box bindings","bindings":[
               {"name":"start","value":str(start)},{"name":"total","value":str(total)}]}])
    text(12,225,operation+": total="+str(total),size=16)
    frame()

change,read,reset=make_box(20)
print(change(5),change(-2),read(),reset())
