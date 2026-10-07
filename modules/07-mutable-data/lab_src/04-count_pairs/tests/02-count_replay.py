from scimigo import _frame_count,_frame
def recorded(before):
    rows=[]
    for i in range(before,_frame_count()):
        pictures=[o for o in _frame(i) if o['kind']=='figure']
        assert len(pictures)==1, f'Each frame should hold one count; frame {i-before+1} holds {len(pictures)} figures'
        rows.append(pictures[0]['params']['values'])
    return rows
p=shared_stack(4);before=_frame_count();got_count=count_pairs(p,pair_fields)
assert got_count==4, f'A stack of 4 shared pairs has 4 pairs; count_pairs returned {got_count!r}'
got=recorded(before);want=[[1],[2],[3],[4]]
assert got==want, f'Counting 4 pairs should draw {want}, one frame per new pair; it drew {got}'
