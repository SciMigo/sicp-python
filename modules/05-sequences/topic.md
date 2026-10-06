# Module 5: sequences — 2026-10-06

## Scope and sequencing

Owner: take SICP §§2.2.1 and 2.2.3 only, plus Python generators. Module 6 owns §2.2.2. Do not repeat count_leaves or tree_map, nested structural mapping, or tree enumeration. The shared reading includes all §2.2 and remains an optional reference; the lesson explicitly scopes the sections. Working source: reference/2.2-hierarchical-data.md, those two sections. Keep book examples/exercises in Python and new teaching prose. Follow reviewed merged main 5f8554a; Module 4 PR #9 is independent and pending, not a base dependency.

## Seven beats and lab plan

Problem: ordered sequences connect reusable stages. Naive approach: pair chains and separate loops. Visual trace: ordered row and stage records. Invariants: visited-prefix map/filter and completed-suffix right fold. Implementation: list-ref/length/append, map/scale-list, even-fibs, folds, nested pair enumeration. Complexity: callback/selector/source counts with representation and arithmetic qualifications. Transfer teaser: delayed candidate shape generation; not the mastery feed task.

Book examples include the chain 1..4, scaling 1..5 by ten, map abs, odd-square flat input 1..5, even-fibs through 8, and prime-sum-pairs through 6. Section 2.2.3's hierarchical odd-square input is replaced by its already-enumerated flat input; hierarchy enumeration stays in Module 6. Exercise 2.34 is mentioned but not solved in the lesson. No same-parity lab answers, polynomial demo answer, measured lab pull counts or mastery implementation are printed.

Five labs: same_parity (2.20) from a stub, exact demand trace, horner (2.34) from a stub, actual source-yield measurement, rising_preview with one-shot/unbounded input. Demo instances differ from lesson. Build/Implement starters run/draw one frame without marker comments. Tailored hints and messages on all assertions; only mastery correctness may pass untouched.

Measured operation: a value yielded by the supplied source, including later-rejected values. Increment inside the generator, not on iterator creation. Pass a counting source function into each strategy; do not rebind globals. The original source stays unchanged, including on errors. Mastery tracks original adjacent readings, stops at the kth rise, consumes nothing for k=0. For an unbounded source and positive k, eventual k rises are a precondition, not something laziness can guarantee. Guarded sources terminate overeager attempts immediately, without timing-based grading.

## Sources for Python extension

Checked 2026-10-06 against official Python documentation: map/filter return iterators (https://docs.python.org/3/library/functions.html#map); yield suspends and retains local state (https://docs.python.org/3/reference/expressions.html#yield-expressions); bounded prefix consumption (https://docs.python.org/3/library/itertools.html#itertools.islice). Use established behavior available in Pyodide's Python, no 3.14-specific features. SICP's §2.2 finite list implementations are not claimed to be lazy. No implementation-specific Python list timing guarantee is asserted.

## Contracts and oral anchors

Finite integer lists/coefficients at most 20 in drawn labs, nonnegative k at most 20; closures and callbacks terminate normally. Prefix work depends on inspected source values p, not just accepted outputs k. Callback costs, big integer costs, allocation and drawing remain separate. The teaching recursive linked append copies the first chain and shares the second; Python call-depth and mutable payload sharing are explicit. Iterative right fold has the book's grouped value for pure operations, with callback effects evaluated right to left.

Oral: filtering before mapping is not interchangeable without translating predicates; zero demand cannot pull; rejected adjacent pairs still replace the predecessor; materializing a live source cannot produce an early preview; lists can replay stored values, an exhausted iterator cannot.

Publication remains separate: add 05 to PREVIEW_MODULES in scimigo-platform, publish the reviewed revision, then use sicpModule(...) in the viewer registry and deploy. Preserve unlisted status. Course-wide concepts/tutor tags and reference-host/licence cleanup remain open.
