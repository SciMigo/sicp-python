# Module 01 review notes

## 2026-10-05: rewrite after review (Claude)

Status: local draft, not published. Replaces the 2026-10-04 conversion.

What changed, and why:

- **Lesson rewritten around SICP 1.3.** The owner asked for the book's content to stay. The
  workshop-credit and minimum-charge examples are gone; the lesson now uses the three sums,
  `summation`, lambda, `integral`, `fixed_point`, `average_damp`, `deriv` and Newton's method.
  2,450 words, 11 executed code blocks, 1 figure.
- **Lab exercises are written from stubs.** The earlier starters were one-line repairs with a
  comment on the line to change. Exercises 1 to 4 are new: `accumulate` (1.32), `compose` (1.42),
  `repeated` (1.43) and a fixed-point call count.
- **The lesson no longer contains lab answers**: it shows `summation`, the lab asks for `accumulate`.
- **Every checklist step is red on the untouched starter**, except the mastery correctness step
  (that starter is correct and over budget). The old `measured_bars` check passed untouched.
- **Hints are written per exercise**; the same three were pasted on four exercises before.
- **Every assert has a message** saying what was expected and what came back.
- **Mastery meter tightened**: subtraction, negation, abs and `.real` no longer shed the count.
- **Estimate lowered** from 100 to 80 minutes (lesson 20–25, lab 45–70), still unmeasured.
- `chapter` is now "SICP §1.3" (it was "1.6", which matched nothing).

Verified in this pass:

- `tools/lessons.py check 01`: ok, 11 blocks, 1 figure.
- `tools/check_lab.py 01`: ok, 5 exercises, 10 solution checks. `lab_src.py check`: up to date.
- Each untouched starter run against each check: 9 of 10 fail, with the message aimed at the
  missing work; the tenth is the mastery correctness check.
- Wrong submissions tried and rejected: term called twice per point, combiner arguments swapped,
  `compose` that calls its functions again for drawing, `repeated` as nested calls, a hand-written
  search loop in `measure`, and the mastery starter with `.real` or `x - 0` conversions.
- Browser smoke (`preview_smoke.mjs --all`, Chromium, Pyodide 0.27.4 from the CDN): all checks
  passed. Looked at the first exercise's screenshot and the lesson figure.
- Lesson at 390 px, dark: no horizontal overflow (scrollWidth 390).

Known limits:

- The figure's bracket label sits on the bracket line (straightedge 0.8.0 `array_state`); legible.
- No `concepts` tags: the course has no `concepts.yaml` yet.
- The reference link is relative (`../../reading/…`) and must be rewritten at publication.
- Time estimate is an author estimate.
