original=source
for items,k in [(list(range(1,18)),2),([3,4,4,7,8],2),([],0),([1,2],5),([4,8],0)]:
    matches=[x+10 for x in items if x%4==0][:k]
    needed=0;accepted=0
    if k:
        for x in items:
            needed+=1
            if x%4==0:
                accepted+=1
                if accepted==k:break
    assert profile(eager,items,k)==(matches,len(items)),"The supplied eager solver reads the complete finite input before taking a prefix."
    assert profile(lazy,items,k)==(matches,needed),"Count actual source yields, not output length."
    assert source is original,"Leave the supplied source unchanged."
def unusual(items,k,read_source):return list(islice(read_source(items),2))
assert profile(unusual,[7,8,9],0)==([7,8],2),"Observe the solver's real consumption rather than inferring it from k."
def broken(items,k,read_source):
    next(read_source(items))
    raise ValueError('expected')
raised=False
try:profile(broken,[1],1)
except ValueError:raised=True
assert raised and source is original,"Propagate the strategy error without changing source."
