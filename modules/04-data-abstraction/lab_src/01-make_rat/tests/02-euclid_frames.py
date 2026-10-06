from scimigo import _frame_count, _frame
def figure_values(index):
    figures = [o for o in _frame(index) if o['kind'] == 'figure']
    return figures[0]['params']['values'] if figures else None
for (n, d), steps, stored in [((15, -25), [[15, 25], [25, 15], [15, 10], [10, 5]], (-3, 5)), ((0, 4), [[0, 4]], (0, 1)), ((9, 3), [[9, 3]], (3, 1))]:
    before = _frame_count()
    result = make_rat(n, d)
    assert result == stored, f"make_rat({n}, {d}) should be stored as {stored}; got {result!r}."
    recorded = _frame_count() - before
    assert recorded == len(steps) + 1, f"make_rat({n}, {d}) needs {len(steps)} Euclid frame(s) and one frame for the stored fraction; recorded {recorded}."
    for i, pair in enumerate(steps):
        assert figure_values(before + i) == pair, f"make_rat({n}, {d}): Euclid frame {i + 1} should show {pair}; it shows {figure_values(before + i)}. Start from the absolute values and call show_gcd before replacing the pair."
    last = figure_values(before + len(steps))
    assert last == [n, d, stored[0], stored[1]], f"The last frame should show {[n, d, stored[0], stored[1]]}: the inputs and the parts actually stored; it shows {last}."
