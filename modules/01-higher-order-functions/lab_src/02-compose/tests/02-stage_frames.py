from scimigo import _frame_count, _frame
h = compose(lambda x: x - 4, lambda x: 3 * x)
before = _frame_count()
got = h(2)
assert got == 2, f"g(2) is 6 and f(6) is 2; your function returned {got}."
recorded = _frame_count() - before
assert recorded == 2, f"One call of the composed function has two stages, so two frames; recorded {recorded}."
for i, (name, a, b) in enumerate([('g', 2, 6), ('f', 6, 2)]):
    objects = _frame(before + i)
    fig = next((o for o in objects if o['kind'] == 'figure'), None)
    assert fig and fig['params']['values'] == [a, b], f"Frame {i + 1} must show stage {name} taking {a} to {b}."
    assert any(o['kind'] == 'text' and o['value'] == f'{name}: {a} -> {b}' for o in objects), f"Frame {i + 1} must be labelled '{name}: {a} -> {b}': name the function that actually ran."
