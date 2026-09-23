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

Nine modules, 29 exercises: three per module, plus a fourth **Challenge**
exercise in 05 (a lazy pipeline over an infinite sequence) and 06 (every path,
not just the first).

## Technique checks

Some tests check *how* an answer computes, because an exercise that exists to
practise a technique can otherwise be passed without it. Each is an ordinary,
visible test, named for what it checks:

| Exercise | Check | How |
|---|---|---|
| 03 ex3 | `f_rec` follows the definition | it must call itself |
| 03 ex3 | `f_iter` is an iterative process | `f_rec` is replaced by one that raises, and `f_iter(3000)` must not exhaust the stack |
| 05 ex3 | `my_map` / `my_filter` are built from `accumulate` | `accumulate` is wrapped to count calls |
| 05 ex4 | `naturals`, `map_lazy`, `filter_lazy` are generators; `take` pulls exactly `n` | type check, and a source that records what was pulled |
| 06 ex3, ex4 | the tree abstraction barrier holds | the tree ADT is swapped for a dict representation and the answer must still work |

A test that rebinds a name (the wrapper, the swapped ADT) restores it in a
`finally`. The browser gives every test a fresh namespace, but
`check_labs.py` and the publish-time check share one across a lab's tests, and a
test must not change what the next one sees.

## Checking the labs

`modules/check_labs.py` runs every reference solution against that exercise's
own tests. Stdlib only, no dependencies, no network:

```bash
python3 modules/check_labs.py
```

Solutions come in three shapes, and the distinction matters when reading the
output of this or any other checker:

- Implement/extend exercises are answered in **Python**. They must run and pass.
- Predict/trace exercises are answered in **prose** — "it prints 2, because the
  instance attribute shadows the class attribute". Correct content; reported as
  prose and skipped.
- **Broken code** is the one to catch: an answer that opens a block or returns
  a value, so it was written to run, and does not parse. A learner who pastes
  it gets a `SyntaxError`.

Classifying by "does it compile" alone puts broken code in the prose bucket and
calls the lab clean. That is exactly what happened: two solutions shipped
unrunnable and the checker reported 0 failures for months.

Current state: **18 solutions pass, 0 fail, 11 answered in prose.**

Separately, `01/ex3` and `08/ex3` ship starter code that raises until it is
filled in — `pass` stubs plus demo calls at the bottom. Also by design.

## Provenance

Every `lab.json` was extracted verbatim from the file published for that
module, checksum-verified on 2026-09-22. Seven still match exactly. Two carry
changes that have not been published yet:

- `02-environment-diagrams` — the unrunnable solution above.
- `04-data-abstraction` — its lab title, which used to carry a LaTeX artifact.

The course is a mix of two generation runs:

| Module | Published |
|---|---|
| 01, 02, 03 | 2026-08-25 |
| 04–09 | 2026-02-16 / 02-17 |

Modules 01–03 come from a later regeneration; 04–09 are from the original run.

## Unrunnable reference solutions

Five reference solutions could not run. A learner who revealed one and re-ran
the tests saw red, or pasted it and got a `SyntaxError`.

Three failed their own tests, and are **published**:

| Module | Exercise | Was |
|---|---|---|
| 04-data-abstraction | `ex3_extend_sub_rat_survives_repr_swap` | 3/3 failed — `_normalize` / `install_tuple_repr` undefined |
| 08-oop | `ex1_predict_fee_shadowing` | 2/2 failed — comments only, defined no `ch` |
| 08-oop | `ex3_implement_extend_equ_generic` | 6/6 failed — body was a placeholder comment |

Their cause: the `solution` held only the **fragment** the learner fills, while
a checker — or anyone pasting it into the editor — runs it standalone. Each is
now a complete runnable program, the shape the other modules use.

Two more did not parse at all, and the checker had been calling them prose:

| Module | Exercise | Was |
|---|---|---|
| 02-environment-diagrams | `ex3_extend_accumulator_closure` | working code with an explanatory sentence on the last line and no `#` |
| 06-trees (then an unpublished rewrite; now `ex4_challenge_all_paths`) | `ex3_extend_all_paths` | a markdown answer — prose, then the code inside a fence |

In every case `prompt_md`, `starter_code` and `tests` were left alone, so
nothing changed about what the learner is asked or graded on.

## How these files are used today

Historically the pipeline published the lab it generated into its own build
output, and nothing read this file except a check for whether it exists — so an
edit here reached nobody until someone copied it back by hand.

Since 2026-09-22 publication reads `lab.json` directly, validated, with the
lab page re-rendered from it, so these files are the source of truth and an
edit here ships on the next deploy. A lab that fails that validation is not
published and the live copy stays.

Either way, **a change in this repo does not reach learners until someone runs
a deploy.** Merging is not publishing.

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
| 06 | 2.24, 2.25, 2.26 | 2.24, 2.26, 2.28 |
| 07 | 3.1, 3.2, 3.3 | 3.3 |
| 08 | 2.73, 2.74, 2.75 | none |
| 09 | 4.1, 4.2, 4.3 | none |

Treat `lab.json` as the truth about what the course teaches.
