from scimigo import _frame_count, _frame
before=_frame_count()
rows=[(n,profile(make_star(n))) for n in (9,27,81)]
assert rows==[(9,9),(27,27),(81,81)], f"Measured (n, reads) rows should be [(9, 9), (27, 27), (81, 81)]; yours are {rows}."
show_measure(rows)
assert _frame_count()-before==1, "show_measure should record exactly one frame."
objects=_frame(before)
bars=[o for o in objects if o['kind']=='rectangle']
assert len(bars)==3, "Draw a bar for each measured row."
for bar,(n,c) in zip(bars,rows):
    assert abs(bar['width']-430*c/81)<1e-6, f"The bar for n={n} should be proportional to its {c} reads."
    assert any(o['kind']=='text' and o['value']=='n='+str(n) for o in objects), f"Label the bar for n={n}."
    assert any(o['kind']=='text' and o['value'].startswith('reads='+str(c)+',') for o in objects), f"Show the measured count {c} beside its bar."
