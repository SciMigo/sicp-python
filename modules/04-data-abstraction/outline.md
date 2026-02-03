# Data Abstraction — Slide Outline

## Slide 1: Beyond Numbers
- So far: functions operating on numbers
- New question: How do we represent compound data?
- Motivating example: rational number arithmetic — need to track numerator AND denominator

## Slide 2: Constructors and Selectors
- `make_rat(n, d)` — constructor: builds a rational
- `numer(r)`, `denom(r)` — selectors: extract parts
- `add_rat(x, y)` — written using ONLY constructors and selectors
- "The implementation is hidden behind the barrier"

## Slide 3: The Abstraction Barrier
- Diagram: layers of abstraction
- Top: `add_rat`, `mul_rat` (use rationals)
- Middle: `make_rat`, `numer`, `denom` (the interface)
- Bottom: `(n, d)` tuples (the implementation)
- **Checkpoint**: If we change the implementation from tuples to lists, what code needs to change?

## Slide 4: Implementation — It's Just Tuples
- `def make_rat(n, d): return (n, d)`
- `def numer(r): return r[0]`
- But we could also use lists, dictionaries, or even functions!
- The point: users of `add_rat` don't care

## Slide 5: Data Without Data Structures
- Mind-bending: implement pairs using only functions
- `def pair(x, y): def dispatch(m): return x if m == 0 else y; return dispatch`
- `pair(3, 4)(0)` → 3, `pair(3, 4)(1)` → 4
- "Data is just a contract between constructor and selector"

## Slide 6: Layered Abstraction
- Points: `make_point(x, y)`, `x_coord(p)`, `y_coord(p)`
- Segments: `make_segment(p1, p2)`, `start(s)`, `end(s)`
- `midpoint(s)` uses segment selectors, which use point selectors
- Each layer only talks to the layer directly below

## Slide 7: Why Barriers Matter
- Violation: `r[0]` instead of `numer(r)` — works today, breaks tomorrow
- Scenario: we add GCD reduction to `make_rat` → all barrier-respecting code still works
- **Checkpoint**: Write `mul_rat(x, y)` using only `make_rat`, `numer`, `denom`

## Slide 8: The Closure Property
- "Closure" here means: combining things gives you the same kind of thing
- Pairs of pairs → trees, sequences, nested structures
- `(1, (2, (3, None)))` — a linked list from pairs
- Preview: Next we'll explore sequences — lists and their powerful operations

## Slide 9: Summary
- Data abstraction = constructors + selectors + discipline
- Barriers make code flexible, testable, changeable
- Even functions can serve as data (message passing)
- The interface is the contract
