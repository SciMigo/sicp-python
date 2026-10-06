from scimigo import _frame_count,_frame
class PullExceeded(BaseException):pass
class Guarded:
    def __init__(self,values,limit):self.values=iter(values);self.limit=limit;self.pulls=0
    def __iter__(self):return self
    def __next__(self):
        if self.pulls>=self.limit:raise PullExceeded()
        value=next(self.values);self.pulls+=1;return value
from itertools import count
for values,k,limit,expected in [([4,1,3,2,5,9],2,5,[(1,3),(2,5)]),([1,2,3],0,0,[]),(count(7),5,6,[(7,8),(8,9),(9,10),(10,11),(11,12)])]:
    readings=Guarded(values,limit);before=_frame_count()
    try:answer=rising_preview(readings,k)
    except PullExceeded:raise AssertionError("Do not request another source value after the kth rise; k=0 must not request the first value.")
    assert answer==expected and readings.pulls==limit,"Return the requested original adjacent pairs using exactly the needed source prefix."
    assert _frame_count()-before==1,"Record one completed preview."
    objects=_frame(before);figs=[o for o in objects if o['kind']=='figure']
    assert [o['params']['values'] for o in figs]==([list(answer[-1])] if answer else []),"Show the actual last returned adjacent pair, without inventing a pair for empty output."
    assert any(o['kind']=='text' and o['value']=='rising pairs returned='+str(len(answer)) for o in objects),"Draw the actual number of returned pairs."
