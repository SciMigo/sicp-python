def total_terms(values, term):
    total=0
    for i,value in enumerate(values):
        total+=value  # apply the caller's rule instead
        show(values, i+1, total)
    return total
from scimigo import canvas, figure, frame, text

def show(values, processed, total):
    canvas(600, 360)
    if values:
        brackets=[{"from":0,"to":processed-1,"label":"processed"}] if processed else []
        figure("array_state", x=0, y=0, width=600, height=300,
               values=list(values), indices=True, brackets=brackets)
    text(15, 335, "Processed="+str(processed)+", total="+str(total), size=18)
    frame()
print(total_terms([4,-1,3], lambda v:v*v))
