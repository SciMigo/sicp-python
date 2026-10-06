def make_service(settings):
    saved=list(settings)
    def service(value):
        for scale,offset in saved:
            value=scale*value+offset
        return value
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
