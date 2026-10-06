import random
class Table(dict):
    calls=0
    def __contains__(self,key):
        Table.calls+=1
        return super().__contains__(key)
rng=random.Random(4051)
for depth in [1,2,7,19,53]:
    for owner in [None,0,depth-1,rng.randrange(depth)]:
        fs=[{'bindings':Table(),'parent':i-1 if i else None} for i in range(depth)]
        if owner is not None:fs[owner]['bindings']['key']=0
        Table.calls=0
        value,probes=measured_lookup(fs,depth-1,'key')
        expected=depth if owner is None else depth-owner
        assert probes==Table.calls==expected,"Count each actual membership test, including the successful one."
        assert value==(None if owner is None else 0)
assert measured_lookup([],None,'key')==(None,0)

fs=[{'bindings':Table({'key':3}),'parent':None},{'bindings':Table({'key':99}),'parent':0},{'bindings':Table(),'parent':0}]
Table.calls=0
assert measured_lookup(fs,2,'key')==(3,2) and Table.calls==2, 'Follow actual parent links.'
