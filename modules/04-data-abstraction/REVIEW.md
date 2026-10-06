# Module 04 review notes

## 2026-10-06: lab rewrite after review (Claude)

Status: local draft, not published. Follows the conversion of the same day.

The lesson was sound and is mostly unchanged. The lab was the problem.

What changed, and why:

- **Every exercise drew one static frame.** `make_rat` now records each Euclid step; `report`
  records each read through the barrier; the mastery draws the two resistors and the result on
  one scale.
- **Two exercises were a couple of minutes each.** The rectangle exercise was `w*h` and
  `2*(w+h)`; it is now exercise 2.3 proper, with a representation to write and a second one to
  survive. `cons` was one expression inside a supplied skeleton; the learner now writes `cons`
  and `cdr`, with `car` supplied as in the book.
- **Measure needed a mechanism no lesson teaches.** It rebound a module-level `gcd` from inside a
  function. The strategies now take the gcd function as an argument.
- **Intervals had a lesson section and no exercise**, while the mastery was a sum and a running
  maximum with its constraint in bold. The mastery is now the parallel-resistor problem.
- `fractions.Fraction` passed the first exercise; its import is now refused.
- Lesson: added the invariant call-out and two predict blocks, replaced the second figure (a row
  of coordinate strings) with the three layers, added "In real software", and brought "Check
  yourself" to three questions.

Verified in this pass:

- `tools/lessons.py check 04`: ok, 7 blocks, 2 figures. `tools/check_lab.py 04`: ok, 5 exercises,
  11 solution checks. `lab_src.py check`: up to date.
- Untouched starters against each check: 10 of 11 red, each with a message about the missing work.
- 21 wrong, lazy and alternative submissions: every wrong one fails at least one check; the two
  alternative correct ones (a rectangle stored as two side lengths, the mastery by endpoints) pass.
- Browser smoke (`preview_smoke.mjs --all`, Chromium, Pyodide 0.27.4 from the CDN): all checks passed.
- Lesson at 390 px, dark: no horizontal overflow. Looked at both lesson figures and the mastery screenshot.

Estimate: 80 minutes, unchanged in total but now matched by the work (lesson 20–25, lab about 60).
Unmeasured.

Known limits:

- Exercise 3 is small; that is the size of exercise 2.4.
- No `concepts` tags: the course has no `concepts.yaml` yet.
- The reference link is relative and is rewritten by the publish script.
- The licence sentence at the end of the lesson is the earlier draft's; whether lessons carry it
  is an owner decision for all modules.
