# Module 06 conversion review — 2026-10-04

Draft lesson + visual lab, kept free. Optional original reading retained separately and untouched. No CDN upload, production routing change, tutor export, or publication performed.

Validated:
- Five lesson Python blocks execute in order; every assertion passes.
- Both straightedge figures render and were visually reviewed (distinct node identities despite duplicate numeric labels).
- Five lab reference solutions pass all nine checks. Every starter terminates and fails a check aimed at its defect.
- All five exercises run and pass in Chrome/Pyodide; frame playback, checklist/questions, recap, embedded mode, host-supplied lab mode, and example loading pass.
- Mastery questions stay hidden until the first Check, with an optional early-reveal button.
- Sixteen browser screenshots reviewed. Enlarged node circles after label overflow was seen; moved the checklist into the instruction row and Run above the code.
- Lesson at 1366px and 390px, light/dark: no horizontal document overflow. Phone lab: no horizontal overflow. Dark lesson body and callout text contrast exceeds 4.5:1 for the specified foreground/background colors.

Estimate: lesson 25–35 minutes; lab 55–80 minutes, unmeasured. Optional background excluded.

Scope notes: the laboratory is educational feedback, not secure grading. Whole-tree aggregation is linear under the stated model; shipment path construction/storage additionally costs the sum of output path lengths. Python recursion limits remain relevant; lab input depths are bounded.

Before publication: wire this converted module into the site's reading + visualLab route, export its public assets, check that optional reading links resolve at their published URLs, then update tutor knowledge. Other modules are untouched and are not certified by this review.

## Review-fix pass — 2026-10-05

Follows an external review of the checkpoint. Still a draft; nothing published.

Changed:
- Lab is now six exercises: `height`, `trace_totals`, `deep_reverse`, `find_path`, `measure`, `shipment_report`. The first four open on stubs that run and draw but fail both checks; no starter carries a comment marking a fix. `leaf_count` and `transform` are gone because the lesson now teaches the book's `count-leaves` and `tree-map`.
- New first-match search exercise with one frame per examined node; a check asserts the search stops at the match.
- `measure` check `measured_bars` now asserts the measured rows, so no checklist step is green on the untouched starter (the mastery starter still passes its correctness check by design and fails the budget).
- Hints are written per exercise. Every assert in every check has a message.
- Lab sample labels changed to 4, 7, 0, 9, 9, -3 so a node name never reads `0:0` or `1:1`.
- Lesson adds SICP 2.2.2 content in Python: nested-list trees and `count_leaves`, `scale_tree`, `tree_map`, `map_labels`, `fringe`; the search paths and the star-table call counts are now asserted. "Optional background" is one reference sentence.
- Attribution names *Composing Programs* for the labelled-tree interface and `fib_tree`. `chapter` is "SICP §2.2.2".

Verified in this pass:
- `tools/lessons.py check 06`: 10 blocks, 2 figures, 0 failures.
- `tools/check_lab.py 06`: 6 exercises, 12 solution checks pass. `lab_src.py check`: lab.json up to date.
- Untouched starters, each check run separately: 11 of 12 fail; the one pass is the mastery correctness check.
- 20 wrong or lazy submissions (first-child-only height, node count as height, label-based leaf test, final-frame-only and entry-frame drawing, leaves-only totals, shallow or in-place reverse, plain copy, last-match / shallowest-match / children-first search, truthiness on labels, uncounted or doubled label reads, all-labels charges) each fail at least one check. A deepcopy-then-reverse-in-place `deep_reverse` passes, which is a correct solution.
- Chrome/Pyodide smoke (`preview_smoke.mjs 06-trees --all`, real CDN): all checks passed, 19 screenshots; three inspected (mirror result, search frame, embedded), node labels readable.
- Lesson built and opened at 390 px dark and 1100 px light: no horizontal overflow (scrollWidth 390).

Estimate: lesson 25–35 minutes, lab 55–75 minutes, unmeasured.

Not done here: modules/index.json still carries the old heading and subtitle (regenerate with tools/build_preview_index.py). No `concepts` tags, because the course has no concepts.yaml. The meter in the mastery challenge can still be bypassed with direct dictionary access, as topic.md states.
