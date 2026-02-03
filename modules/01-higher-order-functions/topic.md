# Higher-Order Functions

## SICP Reference
- Chapter 1.3: Formulating Abstractions with Higher-Order Procedures

## Core Concepts
- Functions as first-class values in Python
- Functions as arguments (passing behavior)
- Functions as return values (closures, factories)
- Lambda expressions
- Function composition and currying
- The summation abstraction pattern

## Key Examples (Python)
1. **Summation abstraction**: `summation(n, term)` — extract the pattern from `sum_naturals`, `sum_cubes`, `pi_sum`
2. **make_adder**: Return a function that adds `n` — introduces closures
3. **compose**: `compose(f, g)` returns `lambda x: f(g(x))`
4. **Newton's method**: Higher-order `improve` with `close_enough` — real-world application

## Reference Files
- `1.3-higher-order-procedures.md`

## Speaker Persona
- Professor Dana: Clear, methodical. Uses "Notice how..." and "What do you think this will print?"
- Alex (student): Reasons step by step, sometimes surprised by closure behavior
