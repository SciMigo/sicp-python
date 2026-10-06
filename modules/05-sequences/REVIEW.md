# Module 05 review — 2026-10-06

Checked local draft; not published. Based on reviewed merged main 5f8554a, independently of pending Module 4 PR #9.

## Scope and sequencing

1,896 prose words, nine executable Python blocks and two semantic figures. Only SICP §§2.2.1 and 2.2.3, plus an explicitly identified Python generator extension. Includes pair-chain sequences, list-ref/length/append, scale-list/map, odd-square stages over already enumerated input, even-fibs, fold direction, nested pair enumeration and demand. Module 6 owns §2.2.2; no count_leaves, tree_map, nested structural mapping or tree traversal is taught here. The full shared reading remains optional reference.

Five labs: same_parity (2.20), a source/predicate/map/output event trace, horner (2.34), actual source-yield measurement and a separate live-feed preview. Build/Implement starters are stubs, not pre-broken completed solutions. Lesson does not print lab demo answers or complete the polynomial exercise; its drawing-candidate teaser differs from the adjacent-reading mastery. Source credit, changes and CC BY-SA 4.0 notice are included.

## Verification

- Nine lesson blocks and two figures pass; lab_src packing is current.
- Ten solution checks pass. Each starter executes and draws; nine of ten checks fail untouched. Only deliberately correct-but-overeager mastery behavior passes. Every Python assert carries a message.
- Mutation probes reject reversed retained order, eager trace construction, wrong coefficient direction, output-count substitution for source pulls, and reading beyond the kth rise.
- Varied inputs cover negative/zero values, repeats, exact prefix/frame state, no match, short inputs, zero demand, empty coefficients, zero/negative polynomial arguments, input preservation, unchanged supplied source after exceptions and unusual solver consumption.
- Guarded unbounded input stops overeager code immediately with actionable feedback. It verifies zero source reads for k=0 and the exact prefix boundary for original adjacent rises. No wall-clock grading.
- Chrome/Pyodide smoke with the external CDN passes all five exercises, Run/Check, frame playback, question completion, mastery unlock, embedded sizing and host/example integration, with no page errors.
- Inspected all sixteen smoke screenshots, both lesson figures in phone light/dark themes and the phone starter. Visual review replaced the apparently empty Build picture with explicit not-visited/none-retained placeholders; reran checks after that helper change.
- At 1366 and 390 pixels, light and dark lesson layouts have no horizontal overflow. Body contrast 16.74 and 15.26. The phone starter executes and shows the editable function first.

## Estimate and contracts

Unmeasured estimate: about 25 minutes for the lesson (200 prose words/minute plus code and figure study), then 10/15/10/10/15 minutes for five labs: about 85 total. Linked-chain storage is distinguished from Python lists; recursive append's stack and copied pairs are qualified. Callback counts alone are not arithmetic/allocation bounds. Lazy prefix work depends on examined inputs, not only accepted outputs. Generator suspension and map/filter iterator behavior are sourced in topic.md and linked to official Python documentation.

An unbounded mastery source is promised eventually to provide k rises when k is positive; otherwise termination is not guaranteed. Helpers exclude drawing from measured operations. Educational checks do not provide a secure anti-cheating boundary. The shared reference still includes other book sections and uses the existing reference-host path. Course-wide tutor concepts, reference-host cleanup and old-reading licence notices remain separate work.

Publication needs reviewed asset export (05 added to PREVIEW_MODULES), then a sicpModule registry entry and viewer deployment. No live assets changed. Evidence: output/review/05-sequences/.

Follow-up from Module 4 PR #11: measurement now passes a counting source into strategies, using the wrapper pattern taught in Module 1. Learners need no global rebinding. Fresh counts, actual delegation and exceptions remain checked.

## 2026-10-06: polish after review (Claude)

The minor items from the review of this module, none of which blocked it.

- Lesson: the first figure now draws the chain of pairs; the pipeline figure is a flow of four
  stages, so the environment-frame picture keeps its one meaning from module 2. Added the
  invariant call-out, two predict blocks, a measured table (reads for "build everything" against
  "ask for three" at 20, 40 and 80 items, asserted in a code block), the standard recap labels
  with an "In real software" line, and three "Check yourself" questions.
- Lab: every check message now says what was called, what was expected and what came back. The
  trace check names the first event that differs.
- Measure: the bars check recounts on sizes the demo does not use (10, 30, 70 with two results).
- Horner: the starter's placeholder frame no longer shows index -1, and is not counted.
- Mastery: one frame per pair of neighbouring readings, then the preview. The check compares the
  step frames with the readings actually pulled.
- Prompts are split into what to build, what to draw and the limits.

Verified: `lessons.py check 05` ok (10 blocks, 2 figures); `check_lab.py 05` ok (5 exercises,
10 solution checks); lab sources up to date; 9 of 10 checks red on untouched starters (the tenth
is the mastery correctness check); 13 wrong, lazy and alternative submissions behave as expected;
browser smoke with `--all` on Pyodide 0.27.4 from the CDN passes; lesson stays within 390 px.
Looked at both lesson figures and the mastery's first step frame.
