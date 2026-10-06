from scimigo import _frame_count, _frame
# A pair built by the check, so cdr is tested by itself.
theirs = lambda choose: choose('near', 'far')
got = cdr(theirs)
assert got == 'far', f"cdr of a pair holding 'near' and 'far' should be 'far'; got {got!r}."
marker = object()
assert cdr(lambda choose: choose(0, marker)) is marker, "cdr must return the second part itself, whatever kind of object it is."
calls = []
def counting_pair(choose):
    calls.append(choose)
    return choose(1, 2)
cdr(counting_pair)
assert len(calls) == 1 and callable(calls[0]), "cdr should call the pair once, passing it a function of two arguments."
z = cons('north', 'south')
before = _frame_count()
show_pair(z)
figure_values = [o for o in _frame(before) if o['kind'] == 'figure'][0]['params']['values']
assert figure_values == ['north', 'south'], f"The picture of cons('north', 'south') should show ['north', 'south']; it shows {figure_values}."
