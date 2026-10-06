from scimigo import _frame_count,_frame
class BudgetExceeded(BaseException):pass
for size in (1,8,500):
    class Record:
        def __init__(self,i):self.i=i
        def __getitem__(self,key):raise AssertionError("These records have no public positional layout.")
    records=[Record(i) for i in range(size)];counts={id(r):0 for r in records}
    def getweight(r):
        counts[id(r)]+=1
        if counts[id(r)]>1:raise BudgetExceeded()
        return r.i%13
    def getlabel(r):return 'tag'+str(r.i)
    before=_frame_count()
    try:answer=manifest_report(records,getweight,getlabel)
    except BudgetExceeded:raise AssertionError("The weight accessor may be called only once per record; retain values already read.")
    expected=(sum(i%13 for i in range(size)),'tag'+str(min(size-1,12)))
    assert answer==expected,"Opaque records still need the correct total and first heaviest label."
    assert _frame_count()-before==1,"Draw one completed report after each invocation."
    objects=_frame(before);fig=next(o for o in objects if o['kind']=='figure')
    assert fig['params']['values']==[answer[0]],"Draw this report's computed total."
    assert any(o['kind']=='text' and o['value']=='heaviest label='+str(answer[1]) for o in objects),"Draw this report's selected label."
