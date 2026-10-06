saved=combine
class BudgetExceeded(BaseException):pass
try:
    for n,sizes,mod in [(45,[1,4,6],97),(1200,[3,1,5],1009),(6000,[1,7,4],1000000007),(1200,[3,1,5],1009)]:
        count=[0]
        def counted(a,b,m):
            count[0]+=1
            if count[0]>n*len(sizes):raise BudgetExceeded()
            assert 0<=a<m and 0<=b<m,f"combine received {a} and {b} with modulus {m}: keep every count reduced below the modulus."
            return saved(a,b,m)
        combine=counted
        table=[1%mod]+[0]*n
        for k in range(1,n+1):table[k]=sum(table[k-s] for s in sizes if s<=k)%mod
        try:
            result=packing_plans(n,list(sizes),mod)
        except BudgetExceeded:
            raise AssertionError(f"n = {n} with {len(sizes)} sizes used more than {n*len(sizes)} additions: the same amounts are being worked out again and again.")
        except RecursionError:
            raise AssertionError(f"n = {n} needed more waiting calls than Python allows. The answer for {n} must not wait on a chain of {n} unfinished calls.")
        assert result==table[n],f"packing_plans({n}, {sizes}, {mod}) should be {table[n]}; got {result}."
        assert count[0]>0,"Add plan counts with combine, so the additions can be counted."
finally:
    combine=saved
