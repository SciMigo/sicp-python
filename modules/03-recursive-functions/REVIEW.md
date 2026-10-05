# Module 03 review — 2026-10-05

Status: checked local draft, free; not published.

## Scope and changes

Independent Expanded three-round lesson with six executable Python blocks and four semantic figures. Teaches termination and decreasing measures, pending calls versus lexical parents, correctness by induction, loop invariants, repeated subproblems, memoization and bottom-up computation. Python does not eliminate tail calls; storing two integers is not a claim of constant bit space. Original reading remains optional background; old lab and slide outline are archived.

Seven exercises (adding mirrored sequences and nested-container totals): recursive sum with actual stack snapshots, postorder trace, memoized routes, measured transition calls, and ordered batch packing with caller-supplied sizes and modular arithmetic. Mastery names no technique and gates reasoning questions behind an attempt or explicit request.

## Checks

- Six lesson blocks and four figures pass. Syntax highlighting retained.
- Fourteen solution checks pass; all seven starters execute and draw but fail substantive checks.
- Varied inputs check recursive calls, caller-stack restoration, exact completion order, fresh memo state, actual counted transitions, counter restoration after exceptions, ordered versus unordered plans, input preservation and modular residues. Budget guards stop runaway attempts promptly and report ordinary check failures.
- Memo checks reach length 200; mastery reaches 6,000 with a bound of n times the number of allowed sizes. Operation counts exclude base cases where explicitly stated, and never grade wall-clock speed.
- Chrome/Pyodide smoke passes all seven exercises, frame playback, question completion, mastery gating, recap, embedded sizing and host-provided lab/example retrieval. All twenty-two screenshots inspected.
- Browser execution used real Pyodide 0.27.4 cached locally because external-CDN startup stalled earlier. The external-CDN startup path is not verified today. The localhost-only runtime=local option and ignored cache are review aids.
- Lesson checked at 1366px and 390px, light and dark: no horizontal overflow; body contrast 16.74 and 15.26 respectively. Phone starter executes and shows the editable function first.
- All four figures inspected. Replaced an overlapping bracket label with the actual nine-call tree; reviewed the replacement in both phone themes. The pending-call diagram explicitly distinguishes calls from lexical parents.
- Across the four converted modules: 23 lesson blocks, ten figures and 43 solution checks pass.

Generated evidence: output/review/03-recursive-functions/.

## Limits

Author estimate is unmeasured: lesson 35–45 minutes, lab 90–130 minutes (125–175 total), recommended over three sessions. Recursive demonstrations use small inputs; memoization does not remove recursion depth. Arithmetic operation bounds use a unit-cost model, with integer growth qualified in the lesson. Checks provide educational feedback, not secure anti-cheating. Optional legacy reading is not fully re-audited. No live assets were published.

Expansion review: invalid window-diagram bindings were repaired after image inspection; boundary arrows and active-window coloring show actual current indices. Nested-node frames use a readable node kind, path and returned value rather than overflowing cells with a stringified container. Varied and frame checks cover both new exercises.

# Review and fix pass — 2026-10-05 (Claude)

Reviewed Codex's commits b51b20b and 0f1a4bf, then changed the module. Not published.

## Found in the previous version

- The lesson used none of SICP 1.2's examples (no factorial, Fibonacci by name, counting change, orders of growth, exponentiation or gcd).
- "A problem that looks different" described the mastery problem, including the modulus, and `tray_total` was the solution to lab exercise 1.
- Four starters were a one-line repair with a comment marking the line.
- 24 assertions had no message.
- The 150-minute estimate was about 40% above my estimate.
- `chapter` was "1.8", which matches nothing.

## Changed

- Lesson rewritten around SICP 1.2 (see topic.md). Nine executable blocks, four figures, about 2,300 prose words.
- Exercise 1 is now `power` (linear recursive b^n). Exercises 1–4 start from stubs.
- Every assertion has a message that states what was expected and what came back.
- `mirrored` rejects slicing; `memo_routes` and `packing` are called twice with the same input to catch shared state; `packing` must use `combine`; RecursionError is reported as a check failure with an explanation.
- Hints rewritten per exercise. Recap, description, subtitle, attribution and estimate (110 minutes, unmeasured) updated; `chapter` is "1.2".

## Verified in this pass

- `tools/lessons.py check 03`: 9 blocks, 4 figures, 0 failures.
- `tools/check_lab.py 03`: 7 exercises, 14 solution checks pass.
- `lab_src.py check`: lab.json up to date.
- Every starter fails at least one check; only `packing_behavior` passes on its starter, by design (the starter is correct but too slow).
- Eight shortcut submissions each fail at least one check.
- Browser smoke (`preview_smoke.mjs --all`, Chromium, Pyodide from the public CDN): all checks passed for the seven exercises, embedded mode and host-supplied lab.
- Lesson at 390 px dark and 1100 px light: document width stays 390 px on the phone after shortening one formula and one table header. Four figures and the growth table inspected.

## Not done

- No learner has timed the module.
- The background-reading link is still relative (`../../reading/...`); it needs the published URL once routing for converted modules exists.
- Pyodide's recursion limit was not measured (see topic.md).
