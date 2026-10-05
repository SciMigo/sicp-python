# Trees: let the structure guide the program

## A question with branches

A small museum stores a collection inside containers. The outer container, labelled 12, holds three things: an item labelled 4, a container labelled 7 holding items 4 and 0, and an item labelled 9. How many items sit at the ends of this structure? The answer is four. Adding the labels gives a different answer, because a label describes a node; it does not say whether that node contains anything.

```figure
{"type":"tree","params":{"node_radius":32,"node_spacing_x":110,"node_spacing_y":95,"root":{"value":"A:12","children":[{"value":"B:4"},{"value":"C:7","children":[{"value":"D:4"},{"value":"E:0"}]},{"value":"F:9"}]}},"caption":"Six nodes, four leaves. Letters identify positions; numbers are labels. B and D are distinct nodes with equal labels."}
```

This module assumes that you can define functions, loop over a list, and explain a recursive call on a smaller input. Module 4 introduced constructors and selectors; module 5 introduced combining the results of processing a sequence. Here the elements themselves contain more elements. That extra level is the source of both the difficulty and the useful pattern.

A **tree** is a node with a label and an ordered sequence of child trees. A **leaf** has no children. The root is the outermost node, and every other node has exactly one parent. We will work with finite trees without cycles or shared child nodes. Those conditions are part of the input contract, rather than facts that our short algorithms validate.

The labels may repeat. They may be zero, negative, strings, or other values. Neither equality of labels nor the truth value of a label determines the shape. Every tree in this model has a root: an empty list of children represents a leaf, not an absent tree.

## Why a fixed number of loops fails

For this museum example, two nested loops seem enough. Look at the root's children, then inspect the children of each container. But the next collection might contain a box inside another box inside another box. Adding one more loop fixes one instance and creates another depth limit. A general solution must follow the structure supplied by its input.

Flattening the numbers first also loses information. The sequence 12, 4, 7, 4, 0, 9 does not tell you which nodes are leaves, which items belong inside container 7, or how to reach the second occurrence of 4. Flattening is useful when the requested result is a sequence; it is not a substitute for a representation of relationships.

Recursion gives us a different promise. Instead of knowing the maximum depth, a function knows how to solve the same question for one child. Its current call combines those child answers into an answer for the current node. The important design step is deciding what each child answer means. “Use recursion” alone does not specify a correct program.

## Keep the representation behind selectors

Here is a dictionary representation. The constructor copies the supplied child sequence so that appending to that sequence later does not append a new child to this node. It does not deep-copy existing children. We will avoid mutation while processing the tree.

```python
def tree(value, children=None):
    return {"value": value, "children": list(children or [])}

def label(t):
    return t["value"]

def branches(t):
    return t["children"]

def is_leaf(t):
    return len(branches(t)) == 0

museum = tree(12, [tree(4), tree(7, [tree(4), tree(0)]), tree(9)])
assert label(museum) == 12
assert not is_leaf(museum)
assert is_leaf(branches(museum)[0])
assert is_leaf(tree(0)) and is_leaf(tree(999))
```

The functions below will use these selectors. That separation matters even for a small exercise: the programmer reading the traversal should be able to identify its mathematical rule without also decoding dictionary layout. A tuple or a small class could implement the same interface.

The default is `None`, rather than a mutable list shared by calls. There is a second subtlety: `branches` exposes the actual child list. That is acceptable under our no-mutation contract, but a production interface might return a tuple or an iterator. An abstraction barrier is an agreement about which operations clients use, not a guarantee that Python prevents every possible violation.

## The book's trees: sequences inside sequences

SICP reaches trees from the other direction. It has no labelled nodes. A tree there is a sequence whose items may themselves be sequences, and the leaves are the items that are not sequences. In Python that is a list containing numbers and lists. The book's first example is the structure `((1 2) 3 4)`: three items at the top level, four leaves in all.

Its `count-leaves` procedure states the plan in three cases: an empty list has no leaves, anything that is not a list is one leaf, and a list has the leaves of its first item plus the leaves of the rest. A Python loop over the items covers the first and third cases together.

```python
def count_leaves(x):
    if not isinstance(x, list):
        return 1
    return sum(count_leaves(item) for item in x)

x = [[1, 2], 3, 4]
assert len(x) == 3
assert count_leaves(x) == 4
assert len([x, x]) == 2
assert count_leaves([x, x]) == 8
assert count_leaves([]) == 0
```

