# Recursive functions: author plan

Follows SICP section 1.2 ("Procedures and the Processes They Generate") in Python, by owner decision of 2026-10-05: the lesson keeps the book's own examples, in original prose; the SICP reading is linked as optional background only.

## Lesson

Three rounds, one question each.

1. What is still waiting? `factorial` as a linear recursive process, `factorial_loop` as a linear iterative one, with the loop invariant. Python has no tail-call optimization, so SICP's "iterative process from a recursive procedure" needs a loop here.
2. What smaller input can I trust? Euclid's `gcd` (shrink by a remainder), a mirrored window (shrink from both ends), a nested package (shrink to a child). The last two are described in prose and figures only, because the lab asks for them.
3. Which work repeats? `fib` as tree recursion with its exact call count, `fib_loop`, `count_change`, memoization (`fib_memo`; SICP places it in exercise 3.27), orders of growth, `fast_expt`.

Numbers, all asserted in lesson blocks: factorial(6) = 720; gcd(206, 40) = 2 in 4 remainders; fib calls = 2·fib(n+1) − 1 (15, 177, 21,891, 2,692,537 for n = 5, 10, 20, 30); 2·fib(91) − 1 = 9,320,093,220,751,060,617; count_change(100) = 292 ways in 15,499 calls with coins ordered (1, 5, 10, 25, 50) and the "one fewer kind" branch first; fast_expt multiplications 5, 6, 8, 9, 15 for n = 10, 20, 30, 100, 1000. The bound 2·log2(n) + 2 was checked for every n below 100,000.

Model for the growth table: one step per call or loop pass, one unit of space per waiting call or state variable, unit-cost arithmetic. The lesson says that Python integers grow.

Not covered from 1.2: Ackermann's function, the fixed-point view of the golden ratio, Lamé's theorem, primality testing (Fermat test, Miller–Rabin). The teaser (guess a number with higher/lower answers) is a halving argument and is not the mastery problem.

## Lab

Lab functions differ from every function the lesson prints.

| # | Exercise | Kind | What the learner writes |
|---|---|---|---|
| 1 | `power` | Round 1 | linear recursive b^n, drawing the stack of waiting exponents |
| 2 | `mirrored` | Round 2 | two-boundary window recursion, no slicing |
| 3 | `nested_total` | Round 2 | sum of a nested list, children before parent |
| 4 | `route_trace` | Round 3, trace | routes with jumps 1 or 3; predict the 11 calls for n = 4 |
| 5 | `memo_routes` | Round 3, implement | each positive state expanded once per call |
| 6 | `measure_routes` | Round 3, measure | count real `transition` calls of a naive and a cached solver |
| 7 | `packing` | Mastery | ordered plans modulo m for n up to 6,000 within n·k additions |

Starters for 1–4 are stubs that run, draw and fail; they carry no comment that states the fix. Starters for 5 and 7 are correct but wasteful programs, which is the task. Seven exercises is two more than the usual five; the owner asked for more beginner practice on this module.

Operation model: `transition(k)` calls for state expansions; `combine(a, b, m)` calls for mastery additions. No wall-clock grading. Budget guards raise a BaseException subclass and the check turns it into an AssertionError.

Mastery tell: the largest input is far deeper than Python's call stack, and the same amounts recur. The prompt, hints and questions do not name the technique.

## Check limits

- Checks are feedback, not secure grading. A learner can fake `power`'s frames with loops, but then `power_values` fails because it watches the recursive calls; each shortcut I tried fails at least one check.
- `mirrored` receives a list subclass that rejects slices; `list(items)` would still copy it.
- The mastery budget check relies on RecursionError for a memoized recursion at n = 6,000. CPython's default limit is 1,000. Pyodide sets its own limit, which I did not measure, so a memoized recursive solution might pass in the browser. It would still meet the addition budget.

## Sources

SICP 2nd edition, section 1.2 (reference/1.2-procedures-and-processes.md), for the examples and their order. Python recursion limit: https://docs.python.org/3/library/sys.html#sys.getrecursionlimit, checked 2026-10-05; `sys.getrecursionlimit()` returned 1000 on CPython 3.12 here.

## Oral anchors

What differs between two Θ(n)-step factorial processes; why `count_change` does not count orderings; what memoization improves and what it leaves at depth n.
