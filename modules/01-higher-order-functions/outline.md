# Higher-Order Functions — Slide Outline

## Slide 1: The Repetition Problem
- Show `sum_naturals(n)`, `sum_cubes(n)`, `pi_sum(n)` — three functions with identical structure
- "What's the same? What's different?"
- Motivate: Can we capture this pattern?

## Slide 2: Functions as Arguments
- Define `summation(n, term)` — the general pattern
- `sum_naturals = summation(n, lambda k: k)`
- `sum_cubes = summation(n, lambda k: k**3)`
- **Checkpoint**: Predict `summation(4, lambda k: k*k)` → 30

## Slide 3: The Power of Lambda
- Lambda expressions: anonymous, inline functions
- `square = lambda x: x * x` vs `def square(x): return x * x`
- When to use lambda vs def (short expressions vs named operations)

## Slide 4: Functions as Return Values
- `make_adder(n)` returns a function that adds `n`
- `add_three = make_adder(3)` → `add_three(4)` → 7
- "The returned function remembers `n` — that's a closure"

## Slide 5: Closures in Action
- Environment diagram showing `make_adder` frame, inner function, and lookup chain
- Trace `make_adder(3)(4)` step by step
- "The function carries its birth environment with it"

## Slide 6: Function Composition
- `compose(f, g)` returns `lambda x: f(g(x))`
- Example: `compose(square, make_adder(1))(5)` → 36
- Build up: applying transformations in sequence

## Slide 7: Newton's Method
- Real-world application of higher-order functions
- `improve(update, close_enough)` — pass the strategy as a function
- Find sqrt(2): `find_root(f, df)` using `newton_update`
- **Checkpoint**: Edit `f = lambda x: x*x - 2` to find cube root of 27

## Slide 8: Currying
- `curry(f)` transforms `f(x, y)` into `f(x)(y)`
- `curried_pow = curry(pow)` → `curried_pow(2)(10)` → 1024
- Connection to partial application and function factories

## Slide 9: The Big Picture
- Functions are the fundamental unit of abstraction
- Summary: functions as args → generalization, as return values → customization
- Preview: Next we'll explore how Python tracks all these names and values (environments)