`len` answers a question about one level. `count_leaves` answers a question about the whole structure, and it can do so only because it asks the same question of every item. Putting two copies of `x` in a list doubles the leaves and leaves the length at 2.

The two representations differ in one way that matters for base cases. A nested list can be empty, and an empty list has zero leaves. Our labelled trees always have a root, so the smallest one is a single node, which is one leaf. Most wrong base cases come from mixing up those two conventions. For the rest of this lesson, "tree" means the labelled kind unless nested lists are named.

## Give the recursive answer a meaning

Consider a summary function that returns two numbers: the number of nodes and the number of leaves in its input. A leaf returns `(1, 1)`. An internal node counts itself as one node, then adds the node counts of its children. Its leaf count is the sum of their leaf counts; the internal node itself contributes no leaf.

!!! invariant "What each returned answer means"
    For every completed call, the first result counts all nodes in that call's subtree exactly once, and the second counts exactly the nodes with no children.

This statement supplies a test of the combining rule. If we add one to the leaf count of every internal node, we count nodes rather than leaves. If we return the label at a leaf, we sum labels rather than count leaves. Both programs can terminate and still answer the wrong question.

```python
def summary(t):
    if is_leaf(t):
        return 1, 1
    nodes, leaves = 1, 0
    for child in branches(t):
        child_nodes, child_leaves = summary(child)
        nodes += child_nodes
        leaves += child_leaves
    return nodes, leaves

assert summary(museum) == (6, 4)
assert summary(tree(-8)) == (1, 1)
```

??? predict "What changes if label 7 becomes label 1?"
    Neither count changes. The node still has two children. Only its label changes.

## Read a trace from the bottom up

A call can begin before it knows its answer. At A, the program must wait for B, C, and F. B immediately returns `(1, 1)`. C waits for D and E; they each return `(1, 1)`, so C returns `(3, 2)`. F returns `(1, 1)`. A finally returns `(6, 4)`.

| Completed node | Nodes in its subtree | Leaves in its subtree |
|---|---:|---:|
| B | 1 | 1 |
| D | 1 | 1 |
| E | 1 | 1 |
| C | 3 | 2 |
| F | 1 | 1 |
| A | 6 | 4 |

This completion order is **postorder**: children finish before their parent. The order of starting calls is different. A starts first, then B, then C, then D and E, then F. Starting a call is not the same event as returning a result. A useful visual trace says which event a frame represents.

```figure
{"type":"tree","params":{"node_radius":32,"node_spacing_x":110,"node_spacing_y":95,"root":{"value":"A:6,4","children":[{"value":"B:1,1"},{"value":"C:3,2","children":[{"value":"D:1,1"},{"value":"E:1,1"}]},{"value":"F:1,1"}]},"highlights":{"C:3,2":"current"}},"caption":"After C finishes, its answer summarizes D, E, and C itself. Each label here is node-count, leaf-count, not the original item label."}
```

## Why termination is only half the proof

A recursive call receives a proper child subtree, containing fewer nodes than its parent tree. Because the input is finite, repeatedly moving to a child eventually reaches a leaf. That proves termination under the stated input conditions.

Correctness requires a separate argument. For a leaf, `(1, 1)` satisfies the invariant directly. Now suppose the invariant holds for each child. The child subtrees are disjoint, and together with the current node they partition the current subtree. Adding their node counts and one therefore counts each node exactly once. For an internal node, every leaf belongs to exactly one child subtree, so adding child leaf counts counts all and only its leaves. This is structural induction.

Notice which assumptions the proof uses. A cycle destroys the shrinking-input argument. A shared child changes “count once” into an ambiguous promise: once per object, or once per occurrence? Those inputs need a graph model and an explicit policy. We are not repairing them with a different base case.

## Transformation returns a structure

An aggregation returns a number or a small summary. A transformation returns a new tree. To change every label, reconstruct a node with the transformed label and transformed children. The shape should survive even when labels repeat or transform to equal values.

The book's example is `scale-tree`, which multiplies every leaf of a nested list by a factor. It gives two versions. The first follows the same cases as `count-leaves`. The second treats the tree as a sequence of subtrees and maps over it, scaling each subtree in turn and multiplying when it reaches a leaf. Here is the second, with the book's own data.

```python
def scale_tree(x, factor):
    if not isinstance(x, list):
        return x * factor
    return [scale_tree(item, factor) for item in x]

nested = [1, [2, [3, 4], 5], [6, 7]]
assert scale_tree(nested, 10) == [10, [20, [30, 40], 50], [60, 70]]
assert nested == [1, [2, [3, 4], 5], [6, 7]]
```

