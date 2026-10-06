from math import gcd
import random
saved=show_rat;show_rat=lambda *args:None
try:
    rng=random.Random(204)
    cases=[(0,7),(0,-7),(-8,-12),(8,-12),(-8,12),(27,9)]+[(rng.randrange(-150,151),rng.choice([i for i in range(-30,31) if i])) for _ in range(45)]
    for n,d in cases:
        result=make_rat(n,d);a,b=numer(result),denom(result)
        assert isinstance(a,int) and isinstance(b,int),"Keep selected numerator and denominator as integers."
        assert a*d==n*b,"Selected parts must preserve the original ratio."
        assert b>0,"Keep the denominator positive; put any negative sign on the numerator."
        assert gcd(a,b)==1,"Divide out all common factors."
    rejected=False
    try:make_rat(5,0)
    except ZeroDivisionError:rejected=True
    assert rejected,"A zero denominator must raise ZeroDivisionError."
finally:show_rat=saved
