from scimigo import _frame_count,_frame
a=chain(['h','i']);b=chain(['j']);before=_frame_count();append_in_place(a,b)
frames=[_frame(i) for i in range(before,_frame_count())]
got=[[o['value'] for o in f if o['kind']=='text'] for f in frames]
want=[['first / second references; current=h','p0:h->p1','p1:i->-','p2:j->-'],['first / second references; current=i','p0:h->p1','p1:i->-','p2:j->-'],['first / second references; current=linked','p0:h->p1','p1:i->p2','p2:j->-']]
assert got==want, f'Expected traversal and changed link rows {want}; got {got}'
