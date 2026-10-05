# Module 06 conversion plan and review notes

## Teaching plan
Problem: count terminal items in a museum hierarchy. Naive approach: fixed-depth loops or flattening away structure. SICP's nested-list trees and `count-leaves` (the book's `((1 2) 3 4)` example). Trace: completed subtree summaries. Invariant: each completed answer describes exactly its subtree. Mapping over trees: the book's `scale-tree` and `tree-map` on nested lists, then `map_labels` on labelled trees. Search: first-match contract, checked with an exhaustive `all_paths` helper (not an early-stopping search). Complexity: calls counted by wrapping `summary`. `fringe` (exercise 2.28) on the Fibonacci tree. Transfer teaser: evaluating an expression. Lab transfer: enclosing charges in a shipment manifest.

Lesson instance: six museum nodes with labels 12, 4, 7, 4, 0, 9; nested lists `[[1, 2], 3, 4]` and `[1, [2, [3, 4], 5], [6, 7]]` from the book. Lab instance: six nodes with labels 4, 7, 0, 9, 9, -3 (label 0 on an internal node; no label equals its child position). Deep-reverse uses 4, 7, 0, 9, 2, -3 so a shallow reversal is visible.

Six exercises, none of which the lesson solves: Build `height` (combine with max, completion frames); Trace `totals` (postorder label sums, two predictions); Implement `deep_reverse` (SICP exercise 2.27 on labelled trees, fresh nodes); Search `find_path` (first match, one frame per examined node, stops early); Measure `profile` (one label read per node); Mastery report for every shipment position. Build, Trace, Implement and Search starters are stubs that run, draw one frame and fail both checks.

## Sources and scope
SICP section 2.2.2, Hierarchical Structures (Abelson and Sussman with Julie Sussman): `count-leaves`, `scale-tree`, `tree-map` (exercise 2.31), `fringe` (2.28) and `deep-reverse` (2.27) are the book's, translated to Python with new prose. reference/2.2-hierarchical-data.md is the working copy of the section; reading/06-trees.html stays a reference link. The labelled-tree interface `tree` / `label` / `branches` / `is_leaf` and the `fib_tree` example follow John DeNero's *Composing Programs* section 2.3.6 (CC BY-SA 3.0), the text of UC Berkeley CS 61A; that vocabulary is not original to this course. The museum and shipment scenarios, figures, checks and lab exercises are written for this course. Python ast.iter_child_nodes: Python 3.14 docs, checked 2026-10-04, https://docs.python.org/3/library/ast.html#ast.iter_child_nodes (immediate child nodes, including nodes in list fields). Independent course, no university endorsement.

## Correctness contracts
Finite nonempty ordered trees, no shared subtrees or cycles. A leaf is determined by zero children, never label 1 or truthiness. Aggregation correctness requires a correct combining rule as well as termination. First-match search returns a one-label path when the root matches, None on failure. Fibonacci call tree for argument 5 has root label 5, 15 nodes, eight leaves: five labelled 1 and three labelled 0.

Whole-tree aggregation: Theta(n) under constant-time selectors and bounded-size arithmetic, O(h) call stack. Transformation additionally allocates Theta(n) nodes. Python recursion limits apply. Shipment report uses O(n) child-list inspections, but child-index path materialization/hashing/storage can cost Theta(sum of path lengths); do not claim total linear time on a long chain. Metering is educational feedback, not secure grading: direct dictionary access or modified selectors can escape it. Nested lists may be empty (zero leaves); labelled trees always have a root.

## Oral-defense anchors
1. Leaf returning zero: fails base-case correctness, while termination still holds.
2. Equal leaf counts do not imply identical ordered structure.
3. Processing cost is measured in generated-tree nodes, not Fibonacci argument n.

## Publication
Draft only. The new module requires the site's reading + visualLab routing and a preview export; the legacy deck bundle remains live until publication is explicitly performed. modules/index.json lists only converted modules. The course remains free. Do not deploy the new lab as a legacy deck lab_spec.json.
