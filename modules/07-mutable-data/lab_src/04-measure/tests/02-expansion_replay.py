from scimigo import _frame_count,_frame

def recorded(before):
    rows=[]
    for i in range(before,_frame_count()):
        pictures=[o for o in _frame(i) if o['kind']=='figure']
        assert len(pictures)==1, f'Expected one state figure in frame {i}; got {len(pictures)}'
        rows.append(pictures[0]['params']['values'])
    return rows

p=shared_stack(3);before=_frame_count();got_result=measure(naive,p,pair_fields)
got=recorded(before);want=[[i] for i in range(1,8)]
assert got==want, f'Expected measured expansion frames {want}; got {got}'
before=_frame_count();measure(distinct,p,pair_fields);got=recorded(before);want=[[1],[2],[3]]
assert got==want, f'Expected distinct expansion frames {want}; got {got}'
