# Module 03 review — 2026-10-05

Status: checked local draft, free; not published.

## Scope and changes

Independent 1,976-word lesson with six executable Python blocks and two semantic figures. Teaches termination and decreasing measures, pending calls versus lexical parents, correctness by induction, loop invariants, repeated subproblems, memoization and bottom-up computation. Python does not eliminate tail calls; storing two integers is not a claim of constant bit space. Original reading remains optional background; old lab and slide outline are archived.

Five exercises: recursive sum with actual stack snapshots, postorder trace, memoized routes, measured transition calls, and ordered batch packing with caller-supplied sizes and modular arithmetic. Mastery names no technique and gates reasoning questions behind an attempt or explicit request.

## Checks

- Six lesson blocks and two figures pass. Syntax highlighting retained.
- Ten solution checks pass; all five starters execute and draw but fail substantive checks.
- Varied inputs check recursive calls, caller-stack restoration, exact completion order, fresh memo state, actual counted transitions, counter restoration after exceptions, ordered versus unordered plans, input preservation and modular residues. Budget guards stop runaway attempts promptly and report ordinary check failures.
- Memo checks reach length 200; mastery reaches 6,000 with a bound of n times the number of allowed sizes. Operation counts exclude base cases where explicitly stated, and never grade wall-clock speed.
- Chrome/Pyodide smoke passes all five exercises, frame playback, question completion, mastery gating, recap, embedded sizing and host-provided lab/example retrieval. All sixteen screenshots inspected.
- Browser execution used real Pyodide 0.27.4 cached locally because external-CDN startup stalled earlier. The external-CDN startup path is not verified today. The localhost-only runtime=local option and ignored cache are review aids.
- Lesson checked at 1366px and 390px, light and dark: no horizontal overflow; body contrast 16.74 and 15.26 respectively. Phone starter executes and shows the editable function first.
- Both figures inspected. Replaced an overlapping bracket label with the actual nine-call tree; reviewed the replacement in both phone themes. The pending-call diagram explicitly distinguishes calls from lexical parents.
- Across the four converted modules: 23 lesson blocks, eight figures and 39 solution checks pass.

Generated evidence: output/review/03-recursive-functions/.

## Limits

Author estimate is unmeasured: lesson 25–35 minutes, lab 65–90 minutes (90–125 total). Recursive demonstrations use small inputs; memoization does not remove recursion depth. Arithmetic operation bounds use a unit-cost model, with integer growth qualified in the lesson. Checks provide educational feedback, not secure anti-cheating. Optional legacy reading is not fully re-audited. No live assets were published.
