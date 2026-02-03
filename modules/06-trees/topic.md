# Trees

## SICP Reference
- Chapter 2.2: Hierarchical Data and the Closure Property (tree processing subset)

## Core Concepts
- Trees as nested lists (recursive data structure)
- Tree constructor: `tree(label, branches)`
- Tree selectors: `label(t)`, `branches(t)`, `is_leaf(t)`
- Tree recursion patterns: process label, recurse on branches
- Tree mapping, filtering, searching
- Common tree operations: count leaves, tree height, tree map

## Key Examples (Python)
1. **Tree ADT**: `tree(3, [tree(1), tree(2, [tree(1), tree(1)])])` — build and inspect
2. **Count leaves**: Recursive — base case is leaf, recurse on branches
3. **Tree map**: Apply a function to every label in the tree
4. **Fibonacci tree**: Visualize `fib(5)` as a tree of recursive calls
5. **Tree search**: Find a path from root to a target label

## Reference Files
- `2.2-hierarchical-data.md`

## Speaker Persona
- Professor Dana: Draws trees, emphasizes recursive structure, "What's the base case?"
- Alex (student): Builds intuition by tracing small trees, sometimes forgets the base case