Nothing in that function is about multiplying except one expression. Pull that expression out as a parameter and you have the book's `tree-map`: one traversal, any per-leaf rule. This is the step from module 1 again, where a shared process took its rule as an argument.

```python
def tree_map(f, x):
    if not isinstance(x, list):
        return f(x)
    return [tree_map(f, item) for item in x]

assert tree_map(lambda v: v * v, [1, [2, 3], [4, [5]]]) == [1, [4, 9], [16, [25]]]
assert tree_map(lambda v: v * 10, nested) == scale_tree(nested, 10)
```

The labelled version has the same shape. Every node has a label, so the rule applies at every node, and the children are rebuilt by the same function.

```python
def map_labels(f, t):
    return tree(f(label(t)), [map_labels(f, b) for b in branches(t)])

doubled = map_labels(lambda v: 2 * v, museum)
assert label(doubled) == 24
assert summary(doubled) == summary(museum)
assert label(museum) == 12
```

To check a transformed tree we need to see all its labels. Here is a separate, iterative operation that visits labels in root-first order.

```python
def preorder_labels(t):
    pending = [t]
    result = []
    while pending:
        current = pending.pop()
        result.append(label(current))
        pending.extend(reversed(branches(current)))
    return result

assert preorder_labels(museum) == [12, 4, 7, 4, 0, 9]
assert preorder_labels(doubled) == [24, 8, 14, 8, 0, 18]
```

An empty child sequence is helpful in `map_labels`. Mapping over zero children produces zero transformed children, and constructing a node with that result creates a leaf. There is no separate `if is_leaf` branch in the code, even though the mathematical definition still has a leaf case. An implicit stopping case is not the absence of a stopping case.

Preserving shape is stronger than preserving leaf count. Two different shapes can have four leaves. To verify a transformation, compare each node's ordered children and label with the corresponding original node, and also verify that the original input has not changed. The same pattern builds results that are not label-for-label copies: a new node can also receive its children in a different order, or only some of them.

## Search has a different stopping rule

Search asks whether a target occurs. When it does, we may want a path from the root. Define the contract before coding: return the labels along the first matching path in left-to-right depth-first order, or `None` if no match exists. If the root matches, the path contains that root label. It is not empty: an empty sequence would leave out the node we found.

For the museum tree, a target of 4 first reaches B, producing `[12, 4]`. D has the same label, but the first-match contract stops at B. A target of 0 reaches E, producing `[12, 7, 0]`. A target of 12 produces `[12]`. A target of 99 produces `None`.

??? predict "Does a path of labels uniquely identify a node?"
    Not always. Equal labels under equal-labelled ancestors can yield equal label paths. Use child-index paths or unique node identifiers if identity matters.

The following helper lists every root-to-node label path in root-first, left-to-right order. It examines the whole tree, so it is not a search that stops early, but the first matching entry in its list is the path the contract asks for.

```python
def all_paths(t):
    pending = [(t, [label(t)])]
    result = []
    while pending:
        current, path = pending.pop()
        result.append(path)
        for b in reversed(branches(current)):
            pending.append((b, path + [label(b)]))
    return result

def first_path(t, target):
    return next((p for p in all_paths(t) if p[-1] == target), None)

assert first_path(museum, 4) == [12, 4]
assert first_path(museum, 0) == [12, 7, 0]
assert first_path(museum, 12) == [12]
assert first_path(museum, 99) is None
assert [p for p in all_paths(museum) if p[-1] == 4] == [[12, 4], [12, 7, 4]]
```

This distinguishes existence, first match, and all matches. They are separate output contracts. A function that returns one path cannot be judged against an expectation of every path unless the task explicitly changes. Also check the result with `is not None`, which tests the failure sentinel directly. Truthiness can hide errors when a future contract allows a valid empty result.

## Count the work you actually do

For `summary`, let $n$ be the number of nodes and $h$ the maximum number of nodes along a root-to-leaf path. Assume constant-time selectors, bounded-size integer arithmetic, and ordered child sequences. The function enters one call per node and examines one child edge per non-root node. Thus it makes exactly $n$ calls and examines $n-1$ edges; its running time is $\Theta(n)$ under this model.

The recursive call stack has depth at most $h$, so the auxiliary stack space is $O(h)$. A recursive transformation also allocates $\Theta(n)$ new nodes, separate from its stack space. An explicit stack removes Python's recursion-depth limit but does not remove all memory requirements; pushing every pending child can use $O(n)$ space in a wide tree.

