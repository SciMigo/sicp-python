def make_service(settings):
    scale,offset=1,0
    for a,b in settings:
        scale,offset=a*scale,a*offset+b
    def service(value):
        return scale*value+offset
    return service
from scimigo import canvas, figure, frame, text

def show_stage(name, value, result):
    canvas(600, 360)
    figure("array_state", x=0, y=0, width=600, height=290,
           values=[value,result], indices=False)
    text(15, 335, name+": "+str(value)+" -> "+str(result), size=18)
    frame()
settings=[(2,1),(-1,4)]
service=make_service(settings)
show_stage("service",3,service(3))
