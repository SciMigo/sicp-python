import random
rng=random.Random(3003)
def oracle(n,sizes,mod):
    table=[1%mod]+[0]*n
    for k in range(1,n+1):table[k]=sum(table[k-s] for s in sizes if s<=k)%mod
    return table[n]
for _ in range(25):
    n=rng.randrange(0,9);sizes=rng.sample(range(1,7),rng.randrange(0,4));mod=rng.choice([1,2,7,97])
    old=list(sizes)
    got=packing_plans(n,sizes,mod)
    assert got==oracle(n,old,mod),f"packing_plans({n}, {old}, {mod}) should be {oracle(n,old,mod)}; got {got}."
    assert sizes==old,"Do not change the list of sizes."
assert packing_plans(0,[],13)==1,"Zero units has exactly one plan, the empty one, even with no sizes."
assert packing_plans(5,[],13)==0,"With no permitted sizes there is no plan for 5 units."
assert packing_plans(3,[1,2],97)==3,"Sizes 1 and 2 fill 3 units in three ordered plans: [1,1,1], [1,2] and [2,1]."
assert packing_plans(3,[2,1],97)==3,"The order in which sizes are listed must not change the count."
