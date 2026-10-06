show_state=lambda *args:None
import random
rng=random.Random(731)
for initial in (0,20,90):
    a=make_account(initial,'key');other=make_account(initial,'key');balance=initial
    saved=a('key','deposit')
    for _ in range(35):
        pw=rng.choice(['key','bad']);op=rng.choice(['deposit','withdraw']);amount=rng.randrange(25)
        if pw!='key':want='Incorrect password'
        elif op=='withdraw' and amount>balance:want='Insufficient funds'
        else:balance+=amount if op=='deposit' else -amount;want=balance
        got=a(pw,op)(amount)
        assert got==want, f'{pw}/{op}/{amount}: expected {want!r}; got {got!r}'
    got=saved(4);balance+=4
    assert got==balance, f'Saved operation expected shared balance {balance}; got {got!r}'
    got=other('key','withdraw')(0)
    assert got==initial, f'Independent account expected {initial}; got {got!r}'
    try:a('key','missing')
    except ValueError:pass
    else:raise AssertionError('Expected ValueError for authorized unknown request; got normal return')
    got=a('key','withdraw')(0)
    assert got==balance, f'Unknown request must preserve {balance}; got {got!r}'

password=''.join(['fresh','-','credential'])
equal_password=''.join(['fresh-','credential'])
a=make_account(9,password)
got=a(equal_password,'deposit')(1)
assert got==10, f'Equal credentials should authorize by value and yield 10; got {got!r}'
