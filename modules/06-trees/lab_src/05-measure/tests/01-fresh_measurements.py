show_measure=lambda *args: None
original_label=label
observed=[0]
def counted(node):
    observed[0]+=1
    return original_label(node)
label=counted
for n in [7,19,53,211]:
    observed[0]=0
    value=profile(make_star(n))
    assert value==observed[0], f"profile reported {value} reads but made {observed[0]}: report the reads that happened, not a stored number."
    assert value==n, f"A hierarchy of {n} nodes needs {n} label reads, one per node; yours made {value}."
t={'value':4,'children':[make_star(9),make_star(12),{'value':1,'children':[{'value':2,'children':[make_star(5)]}]}]}
observed[0]=0
value=profile(t)
assert value==observed[0]==29, f"On a deeper 29-node hierarchy profile reported {value} and made {observed[0]} reads: descend below the first level."
