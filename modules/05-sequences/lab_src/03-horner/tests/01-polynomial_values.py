import random
saved=show_horner;show_horner=lambda *args:None
try:
    rng=random.Random(534)
    cases=[(3,[2,-1,3,0,1]),(0,[8,2,9]),(-2,[1,0,3]),(5,[]),(7,[0]),(2,[9])]
    cases += [(rng.randrange(-3,4),[rng.randrange(-5,6) for _ in range(rng.randrange(12))]) for _ in range(30)]
    for x,coefficients in cases:
        before=list(coefficients);expected=sum(c*x**i for i,c in enumerate(coefficients))
        assert horner(x,coefficients)==expected,"Coefficients run from constant term upward, including missing powers represented by zero."
        assert coefficients==before,"Do not reverse or overwrite the caller's list."
finally:show_horner=saved
