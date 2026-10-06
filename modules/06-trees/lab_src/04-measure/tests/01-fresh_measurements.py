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
    assert value==observed[0], "Report the reads actually made, not a stored expected number."
    assert value==n, "Inspect each of the n node labels once."
# Also test a non-star, unpublished shape.
t={'value':4,'children':[make_star(9),make_star(12)]}
observed[0]=0
assert profile(t)==22 and observed[0]==22, "Count actual reads on a different shape."

