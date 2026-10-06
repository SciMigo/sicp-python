def manifest_report(records,weight_of,label_of):
    total=sum(weight_of(record) for record in records)
    heaviest=None
    if records:
        best=max(records,key=weight_of)
        heaviest=label_of(best)
    show_report(total,heaviest)
    return total,heaviest
from scimigo import canvas,figure,frame,text

def weight_of(record):return record[1]
def label_of(record):return record[0]

def show_report(total,heaviest):
    canvas(600,300)
    figure("array_state",x=0,y=0,width=600,height=220,
           values=[total],indices=False)
    text(12,250,"total weight="+str(total),size=18)
    text(12,280,"heaviest label="+str(heaviest),size=18)
    frame()

print(manifest_report([('birch',6),('cedar',9),('elm',9)],weight_of,label_of))
