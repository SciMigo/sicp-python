from scimigo import _frame_count,_frame

def recorded(before):
    rows=[]
    for i in range(before,_frame_count()):
        pictures=[o for o in _frame(i) if o['kind']=='figure']
        assert len(pictures)==1, f'Expected one state figure in frame {i}; got {len(pictures)}'
        rows.append(pictures[0]['params']['values'])
    return rows

before=_frame_count();got_result=run_access(supplied_account(18,'a'),[('join','g','owner','a','b'),('use','g','b','deposit',4),('join','bad','g','x','y'),('use','owner','a','withdraw',7)])
got=recorded(before);want=[[2,'Joined'],[2,22],[2,'Incorrect password'],[2,15]]
assert got==want, f'Expected route-count/result frames {want}; got {got}'
