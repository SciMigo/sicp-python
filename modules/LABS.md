# Lab content

Each module carries a `lab.json`: the full lab a learner works through — prompt,
starter code, assert-based tests, hints and a reference solution.

Until 2026-09-22 none of this was in the repo. The labs were produced by the
course generation pipeline and kept only as build output and as published
files, so `module.json` — which lists nothing but SICP exercise numbers — was
all the lab content this repo held. They are source now.

## Schema (`lab_v1`)

```
schema_version, lab_spec_id, title, description, runtime
exercises[]
  exercise_id     stable slug
  title
  slide_anchor    the deck slide this exercise follows — deck-specific
  prompt_md       markdown shown to the learner
  starter_code    what the editor is pre-filled with
  tests[]         {name, code} — plain asserts, run in Pyodide
  hints[]         revealed one at a time
  solution        reference answer; PROSE for predict/trace exercises,
                  Python for implement/extend ones
```

Nine modules, three exercises each, 27 total.

## Checking the labs

`modules/check_labs.py` runs every reference solution against that exercise's
own tests. Stdlib only, no dependencies, no network:

```bash
python3 modules/check_labs.py
```

Solutions come in two shapes, and the distinction matters when reading the
output of this or any other checker:

- Implement/extend exercises are answered in **Python**. They must run and pass.
- Predict/trace exercises are answered in **prose** — "it prints 2, because the
  instance attribute shadows the class attribute". That is correct content, so
  `check_labs.py` reports it as prose and skips it. A checker that assumes every
  solution is code will report all 13 as syntax errors; they are not defects.

Separately, `01/ex3` and `08/ex3` ship starter code that raises until it is
filled in — `pass` stubs plus demo calls at the bottom. Also by design.
Current state: **14 solutions pass, 3 fail, 13 answered in prose.**

## Provenance

Every `lab.json` was extracted verbatim from the file published for that
module, checksum-verified on 2026-09-22 — all nine match exactly. The course
turns out to be a mix of two generation runs:

| Module | Published |
|---|---|
| 01, 02, 03 | 2026-08-25 |
| 04–09 | 2026-02-16 / 02-17 |

Modules 01–03 come from a later regeneration; 04–09 are from the original run.

## Three reference solutions fail their own tests

A learner who reveals the solution and re-runs the tests sees red. This is
true of the published labs as well as of the files here:

| Module | Exercise | Failure |
|---|---|---|
| 04-data-abstraction | `ex3_extend_sub_rat_survives_repr_swap` | 3/3 — `_normalize` / `install_tuple_repr` undefined |
| 08-oop | `ex1_predict_fee_shadowing` | 2/2 — solution is comments only, defines no `ch` |
| 08-oop | `ex3_implement_extend_equ_generic` | 6/6 — body is the placeholder `# Same code as starter up to install_equ_package...` |

One root cause: the `solution` holds only the **fragment** the learner fills,
while a checker — or anyone pasting it into the editor — runs it standalone.
The six passing modules ship complete, runnable solutions.
## `06-trees` has an unpublished rewrite

`lab.remake-2026-08-31.json` is a later re-authoring of the trees lab that was
never published. It is kept because it is the better lab on the merits: it
covers SICP 2.24/2.25/2.26, exactly what `module.json` declares, where the
published lab substitutes 2.28.

**It is not a drop-in replacement.** Its `slide_anchor` values point at the
rebuilt trees deck, which is also unpublished — the deck learners see is still
the February one. Shipping the lab without the deck would anchor exercises to
slides the learner never sees. Promoting it means publishing deck and lab
together.

## How these files are used today

`lab.json` is **not yet wired into publication**. The pipeline still publishes
the lab it generates into its own build output; nothing reads this file except
a check for whether it exists. So these files are the reviewable record and the
recovery source, and making them the thing that gets published is a separate
change on the pipeline side.

The practical consequence: edits here do not reach learners until the labs are
regenerated or republished.

## `module.json` → `lab.exercises` is a hint, not a spec

That list is handed to the generator as prompt context; the model then authors
what it likes. The two drifted badly — declared numbers absent from the lab
that shipped:

| Module | Declared | Actually covered |
|---|---|---|
| 01 | 1.29, 1.31, 1.34, 1.42, 1.43 | 1.34, 1.42, 1.43 |
| 02 | 1.35, 1.36 | none |
| 03 | 1.11, 1.12, 1.13 | 1.11, 1.12 |
| 04 | 2.1, 2.2, 2.3 | 2.1 |
| 05 | 2.17, 2.18, 2.19 | none |
| 06 | 2.24, 2.25, 2.26 | 2.28 (the unpublished rewrite covers all three) |
| 07 | 3.1, 3.2, 3.3 | 3.3 |
| 08 | 2.73, 2.74, 2.75 | none |
| 09 | 4.1, 4.2, 4.3 | none |

Treat `lab.json` as the truth about what the course teaches.
