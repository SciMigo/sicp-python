show_stage=lambda *args: None
calls=[]
f=lambda x:calls.append(('f',x)) or (x-4)
g=lambda x:calls.append(('g',x)) or (3*x)
h=chain(f,g)
assert callable(h) and calls==[], "Constructing the operation must not invoke its callbacks."
assert h(2)==2 and calls==[('g',2),('f',6)], "Evaluate g first, then feed its result into f."
calls.clear()
assert h(-3)==-13 and calls==[('g',-3),('f',-9)], "Each invocation starts with its own input."

