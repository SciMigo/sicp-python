def run_trace(items,k):
    reset_trace()
    emit("start",k)
    pipeline=map(transform,filter(accept,source(items)))
    answer=[]
    for _ in range(k):
        try:value=next(pipeline)
        except StopIteration:break
        answer.append(value)
        emit("output",value)
    return answer
from scimigo import canvas,figure,frame,text

events=[]
pulled=[]
outputs=[]

def reset_trace():
    events.clear();pulled.clear();outputs.clear()

def draw(kind,value):
    canvas(600,350)
    if pulled:figure("array_state",x=0,y=0,width=600,height=140,values=list(pulled),indices=False)
    if outputs:figure("array_state",x=0,y=150,width=600,height=140,values=list(outputs),indices=False)
    text(12,325,kind+": "+str(value),size=18)
    frame()

def emit(kind,value):
    events.append((kind,value))
    if kind=="pull":pulled.append(value)
    if kind=="output":outputs.append(value)
    draw(kind,value)

def source(items):
    for item in items:
        emit("pull",item)
        yield item

def accept(item):
    emit("test",item)
    return item%3==0

def transform(item):
    emit("map",item)
    return item+100

print(run_trace([1,3,4,6,9],2))