Python does not guarantee that a recursive function can handle arbitrary depth. A long chain can exceed the interpreter's recursion limit even though the mathematical recurrence terminates. Increasing that limit is not a proof of safe execution. For deep inputs, design an iterative traversal; for this lab, input depths stay modest.

```python
def star(n):
    assert n >= 1
    return tree("root", [tree(i) for i in range(n - 1)])

calls = 0
plain_summary = summary

def summary(t):
    global calls
    calls += 1
    return plain_summary(t)

for n in (8, 32, 128):
    calls = 0
    assert summary(star(n)) == (n, n - 1)
    assert calls == n
calls = 0
assert summary(museum) == (6, 4) and calls == 6
```

The second definition wraps the first and counts each entry. The recursive calls inside `plain_summary` look up the name `summary` when they run, so they go through the counter too. Every call except the first was made across one child edge, which gives the edge column: calls minus one.

| Star size | Calls | Child edges | Leaves |
|---:|---:|---:|---:|
| 8 | 8 | 7 | 7 |
| 32 | 32 | 31 | 31 |
| 128 | 128 | 127 | 127 |

The ratio of calls to nodes is one. These counts illustrate the proof; they do not replace it. Drawing the entire tree at every step adds visualization cost and is deliberately limited to small instances. The lab's larger measurements suppress drawing while counting traversal work.

## A computation tree is not its returned value

A Fibonacci computation tree can label each node with the Fibonacci value its call returns. A call on 5 has value 5, but its expanded tree has eight leaves: five calls returning 1 and three returning 0. The root's label and the number of leaves answer different questions.

```python
def fib_tree(n):
    assert isinstance(n, int) and n >= 0
    if n <= 1:
        return tree(n)
    left, right = fib_tree(n - 1), fib_tree(n - 2)
    return tree(label(left) + label(right), [left, right])

ft = fib_tree(5)
assert label(ft) == 5
assert summary(ft) == (15, 8)
assert preorder_labels(ft).count(1) == 8  # includes internal nodes labelled 1

def fringe(t):
    return [label(t)] if is_leaf(t) else [v for b in branches(t) for v in fringe(b)]

assert fringe(ft).count(1) == 5
assert fringe(ft).count(0) == 3
assert fringe(museum) == [4, 4, 0, 9]
```

`fringe` is the book's name (exercise 2.28) for the leaves of a tree listed left to right. It is an aggregation whose combined answer is a list, where `summary` combined numbers.

Repeated subproblems explain why constructing this expanded computation tree grows quickly. Processing a tree already given as input is linear in its number of nodes; generating that input can have a very different cost. Always name the input size used by a complexity claim.

## A problem that looks different

An arithmetic expression contains a constant, or an operator with smaller expressions as operands. Could one program compute the expression's value and another print it with parentheses while following the same structure? Think about what each child would return and how an operator would combine those answers. Do not assume that counting children supplies the correct combining rule.

## Practise

The lab uses a different hierarchy and asks for functions this lesson has not written. You will compute a subtree answer that combines children with a rule other than addition, predict the order in which answers become available, build a mirrored tree (the book's exercise 2.27, `deep-reverse`), write a search that stops at the first match, and measure work on unfamiliar sizes. Its final challenge asks for a useful report without identifying the method for you. Run a small example first, inspect its frames, then use the checks to investigate missing cases.

## Recap

**You can now:** Distinguish labels from structure, specify a recursive return contract, count leaves and map over a tree as the book does, and justify a traversal with structural induction.

**Invariant:** A completed call summarizes exactly its own subtree according to the chosen contract.

**Complexity achieved:** Whole-tree aggregation takes $\Theta(n)$ time and $O(h)$ recursive stack space under the selector and arithmetic model above.

**Failure mode:** A shrinking recursive call proves termination, while a correct base value and combining rule are still required for correctness.

**In real software:** Python's `ast.iter_child_nodes` exposes immediate children of an AST node. Syntax trees need node-specific rules, just as our museum summary needs its own combining rule.

**Retrieval:** Module 4: why should traversal code use selectors rather than dictionary keys?

## Check yourself

1. If leaves return zero instead of one in the leaf count, which part of the correctness proof fails?
2. How can a transformation preserve leaf count while changing shape?
3. Why does the linear bound for processing `fib_tree(5)` say nothing by itself about the cost of constructing `fib_tree(n)`?

## Optional background

The [SICP reading for this module](../../reading/06-trees.html) is the book's own section 2.2, kept as a reference. This lesson does not depend on it.
