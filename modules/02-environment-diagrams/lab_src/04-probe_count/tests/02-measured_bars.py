from scimigo import _frame_count, _frame
rows = []
for depth in [3, 6, 12]:
    fs = [{"bindings": {}, "parent": i - 1 if i else None} for i in range(depth)]
    fs[0]["bindings"]["key"] = 42
    result = measured_lookup(fs, depth - 1, "key")
    assert isinstance(result, tuple) and len(result) == 2, f"Return the pair (value, probes); got {result!r}."
    rows.append((depth, result[1]))
assert rows == [(3, 3), (6, 6), (12, 12)], f"A name bound only in the root costs one probe per frame: expected [(3, 3), (6, 6), (12, 12)] as (depth, probes); measured {rows}."
before = _frame_count(); show_probes(rows)
objects = _frame(before); bars = [o for o in objects if o["kind"] == "rectangle"]
assert len(bars) == 3, f"The chart needs one bar per depth; it has {len(bars)}."
for bar, (depth, count) in zip(bars, rows):
    assert abs(bar["width"] - 430 * count / 12) < 1e-8, f"The bar for depth {depth} must be proportional to its {count} probes."
    assert any(o["kind"] == "text" and o["value"] == "probes=" + str(count) for o in objects), f"The chart must label the depth-{depth} bar with probes={count}."
