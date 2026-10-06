import random
class Table(dict):
    calls = 0
    def __contains__(self, key):
        Table.calls += 1
        return super().__contains__(key)
rng = random.Random(4051)
for depth in [1, 2, 7, 19, 53]:
    for owner in [None, 0, depth - 1, rng.randrange(depth)]:
        fs = [{"bindings": Table(), "parent": i - 1 if i else None} for i in range(depth)]
        if owner is not None: fs[owner]["bindings"]["key"] = 0
        Table.calls = 0
        result = measured_lookup(fs, depth - 1, "key")
        assert isinstance(result, tuple) and len(result) == 2, f"Return the pair (value, probes); got {result!r}."
        value, probes = result
        expected = depth if owner is None else depth - owner
        where = "no frame" if owner is None else f"frame {owner}"
        assert Table.calls == expected, f"Depth {depth}, key bound in {where}, lookup from frame {depth - 1}: the walk should make {expected} membership tests (name in bindings); the check counted {Table.calls}."
        assert probes == Table.calls, f"Depth {depth}, key bound in {where}: you reported {probes} probes but {Table.calls} membership tests were made. Count every test, including the one that succeeds."
        assert value == (None if owner is None else 0) and (owner is None or value is not None), f"Depth {depth}, key bound in {where}: the value must be {None if owner is None else 0!r} (a binding to 0 is a hit, not a miss); got {value!r}."
assert measured_lookup([], None, "key") == (None, 0), "Starting from no frame at all makes 0 probes and returns (None, 0)."
fs = [{"bindings": Table({"key": 3}), "parent": None}, {"bindings": Table({"key": 99}), "parent": 0}, {"bindings": Table(), "parent": 0}]
Table.calls = 0
result = measured_lookup(fs, 2, "key")
assert result == (3, 2) and Table.calls == 2, f"Frame 2's parent is frame 0, not frame 1: expected (3, 2) with 2 tests, got {result!r} with {Table.calls}. Follow the parent links."
