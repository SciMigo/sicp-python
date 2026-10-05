# Module 06 conversion plan and review notes

## Teaching plan
Problem: count terminal items in a museum hierarchy. Naive approach: fixed-depth loops or flattening away structure. Trace: completed subtree summaries. Invariant: each completed answer describes exactly its subtree. Implementation: a combined node/leaf summary (different from lab functions). Complexity: node entries and child edges, explicitly excluding drawing. Transfer teaser: evaluating an expression. Lab transfer: enclosing charges in a shipment manifest.

Lesson instance: six museum nodes with labels 12, 4, 7, 4, 0, 9. Lab instance: six nodes with labels 6, 0, 1, 5, 5, -2. Exercises: Build structural leaf count; Trace postorder label totals; Implement non-mutating transformation; Measure one label read per node; Mastery report for every shipment position.

## Sources and scope
Original explanation and examples, drawing on standard recursive-data and structural-induction ideas. SICP Chapter 2.2 is background, not required reading. Existing reading/06-trees.html is retained without alterations. Python ast.iter_child_nodes: Python 3.14 docs, checked 2026-10-04, https://docs.python.org/3/library/ast.html#ast.iter_child_nodes (immediate child nodes, including nodes in list fields). Independent course, no university endorsement.

## Correctness contracts
Finite nonempty ordered trees, no shared subtrees or cycles. A leaf is determined by zero children, never label 1 or truthiness. Aggregation correctness requires a correct combining rule as well as termination. First-match search returns a one-label path when the root matches, None on failure. Fibonacci call tree for argument 5 has root label 5, 15 nodes, eight leaves: five labelled 1 and three labelled 0.

Whole-tree aggregation: Theta(n) under constant-time selectors and bounded-size arithmetic, O(h) call stack. Transformation additionally allocates Theta(n) nodes. Python recursion limits apply. Shipment report uses O(n) child-list inspections, but child-index path materialization/hashing/storage can cost Theta(sum of path lengths); do not claim total linear time on a long chain. Metering is educational feedback, not secure grading: direct dictionary access or modified selectors can escape it.

## Oral-defense anchors
1. Leaf returning zero: fails base-case correctness, while termination still holds.
2. Equal leaf counts do not imply identical ordered structure.
3. Processing cost is measured in generated-tree nodes, not Fibonacci argument n.

## Publication
Draft only. The new module requires the site's reading + visualLab routing and a preview export; the legacy deck bundle remains live until publication is explicitly performed. modules/index.json lists only converted modules. The course remains free. Do not deploy the new lab as a legacy deck lab_spec.json.
