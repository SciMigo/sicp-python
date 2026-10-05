saved=combine
class BudgetExceeded(BaseException):pass
for n,sizes,mod in [(45,[1,4,6],97),(1200,[3,1,5],1009),(6000,[1,7,4],1000000007)]:
    count=[0]
    def counted(a,b,m):
        count[0]+=1
        if count[0]>n*len(sizes):raise BudgetExceeded('Repeated branches exceed the addition budget.')
        assert 0<=a<m and 0<=b<m,"Keep intermediate residues bounded by the modulus."
        return saved(a,b,m)
    combine=counted
    table=[1%mod]+[0]*n
    for k in range(1,n+1):table[k]=sum(table[k-s] for s in sizes if s<=k)%mod
    try:
        result=packing_plans(n,sizes,mod)
    except BudgetExceeded as exc:
        raise AssertionError(str(exc))
    assert result==table[n],"Handle large input without a deep Python call chain."
combine=saved
