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
