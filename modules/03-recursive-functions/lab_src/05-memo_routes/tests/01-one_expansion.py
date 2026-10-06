saved_transition=transition;saved_record=record_state
record_state=lambda *a:None
class BudgetExceeded(BaseException):pass
try:
    for n in [0,1,4,12,37,120,200,37]:
        seen=[]
        def watched(k):
            seen.append(k)
            if len(seen)>n:raise BudgetExceeded()
            return saved_transition(k)
        transition=watched
        table=[1]+[0]*n
        for k in range(1,n+1):table[k]=table[k-1]+(table[k-3] if k>=3 else 0)
        try:
            result=memo_routes(n)
        except BudgetExceeded:
            raise AssertionError(f"memo_routes({n}) expanded more than {n} states, so some state was expanded twice. Look a state up before expanding it.")
        except RecursionError:
            raise AssertionError(f"memo_routes({n}) ran out of call depth. n is at most 200; check that every chain of calls reaches 0 or a negative state.")
        assert result==table[n],f"memo_routes({n}) should be {table[n]}; got {result}."
        assert all(k>0 for k in seen),"transition was called for 0 or a negative state; those are base cases."
        assert sorted(seen)==list(range(1,n+1)),f"memo_routes({n}) should expand each state from 1 to {n} exactly once, even when an earlier call already ran; it expanded {len(seen)} states."
finally:
    transition=saved_transition;record_state=saved_record
