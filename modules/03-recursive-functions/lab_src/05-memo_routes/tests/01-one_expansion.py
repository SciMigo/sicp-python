saved_transition=transition;saved_record=record_state
record_state=lambda *a:None
class BudgetExceeded(BaseException):pass
for n in [0,1,4,12,37,120,200]:
    seen=[]
    def watched(k):
        seen.append(k)
        if len(seen)>n:raise BudgetExceeded('Repeated work exceeds the positive-state budget.')
        return saved_transition(k)
    transition=watched
    table=[1]+[0]*n
    for k in range(1,n+1):table[k]=table[k-1]+(table[k-3] if k>=3 else 0)
    try:
        result=memo_routes(n)
    except BudgetExceeded as exc:
        raise AssertionError(str(exc))
    assert result==table[n]
    assert sorted(seen)==list(range(1,n+1)),"Expand each positive state exactly once."
transition=saved_transition;record_state=saved_record
