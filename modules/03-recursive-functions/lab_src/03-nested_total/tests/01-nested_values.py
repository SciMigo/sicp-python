import copy,random
saved=show_node;show_node=lambda *args:None
try:
    def oracle(node):
        pending=[node];total=0
        while pending:
            item=pending.pop()
            if isinstance(item,int):total+=item
            else:pending.extend(item)
        return total
    rng=random.Random(41)
    def sample(depth):
        if depth==0 or rng.random()<0.4:return rng.randrange(-8,9)
        return [sample(depth-1) for _ in range(rng.randrange(4))]
    cases=[[],3,[3,[2,[],[5]],1],[[-4],[2,[-3]]],[[[]]]]+[sample(4) for _ in range(30)]
    for node in cases:
        before=copy.deepcopy(node)
        got=nested_total(node)
        assert got==oracle(node),f"nested_total({node}) should be {oracle(node)}; got {got}. An integer is its own total; a list adds the totals of all its children, however deeply they nest."
        assert node==before,"Leave the input unchanged."
finally:show_node=saved
