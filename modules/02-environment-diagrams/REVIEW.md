# Module 02 review — 2026-10-05

Status: checked local draft, free; not published.

## Scope and changes

Independent 1,945-word lesson with six executable Python blocks and two semantic diagrams. Explains definition scope versus caller scope, shadowing, Python local-before-assignment, closure cells, shared nonlocal state and independent factory calls. The dictionary-frame lookup model is explicitly incomplete and its cost is not attributed to CPython variable access. Original reading remains optional background; old lab and slide outline are archived.

Five exercises: nearest-binding lookup, fresh call frames, shared update/read/reset operations, measured membership probes, and distinct deferred panel callbacks. Each has tailored progressive hints. Mastery reasoning stays hidden until an attempt or explicit request.

## Checks

- Six lesson blocks and two figures pass. Syntax highlighting retained.
- Ten solution checks pass; all five starters execute and draw but fail substantive checks.
- Seeded varied cases cover shadowing, missing names, None/False/zero values, nonadjacent parent links, input preservation, fresh parameter tables, interleaved independent services, actual counted membership probes, deferred callbacks, duplicates and input-list mutation.
- Chrome/Pyodide smoke passes all five exercises, frame playback, question completion, mastery gating, recap, embedded sizing and host-provided lab/example retrieval.
- Browser execution used the real Pyodide 0.27.4 distribution cached locally because the browser CDN download stalled. The external-CDN startup path did not pass today. A localhost-only runtime=local option is available for reproducible review; cache files are ignored and not published.
- Lesson layout checked at 1366px and 390px, light and dark. No horizontal overflow. Body/callout contrast ranges from 11.76 to 16.74.
- Inspected both lesson figures, all sixteen browser smoke screenshots and the phone starter. Visual review changed the first demo to show a parent traversal and replaced a misleading empty parent with explicit omitted-binding notation.

Generated evidence: output/review/02-environment-diagrams/.

## Limits

Author time estimate is unmeasured: lesson 25–35 minutes, lab 60–85 minutes (85–120 total). Frame inputs must be finite, acyclic and have valid parents. Model excludes builtins and Python's scope classification; the lesson explains that boundary. Checks are educational feedback, not a secure anti-cheating system. Optional legacy reading is not fully re-audited. Live publication and legacy slide withdrawal remain separate pending work.

# Review pass — 2026-10-05 (Claude), after the external review of PR #6

Status: local draft on `claude/sicp-review-fixes`; not committed by this pass, not published.

## What changed

- Lesson rewritten around SICP 3.2's own examples in Python: square / sum_of_squares / f with f(5) = 136 and its four frames, the frame / environment / function-value rules, make_withdraw with W1 and W2, and sqrt with internal definitions. The lookup invariant, the UnboundLocalError boundary and the probe count are kept. Three predict blocks added. The lesson no longer discusses saved callbacks in a loop, so the mastery problem is not previewed; the teaser is a shared ticket counter, left unsolved. "Not an endorsed university offering" moved out of the prose (module.json carries the attribution).
- Lab: every Build / Trace / Implement / Measure starter is now a stub, with no comment marking a fix. Exercise 1 is define + assign (the lesson shows only lookup); exercise 2 appends a call's frame and chooses its parent; exercise 3 is make_account with withdraw and deposit (the lesson shows the one-function make_withdraw); exercise 4 writes the counted lookup from nothing (the lesson measures with an instrumented dict instead of a counter); exercise 5 keeps the badges problem with new hints and a fourth question that asks for the supplied version's output on prefixes 4 and 9.
- Every assert in every check has a message. Hints are written per exercise.
- module.json: `chapter` removed (1.7 matched nothing; no tool reads the field), estimate 70 minutes, attribution names SICP 3.2.
- Figures: binding-row highlights replaced by frame highlights and `frame_padding` 16, which avoids the band that covered frame titles (a straightedge 0.8.0 geometry issue, noted in topic.md).

## Verified in this pass

- `tools/lessons.py check 02`: ok, 8 blocks, 3 figures.
- `tools/check_lab.py 02`: ok, 5 exercises, 11 solution checks.
- `lab_src.py check`: lab.json up to date.
- Untouched starters: all 11 checks fail, each with the message aimed at the missing behaviour.
- Thirteen wrong or lazy submissions run against the checks (listed in topic.md); twelve are rejected by at least one check, and the default-argument mastery solution passes as intended.
- Browser smoke (`preview_smoke.mjs 02-environment-diagrams --all`, real Pyodide CDN): all checks passed; screenshots of exercises 1 and 2 inspected.
- Lesson built and screenshotted at 1100 px light and 390 px dark; `scrollWidth` is 390 on the phone viewport; all three figures inspected.

## Not done

- The reference-reading link is still the relative `../../reading/02-environment-diagrams.html`; the published URL depends on routing that does not exist yet.
- No `concepts` tags: the course has no concepts.yaml.
- Time estimate is unmeasured.
