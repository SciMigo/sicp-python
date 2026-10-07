show_state=lambda *args:None
class TooManyReads(BaseException):pass
def run(root,want,what):
    reads=[]
    def fields(pair):
        reads.append(pair)
        if len(reads)>4*want+8:raise TooManyReads()
        return pair[0],pair[1]
    try:
        got=count_pairs(root,fields)
    except TooManyReads:
        raise AssertionError(f'{what}: fields was called more than {4*want+8} times for {want} pairs. Remember each pair before following its parts, or a cycle never ends.')
    except RecursionError:
        raise AssertionError(f'{what}: the traversal recursed without end. Remember each pair before following its parts.')
    assert got==want, f'{what}: there are {want} distinct pairs; count_pairs returned {got!r}'
    assert len(reads)==want and len({id(p) for p in reads})==want, f'{what}: call fields once for each of the {want} pairs; it was called {len(reads)} times on {len({id(p) for p in reads})} different pairs'
for n in (0,1,4,6,9):
    run(shared_stack(n),n,f'a stack of {n} shared pairs')
run([1,[2,[3,None]]],3,'a plain chain of three')
a=[1,2];b=[1,2]
run([a,b],3,'two different pairs with equal contents under one parent')
run([a,a],2,'one pair reached twice from its parent')
loop=[None,None];loop[0]=loop
run(loop,1,'one pair whose first part is itself')
x=['x',None];y=['y',x];x[1]=y
run(x,2,'two pairs pointing at each other')
run(7,0,'a root that is not a pair')
deep=None
for i in range(150):deep=[i,deep]
run(deep,150,'a chain of 150 pairs')
