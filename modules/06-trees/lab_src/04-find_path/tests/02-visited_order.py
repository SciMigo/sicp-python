from scimigo import _frame_count, _frame
def visited(target):
    before = _frame_count()
    result = find_path(sample, target)
    names = []
    for f in range(before, _frame_count()):
        figures = [o for o in _frame(f) if o['kind'] == 'figure']
        assert figures, "Every frame of the search should draw the hierarchy (call show_try)."
        names.extend(figures[0]['params']['highlights'])
    return result, names
result, names = visited(9)
assert result == [4, 0, 9], f"The first 9 lies under child 1: expected [4, 0, 9], got {result}."
assert names == ['root:4', '0:7', '1:0', '1.0:9'], f"A search for 9 examines root, 0, 1 and 1.0, then stops. Yours examined {names}."
result, names = visited(-8)
assert result is None, "No node is labelled -8, so the result is None."
assert names == ['root:4', '0:7', '1:0', '1.0:9', '1.1:9', '2:-3'], f"A failed search examines every node once, parents before children. Yours examined {names}."
result, names = visited(4)
assert result == [4] and names == ['root:4'], f"A match at the root examines one node and returns [4]. Got {result} after {names}."
