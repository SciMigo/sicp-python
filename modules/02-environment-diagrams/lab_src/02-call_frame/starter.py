def call_frame(function, caller, arguments):
    created={"bindings":dict(zip(function["params"],arguments)),"parent":caller}
    show_call(created)
    return created
from scimigo import canvas, figure, frame, text

def show_call(created):
    canvas(360,320)
    owner=created["parent"]
    figure("environment_diagram",x=0,y=0,width=360,height=275,frame_width=240,
           frames=[{"id":"owner","label":"Definition environment "+str(owner),"bindings":[{"name":"…","value":"omitted"}]},
                   {"id":"call","label":"Fresh call","parent":"owner",
                    "bindings":[{"name":k,"value":str(v)} for k,v in created["bindings"].items()]}])
    text(12,305,"Parent = definition environment "+str(owner),size=16)
    frame()

function={"params":["reading"],"parent":1}
created=call_frame(function,2,[3])
offsets={1:6,2:80}
print(created["bindings"]["reading"]+offsets[created["parent"]])
