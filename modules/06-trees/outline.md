# Trees — Slide Outline

## Slide 1: From Lists to Hierarchies
- Lists are flat — what if data has structure?
- Family trees, file systems, expression trees, HTML DOM
- Motivate: We need a data structure that branches

## Slide 2: The Tree ADT
- `def tree(label, branches=[]): return [label] + list(branches)`
- `def label(t): return t[0]`
- `def branches(t): return t[1:]`
- `def is_leaf(t): return not branches(t)`
- Build: `t = tree(3, [tree(1), tree(2, [tree(1), tree(1)])])`

## Slide 3: Visualizing Trees
- Diagram of `t` from Slide 2 — root 3, children 1 and 2, leaves under 2
- Labels at nodes, branches are edges
- **Checkpoint**: Predict `label(branches(t)[1])` → 2

## Slide 4: Counting Leaves
- `def count_leaves(t): return 1 if is_leaf(t) else sum(count_leaves(b) for b in branches(t))`
- Trace on our example tree: 1 + (1 + 1) = 3
- Pattern: base case → leaf; recursive case → process branches and combine

## Slide 5: Tree Map
- Apply a function to every label: `tree_map(f, t)`
- `def tree_map(f, t): return tree(f(label(t)), [tree_map(f, b) for b in branches(t)])`
- Example: `tree_map(lambda x: x * x, t)` → tree with squared labels
- **Checkpoint**: Draw the result of `tree_map(lambda x: x + 1, t)`

## Slide 6: Tree Recursion Patterns
- Three common patterns:
  1. **Aggregate**: combine results from branches (count_leaves, tree_sum)
  2. **Transform**: build a new tree (tree_map)
  3. **Search**: find a node or path (find_path)
- All follow: process label, recurse on branches

## Slide 7: The Fibonacci Tree
- `def fib_tree(n): if n <= 1: return tree(n); ...`
- Builds the actual computation tree for `fib(5)`
- Each node shows the value, structure shows the call pattern
- `count_leaves(fib_tree(5))` → 8 (equals fib(5)!)

## Slide 8: Tree Search — Finding a Path
- `def find_path(t, target)` — return the path from root to target
- Uses backtracking: try each branch, return if found
- Example: find path to label 1 in our tree → multiple paths

## Slide 9: Summary
- Trees = labels + branches (recursive definition)
- Tree processing = handle leaf + recurse on branches
- Abstraction barrier: use `tree()`, `label()`, `branches()` — never reach inside
- Preview: Next we'll explore mutation — what happens when data changes
