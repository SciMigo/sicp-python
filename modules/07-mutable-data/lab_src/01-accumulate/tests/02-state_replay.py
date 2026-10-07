from scimigo import _frame_count,_frame

def recorded(before):
    rows=[]
    for i in range(before,_frame_count()):
        pictures=[o for o in _frame(i) if o['kind']=='figure']
        assert len(pictures)==1, f'Expected one state figure in frame {i}; got {len(pictures)}'
        rows.append(pictures[0]['params']['values'])
    return rows

before=_frame_count();a=make_accumulator(10);m=make_monitored(a)
m(5);m(-4);m('reset-count');m(2)
got=recorded(before);want=[[15],[1],[11],[2],[0],[13],[1]]
assert got==want, f'Expected total/count frames {want}; got {got}'
before=_frame_count();count=m('how-many-calls?')
assert _frame_count()==before, f'Asking how-many-calls? should draw nothing; it recorded {_frame_count()-before} frame(s)'
assert count==1, f'One call since the reset; how-many-calls? returned {count!r}'
