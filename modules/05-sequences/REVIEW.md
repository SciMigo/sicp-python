# Module 05 review — 2026-10-06

Checked local draft; not published. Based on reviewed merged main 5f8554a, independently of pending Module 4 PR #9.

## Scope and sequencing

1,896 prose words, nine executable Python blocks and two semantic figures. Only SICP §§2.2.1 and 2.2.3, plus an explicitly identified Python generator extension. Includes pair-chain sequences, list-ref/length/append, scale-list/map, odd-square stages over already enumerated input, even-fibs, fold direction, nested pair enumeration and demand. Module 6 owns §2.2.2; no count_leaves, tree_map, nested structural mapping or tree traversal is taught here. The full shared reading remains optional reference.

Five labs: same_parity (2.20), a source/predicate/map/output event trace, horner (2.34), actual source-yield measurement and a separate live-feed preview. Build/Implement starters are stubs, not pre-broken completed solutions. Lesson does not print lab demo answers or complete the polynomial exercise; its drawing-candidate teaser differs from the adjacent-reading mastery. Source credit, changes and CC BY-SA 4.0 notice are included.

## Verification

- Nine lesson blocks and two figures pass; lab_src packing is current.
- Ten solution checks pass. Each starter executes and draws; nine of ten checks fail untouched. Only deliberately correct-but-overeager mastery behavior passes. Every Python assert carries a message.
- Mutation probes reject reversed retained order, eager trace construction, wrong coefficient direction, output-count substitution for source pulls, and reading beyond the kth rise.
- Varied inputs cover negative/zero values, repeats, exact prefix/frame state, no match, short inputs, zero demand, empty coefficients, zero/negative polynomial arguments, input preservation, restored measurement source after exceptions and unusual solver consumption.
- Guarded unbounded input stops overeager code immediately with actionable feedback. It verifies zero source reads for k=0 and the exact prefix boundary for original adjacent rises. No wall-clock grading.
- Chrome/Pyodide smoke with the external CDN passes all five exercises, Run/Check, frame playback, question completion, mastery unlock, embedded sizing and host/example integration, with no page errors.
- Inspected all sixteen smoke screenshots, both lesson figures in phone light/dark themes and the phone starter. Visual review replaced the apparently empty Build picture with explicit not-visited/none-retained placeholders; reran checks after that helper change.
- At 1366 and 390 pixels, light and dark lesson layouts have no horizontal overflow. Body contrast 16.74 and 15.26. The phone starter executes and shows the editable function first.

## Estimate and contracts

Unmeasured estimate: about 25 minutes for the lesson (200 prose words/minute plus code and figure study), then 10/15/10/10/15 minutes for five labs: about 85 total. Linked-chain storage is distinguished from Python lists; recursive append's stack and copied pairs are qualified. Callback counts alone are not arithmetic/allocation bounds. Lazy prefix work depends on examined inputs, not only accepted outputs. Generator suspension and map/filter iterator behavior are sourced in topic.md and linked to official Python documentation.

An unbounded mastery source is promised eventually to provide k rises when k is positive; otherwise termination is not guaranteed. Helpers exclude drawing from measured operations. Educational checks do not provide a secure anti-cheating boundary. The shared reference still includes other book sections and uses the existing reference-host path. Course-wide tutor concepts, reference-host cleanup and old-reading licence notices remain separate work.

Publication needs reviewed asset export (05 added to PREVIEW_MODULES), then a sicpModule registry entry and viewer deployment. No live assets changed. Evidence: output/review/05-sequences/.
