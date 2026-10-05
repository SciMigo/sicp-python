import random
rng=random.Random(3003)
def oracle(n,sizes,mod):
    table=[1%mod]+[0]*n
    for k in range(1,n+1):table[k]=sum(table[k-s] for s in sizes if s<=k)%mod
    return table[n]
for _ in range(25):
    n=rng.randrange(0,9);sizes=rng.sample(range(1,7),rng.randrange(0,4));mod=rng.choice([1,2,7,97])
    old=list(sizes)
    assert packing_plans(n,sizes,mod)==oracle(n,sizes,mod),"Count ordered plans using these settings, including the empty plan."
    assert sizes==old
assert packing_plans(0,[],13)==1 and packing_plans(5,[],13)==0
assert packing_plans(3,[1,2],97)==3,"Ordered plans are [1,1,1], [1,2], and [2,1]."
