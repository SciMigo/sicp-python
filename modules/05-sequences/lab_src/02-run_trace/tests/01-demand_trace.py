draw = lambda *args: None
for items, k in [([1, 3, 4, 6, 9], 2), ([0, 0, 2], 2), ([-2, -3, 4, 6], 1), ([], 3), ([1, 2], 5), ([3, 6], 0), ([3, 6], 5)]:
    expected = []
    wanted = [('start', k)]
    if k:
        for item in items:
            wanted += [('pull', item), ('test', item)]
            if item % 3 == 0:
                value = item + 100
                expected.append(value)
                wanted += [('map', item), ('output', value)]
                if len(expected) == k:
                    break
    got = run_trace(items, k)
    assert got == expected, f"run_trace({items}, {k}) should return {expected}; got {got!r}."
    if events != wanted:
        at = next((i for i, (a, b) in enumerate(zip(events, wanted)) if a != b), min(len(events), len(wanted)))
        seen = events[at] if at < len(events) else 'nothing more'
        due = wanted[at] if at < len(wanted) else 'nothing more'
        raise AssertionError(f"run_trace({items}, {k}): event {at + 1} should be {due}, but it was {seen}. Only accepted items are mapped, each result is output as it arrives, and nothing is pulled after the last result asked for.")
