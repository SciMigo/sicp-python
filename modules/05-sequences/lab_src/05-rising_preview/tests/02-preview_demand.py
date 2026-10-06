from scimigo import _frame_count, _frame
class PullExceeded(BaseException):
    pass
class Guarded:
    def __init__(self, values, limit):
        self.values = iter(values); self.limit = limit; self.pulls = 0; self.seen = []
    def __iter__(self):
        return self
    def __next__(self):
        value = next(self.values)          # a finite feed may simply end
        if self.pulls >= self.limit:
            raise PullExceeded()
        self.pulls += 1
        self.seen.append(value)
        return value
from itertools import count
cases = [("[4, 1, 3, 2, 5, 9]", [4, 1, 3, 2, 5, 9], 2, 5, [(1, 3), (2, 5)]),
         ("[1, 2, 3]", [1, 2, 3], 0, 0, []),
         ("an endless feed 7, 8, 9, ...", count(7), 5, 6, [(7, 8), (8, 9), (9, 10), (10, 11), (11, 12)]),
         ("[6, 6, 2]", [6, 6, 2], 3, 3, [])]
for name, values, k, limit, expected in cases:
    readings = Guarded(values, limit)
    before = _frame_count()
    try:
        answer = rising_preview(readings, k)
    except PullExceeded:
        raise AssertionError(f"On {name} with k={k} you asked for more than {limit} readings. Stop at the k-th rise without asking for another; with k = 0 ask for none.")
    assert answer == expected, f"On {name} with k={k} the preview should be {expected}; got {answer!r}."
    assert readings.pulls == limit, f"On {name} with k={k} exactly {limit} readings are needed; you read {readings.pulls}."
    frames = [_frame(i) for i in range(before, _frame_count())]
    steps = [[o for o in objects if o['kind'] == 'figure'][0]['params']['values'] for objects in frames[:-1] if any(o['kind'] == 'figure' for o in objects)]
    want = [[a, b] for a, b in zip(readings.seen, readings.seen[1:])]
    assert steps == want, f"On {name} with k={k}, show_step should be called once for each neighbouring pair read, in order: {want}. Your step frames show {steps}."
    assert frames, "Call show_preview(result) once at the end."
    last = frames[-1]
    assert any(o['kind'] == 'text' and o['value'] == 'rising pairs returned=' + str(len(answer)) for o in last), f"The last frame should be show_preview(result), reporting {len(answer)} rises."
