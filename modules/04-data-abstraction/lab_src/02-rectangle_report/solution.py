def rectangle_report(rect):
    w,h=width(rect),height(rect)
    answer=(w*h,2*(w+h))
    show_dimensions(w,h,*answer)
    return answer
from scimigo import canvas,figure,frame,text

def width(rect):return rect("width")
def height(rect):return rect("height")

def rectangle(w,h):
    return lambda name:w if name=="width" else h

def show_dimensions(w,h,area,perimeter):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=220,
           values=[w,h,area,perimeter],indices=False)
    text(12,260,"width / height / area / perimeter",size=18)
    frame()

print(rectangle_report(rectangle(7,3)))
