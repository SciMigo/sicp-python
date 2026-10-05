show_step=lambda *args: None
calls=[]
f=lambda x:calls.append(x) or (x+2)
h=repeat(f,5)
assert callable(h) and calls==[], "Factory setup must not run f."
assert h(3)==13 and calls==[3,5,7,9,11], "Apply f exactly n times."
calls.clear()
assert h(0)==10 and calls==[0,2,4,6,8], "Reset the intermediate result on every invocation."
marker=object()
assert repeat(lambda x: (_ for _ in ()).throw(AssertionError('zero called f')),0)(marker) is marker, "Zero applications preserve the input object without a callback."
assert repeat(lambda x:x+1,3000)(0)==3000, "Handle long repetition without deeply nested calls."
assert repeat(lambda x:x+'!',3)('a')=='a!!!', "The operation need not work on numbers only."

