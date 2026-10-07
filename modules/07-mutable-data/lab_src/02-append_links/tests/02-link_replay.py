from scimigo import _frame_count,_frame
a=chain(['h','i']);b=chain(['j']);before=_frame_count();append_in_place(a,b)
def summary(index):
    rows=[]
    for o in _frame(index):
        if o['kind']=='figure':
            p=o['params']
            rows.append(([n['value'] for n in p['nodes']],sorted(p['highlights']),sorted((q['label'],q['node']) for q in p['pointers'])))
    return rows
got=[summary(i) for i in range(before,_frame_count())]
want=[[(['h','i'],['p0'],[('first','p0')]),(['j'],[],[('second','p2')])],
      [(['h','i'],['p1'],[('first','p0')]),(['j'],[],[('second','p2')])],
      [(['h','i','j'],[],[('first','p0'),('second','p2')])]]
assert len(got)==3, f"A two-pair first chain needs three frames (visit h, visit i, then 'linked'); recorded {len(got)}"
for i,(g,x) in enumerate(zip(got,want)):
    assert g==x, f'Frame {i+1} should show chains, highlighted pair and labels {x}; it shows {g}. Pass show_links the pair you are visiting, and draw the last frame after changing the link.'
before=_frame_count();append_in_place(None,chain(['k']))
assert _frame_count()-before==1, f"An empty first chain draws one frame, with 'empty'; recorded {_frame_count()-before}"
