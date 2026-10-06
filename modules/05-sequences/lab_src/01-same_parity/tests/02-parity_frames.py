from scimigo import _frame_count,_frame
values=[5,2,9,9,0];before=_frame_count();result=same_parity(*values)
assert result==[5,9,9],"The first argument sets odd parity for this call."
assert _frame_count()-before==len(values),"Record one frame after each input occurrence."
for i in range(len(values)):
    prefix=values[:i+1];kept=[x for x in prefix if x%2==1]
    figs=[o for o in _frame(before+i) if o['kind']=='figure']
    assert len(figs)==2,"Draw the visited input and retained output as separate rows."
    assert figs[0]['params']['values']==prefix and figs[1]['params']['values']==kept,"Each frame must describe exactly the prefix already visited."
