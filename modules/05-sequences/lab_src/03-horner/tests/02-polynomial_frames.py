from scimigo import _frame_count, _frame
coefficients = [4, 0, -2, 1]
x = 2
before = _frame_count()
answer = horner(x, coefficients)
assert answer == 4, f"horner(2, [4, 0, -2, 1]) is 4 + 0 - 8 + 8 = 4; got {answer!r}."
steps = []
for index in range(before, _frame_count()):
    figures = [o for o in _frame(index) if o['kind'] == 'figure']
    if figures:
        steps.append(figures[0]['params']['values'])
assert len(steps) == len(coefficients), f"Four coefficients need four show_horner frames; recorded {len(steps)}."
result = 0
for offset, index in enumerate(range(len(coefficients) - 1, -1, -1)):
    result = coefficients[index] + x * result
    want = [index, coefficients[index], result]
    assert steps[offset] == want, f"Step {offset + 1} should show index, coefficient, result = {want}; it shows {steps[offset]}. Start from the highest coefficient."
