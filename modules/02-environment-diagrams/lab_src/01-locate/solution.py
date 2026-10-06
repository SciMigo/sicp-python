def locate(frames, current, name):
    while current is not None:
        show_scope(frames,current,name)
        bindings=frames[current]["bindings"]
        if name in bindings:
            return bindings[name],current
        current=frames[current]["parent"]
    raise NameError(name)
from scimigo import canvas, figure, frame, text

def show_scope(frames, current, name):
    canvas(360, 480)
    shown = [{"id":str(i), "label":"Frame "+str(i),
              "parent":str(f["parent"]) if f["parent"] is not None else None,
              "bindings":[{"name":k,"value":str(v)} for k,v in f["bindings"].items()]}
             for i,f in enumerate(frames)]
    figure("environment_diagram", x=0,y=0,width=360,height=440,
           frames=shown, frame_width=240,
           highlights={"frames":{str(current):"current"}})
    text(12,465,"Probe "+name+" in frame "+str(current),size=16)
    frame()

frames=[{"bindings":{"offset":80},"parent":None},
        {"bindings":{"offset":6},"parent":0},
        {"bindings":{"reading":3},"parent":1}]
try:
    print(locate(frames,2,"offset"))
except NameError:
    print("Offset was not found by this lookup.")
