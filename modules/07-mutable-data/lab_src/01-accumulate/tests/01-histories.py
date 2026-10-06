show_state=lambda *args:None
import random
rng=random.Random(713)
for initial in (-9,0,13):
    a=make_accumulator(initial);b=make_accumulator(initial);want=initial
    for value in [rng.randint(-10,10) for _ in range(15)]:
        want+=value;got=a(value)
        assert got==want, f'After adding {value}, expected retained total {want}; got {got!r}'
    got=b(0)
    assert got==initial, f'Independent accumulator expected {initial}; got {got!r}'
seen=[]
def worker(x):seen.append(x);return ('answer',x)
m=make_monitored(worker);other=make_monitored(worker)
for i in (3,-2,7):
    got=m(i)
    assert got==('answer',i), f'Expected delegated result {("answer",i)!r}; got {got!r}'
got=m('how-many-calls?')
assert got==3 and seen==[3,-2,7], f'Expected 3 calls and [3,-2,7]; got count {got!r}, arguments {seen!r}'
assert other('how-many-calls?')==0, f'Expected independent count 0; got {other("how-many-calls?")!r}'
got=m('reset-count');count=m('how-many-calls?')
assert (got,count)==(0,0), f'Expected reset return and count (0,0); got {(got,count)!r}'
def fails(x):raise ValueError('worker failed')
m=make_monitored(fails)
try:m(8)
except ValueError:pass
else:raise AssertionError('Expected worker ValueError; got normal return')
got=m('how-many-calls?')
assert got==1, f'Expected failed attempt to count once; got {got!r}'
