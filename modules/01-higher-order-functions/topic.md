# Higher-order functions: plan and notes

Follows SICP section 1.3 (Formulating Abstractions with Higher-Order Procedures), with the book's
examples rewritten in Python. The book's own text (`reading/01-higher-order-functions.html`) is a
reference, linked from the end of the lesson.

## Teaching plan

Problem: three sums (integers 1..10 = 55, cubes 1..10 = 3025, 8·pi_sum(1, 1000) = 3.1395…).
Naive approach: three copied loops. Idea: `summation(term, a, next, b)` with the running-total
invariant. Then lambda, `integral`, `fixed_point` (cos, and why y → 2/y oscillates),
`average_damp`, `deriv`, `newtons_method`, order of composition, counted calls.
Teaser: one sort, three orderings (the `key` argument). Left out on purpose: half-interval
method and `let`; the lesson says so.

Lesson code is not lab code: the lesson shows `summation`; the lab asks for `accumulate`
(exercise 1.32). The lesson explains composition order and repetition without writing `compose`
or `repeated` (exercises 1.42 and 1.43), which are lab exercises.

## Lab

1. Build `accumulate(combiner, null_value, term, a, next, b)`: SICP 1.32, iterative, combiner(result, term).
2. Trace `compose(f, g)`: SICP 1.42; predict compose(square, inc)(6) = 49.
3. Implement `repeated(f, n)`: SICP 1.43; must survive n = 3000, so a loop, not nested calls.
4. Measure `measure(f, guess, tolerance)`: count the calls the supplied `fixed_point` makes.
5. Mastery `make_service(settings)`: fixed scale-and-offset records, many later readings, with a
   setup budget and a per-reading budget. The prompt names no technique.

Starters are stubs: each runs, draws one frame and fails every check except the mastery
correctness check (the mastery starter is correct but over budget).

## Numbers and where they are asserted

All in lesson code blocks: 55, 3025, 3.139592655589782; integral of x³ on [0, 1] with dx 0.01 and
0.001; fixed point of cos 0.7390822985224024; average_damp(square)(10) = 55; deriv(cube)(5) ≈ 75;
call counts 10/100/1000 with error 0.125·dx²; 29 calls for cos and 4 for the damped square root
at tolerance 1e-5 from 1.0. The error column is a measurement on x³, and the lesson says so.
Float results are compared with tolerances; call counts are exact in CPython. Lab checks never
hard-code a call count: they recount in the same runtime, because Pyodide's libm may differ from
CPython's in the last bit.

## Check design and limits

- Fold: a list-building combiner checks argument order and one call per point; an empty range must
  return `null_value` itself and call nothing.
- Frames are counted from a baseline and compared with the true prefix on every frame.
- Measure: the check swaps in a `fixed_point` that wastes one call per step, so a count derived
  from the tolerance, or taken from the learner's own loop, fails.
- Mastery: arithmetic is metered through an int subclass whose +, -, *, negation, abs and `.real`
  all stay metered; `int`/`float` are refused by an AST check; a BaseException stops an
  over-budget run. Still open: `//`, `**`, bit operations, `operator.index`, `round`. This is
  feedback, not secure grading.
- `repeated` built from 3000 nested calls raises RecursionError in CPython; the check reports it
  as an assertion. Not verified with a wrong submission in Pyodide.

## Sources

- SICP 2nd edition, section 1.3 and exercises 1.32, 1.42, 1.43 (`reference/1.3-higher-order-procedures.md`).
- Python 3 documentation, checked 2026-10-04: sorting how-to, key functions (called once per
  item); data model, `function.__closure__`.
