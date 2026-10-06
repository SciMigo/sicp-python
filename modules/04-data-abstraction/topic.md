# Data abstraction: plan and notes

Follows SICP §§2.1.1–2.1.4 with the book's examples in Python. The book's own text
(`reading/04-data-abstraction.html`) is a reference, linked from the end of the lesson.

## Teaching plan

Rational arithmetic by wishful thinking; a tuple representation and why tuple equality is the
wrong equality; reduction for positive arguments; the abstraction barrier and a swapped
(dictionary) representation; the law a constructor and its selectors must keep (invariant
call-out); points and segments as two layers; a pair made of a dispatching function; reducing at
construction versus at selection; interval arithmetic and the dependence problem. Teaser: a map
renderer fed pixels or metres.

Lesson code is not lab code. The lesson reduces only positive fractions; the lab asks for the
signed constructor (exercise 2.1). The lesson builds the numeric-dispatch pair; the lab asks for
the chooser pair (2.4). The lesson states the dependence problem in general; the lab's mastery is
the parallel-resistor case, which the lesson does not mention.

## Lab

1. Build `make_rat(n, d)`: exercise 2.1, with one frame per Euclid step and one for the stored fraction.
2. Trace `make_rect`, `rect_width`, `rect_height`, `report`: exercise 2.3. The learner writes a
   corner representation and a client; checks swap the point storage under the rectangle and
   hand the client a rectangle stored as centre and half-sides.
3. Implement `cons` and `cdr`: exercise 2.4, with `car` supplied as in the book. Small by nature.
4. Measure `measure(strategy, n, d, k)`: the strategies take the gcd function as an argument, so
   counting is the wrapper from module 1 and needs no global rebinding.
5. Mastery `parallel(r1, r2)`: the starter evaluates R1·R2/(R1+R2), which is sound and too wide.
   The prompt gives the 1% tightness budget and names no technique. Two correct answers exist:
   1/(1/R1 + 1/R2), and the endpoints directly (the formula is increasing in both resistances).

Starters are stubs that run and draw; 10 of 11 checks are red on them. The eleventh is the
mastery soundness check, which the starter passes by design.

## Numbers and where they are asserted

Lesson blocks: 5/6, 1/6, 6/9, (2, 3), (0, 1), midpoint (3.0, 5.0), interval product (-10, 15).
Lab checks: gcd calls 1 (eager) and 2k (lazy), recounted by the check itself. Mastery question 4:
6.8 ± 10% with 4.7 ± 5% gives 2.2010 to 3.4874 by the starter's formula and 2.5816 to 2.9733 in
truth (computed 2026-10-06; these are the book's exercise 2.14 resistors).

## Check design and limits

- Fractions: 53 signed cases; the `fractions` module is refused by an AST check, because it would
  do the exercise. `math.gcd` is allowed for the answer but the Euclid frames are still required.
- Rectangles and intervals: the check rebinds the layer below (points, intervals) to a dictionary
  form, so code that indexes through the barrier fails with a message.
- Measure: the check wraps the supplied `gcd` itself, so a count worked out from k, or a wrapper
  that does not delegate to `gcd`, fails.
- Mastery: soundness is checked against the exact range on 29 interval pairs in two storages;
  tightness allows 1%. Random widths are up to 6 ohms on resistances from 0.5 to 66.
- These checks are feedback, not secure grading.

## Sources

- SICP 2nd edition §2.1 and exercises 2.1, 2.3, 2.4, 2.13–2.16 (`reference/2.1-data-abstraction.md`).
- CPython `Lib/fractions.py`, `Fraction.__new__`, read 2026-10-06 in Python 3.12.3:
  `g = math.gcd(numerator, denominator)`, negated when the denominator is negative, then both
  parts are floor-divided by it.
