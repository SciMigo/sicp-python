from scimigo import _frame_count,_frame

def recorded(before):
    rows=[]
    for i in range(before,_frame_count()):
        pictures=[o for o in _frame(i) if o['kind']=='figure']
        assert len(pictures)==1, f'Expected one state figure in frame {i}; got {len(pictures)}'
        rows.append(pictures[0]['params']['values'])
    return rows

a=make_account(32,'p');before=_frame_count()
for pw,op,n in [('p','deposit',6),('bad','withdraw',9),('p','withdraw',10),('p','withdraw',40),('p','deposit',1)]:a(pw,op)(n)
got=recorded(before);want=[[38],[38],[28],[28],[29]]
assert got==want, f'Expected actual balances {want}; got {got}'
