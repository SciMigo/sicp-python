# Sequences: an interface for ordered work

## One sequence, several questions

SICP §2.2.1 asks how pairs can represent an ordered collection. Section 2.2.3 then asks how that collection can become an interface between stages of a computation. These are this module's two book sections. Hierarchical traversal belongs to Module 6; here each sequence operation works along one ordered collection.

Suppose we want to scale every number, keep only selected numbers, or add the resulting values. We could write a different loop for every question. The book instead names the recurring roles: enumerate the inputs, filter the ones wanted, map a transformation, and accumulate the results. The interfaces between those roles let us change one stage while preserving the others.

You should already be comfortable with functions, closures and loops. Module 4 introduced the distinction between a value's meaning and its representation. This module applies that distinction to sequences. You will preserve order, distinguish a right fold from a left fold, and explain why asking for a short prefix can do less work than building a whole list.

## A list can be a chain of pairs

The book's sequence `1, 2, 3, 4` is a chain. Each pair contains one value and a reference to the remaining sequence. A distinguished empty value ends the chain. Here is a Python model of that representation, using tuples for pairs and `None` for the empty chain.

```python
def cons(value, rest):
    return (value, rest)

def head(items):
    return items[0]

def tail(items):
    return items[1]

numbers = cons(1, cons(2, cons(3, cons(4, None))))
assert head(numbers) == 1, "The first pair holds the first element."
assert head(tail(numbers)) == 2, "Following one link selects the second element."
assert tail(tail(tail(tail(numbers)))) is None, "Four links reach the empty terminator."
```

```figure
{"type":"linked_list","params":{"type":"singly","nodes":[{"id":"n1","value":1},{"id":"n2","value":2},{"id":"n3","value":3},{"id":"n4","value":4}],"show_null":true,"pointers":[{"node":"n1","label":"numbers"}]},"caption":"The book's four-element sequence as a chain of pairs. Each pair holds one value and a link to the rest; the last link is the empty value. Reaching the fourth value means following three links."}
```

Do not identify this teaching representation with a Python `list`. A Python list supports indexing and can contain arbitrary objects, but it is not this chain of nested pairs. The same abstract operation can have a different cost in a different representation. For a linked chain, reaching index `i` follows `i` links. Indexing a Python list does not walk such a chain.

The book's `list-ref`, `length` and `append` all follow the same structural boundary: inspect the current pair, then ask about its tail. We can make that explicit without using deep Python recursion.

```python
def list_ref(items, index):
    if index < 0:
        raise IndexError("this interface accepts nonnegative indices")
    while index > 0 and items is not None:
        items = tail(items)
        index -= 1
    if items is None:
        raise IndexError("index beyond the sequence")
    return head(items)

def linked_length(items):
    count = 0
    while items is not None:
        count += 1
        items = tail(items)
    return count

assert list_ref(numbers, 3) == 4, "Three tail steps reach the fourth value."
assert linked_length(numbers) == 4, "Count one element per pair."
assert linked_length(None) == 0, "The empty chain has no elements."
```

For appending chains, the book's recursive form copies the first chain and shares the second as its tail. The implementation below follows that form for small examples. It does not mutate either argument.

```python
def append_linked(first, second):
    if first is None:
        return second
    return cons(head(first), append_linked(tail(first), second))

joined = append_linked(numbers, cons(5, None))
assert linked_length(joined) == 5, "Appending one value adds one pair."
assert list_ref(joined, 4) == 5, "The second chain follows the first."
assert linked_length(numbers) == 4, "The original first chain remains unchanged."
```

For a first chain of length `m`, this implementation creates `m` new pairs and has a call chain of depth proportional to `m`. Sharing the second chain is safe here because these pair tuples are immutable. If the parts themselves are mutable objects, sharing them still shares those objects. Deep inputs also encounter Python's recursion limit; the structural idea does not require this recursive implementation for every workload.

## Map names the transformation

The book's `scale-list` multiplies each input by a factor. Its recursive details obscure a more general statement: apply one function to every element and retain the order. That statement is `map`.

```python
def map_list(function, items):
    result = []
    for item in items:
        result.append(function(item))
    return result

def scale_list(items, factor):
    return map_list(lambda item: item * factor, items)

assert scale_list([1, 2, 3, 4, 5], 10) == [10, 20, 30, 40, 50], "Scaling preserves order."
assert map_list(abs, [-10, 2.5, -11.6, 17]) == [10, 2.5, 11.6, 17], "Map applies the supplied rule."
assert map_list(lambda x: x * x, [1, 2, 3, 4]) == [1, 4, 9, 16], "Mapping can change values without changing positions."
```

!!! invariant "What map has built so far"
    Before each iteration, the result holds the transformed values of exactly the items already visited, in their original order.

The empty result satisfies this before the first iteration. Appending the transformation of the next item extends it by one. When every input has been visited, the result is the complete mapping.

A filter has a related invariant: its result contains exactly the visited items that satisfy its predicate, in their original order. It may shorten a sequence, but it should not sort it, remove duplicates merely because they repeat, or change the surviving values. In Python a list comprehension can express either operation: `[f(x) for x in items]` maps, and `[x for x in items if keep(x)]` filters.

Order matters when functions have observable effects. Mapping a printing function and discarding its answers is conceptually different from building a useful list of return values. The book calls the first kind of operation `for-each`. Be clear about which behavior a caller is requesting.

## Sequences connect conventional stages

Section 2.2.3 presents computations as signal-flow stages. We will use an already enumerated flat sequence for the odd-square example. Obtaining values from a hierarchy is deliberately left to Module 6. The stages here are selection, transformation and combination, regardless of where that input sequence came from.

```python
items = [1, 2, 3, 4, 5]
odds = [x for x in items if x % 2 == 1]
squares = map_list(lambda x: x * x, odds)
assert odds == [1, 3, 5], "Selection keeps odd values in their original order."
assert squares == [1, 9, 25], "Only the selected values are squared."
assert sum(squares) == 35, "Accumulation combines the mapped sequence."
```

```figure
{"type":"flow_diagram","params":{"steps":[{"label":"Enumerate","desc":"1, 2, 3, 4, 5"},{"label":"Filter odd","desc":"1, 3, 5"},{"label":"Map square","desc":"1, 9, 25"},{"label":"Accumulate +","desc":"35"}]},"caption":"The four stages of the odd-square sum. Under each stage is the sequence it passes on; the last stage passes on one number."}
```

The book's second comparison is `even-fibs`: enumerate indices, compute each Fibonacci value, select even values, and collect them. The stages come in a different order because the predicate now concerns a computed value. Reversing map and filter without translating the predicate can change the answer.

```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def even_fibs(n):
    return [value for value in map(fib, range(n + 1)) if value % 2 == 0]

assert even_fibs(8) == [0, 2, 8], "Filter the Fibonacci values, not their indices."
assert [i for i in range(9) if i % 2 == 0] == [0, 2, 4, 6, 8], "Even indices answer a different question."
```

A conventional interface does not mean every pipeline is automatically correct. Its stages must agree about what flows between them. If a predicate expects a number but receives a pair, the interface has been misunderstood even though both stages individually work.

## Accumulation has a direction

SICP's sequence `accumulate` is a right fold. For three elements it groups the operations as `op(a, op(b, op(c, initial)))`. This differs from the left-to-right numeric accumulation in Module 1. The position of the initial value and the grouping of the calls are part of the contract.

```python
def fold_right(op, initial, items):
    result = initial
    for item in reversed(items):
        result = op(item, result)
    return result

def fold_left(op, initial, items):
    result = initial
    for item in items:
        result = op(result, item)
    return result

assert fold_right(lambda a, b: a - b, 0, [2, 5, 8]) == 5, "Right grouping is 2 - (5 - (8 - 0))."
assert fold_left(lambda a, b: a - b, 0, [2, 5, 8]) == -15, "Left grouping starts with 0 - 2."
assert fold_right(lambda a, b: a + b, 0, [2, 5, 8]) == 15, "An associative operation with identity zero agrees."
assert fold_left(lambda a, b: a + b, 0, [2, 5, 8]) == 15, "The same identity and associative operation agree here."
```

??? predict "With subtraction and initial value 0, what do the right and left folds of [10, 4] give?"
    The right fold is 10 - (4 - 0) = 6. The left fold is (0 - 10) - 4 = -14. The grouping and the place of the initial value both changed.

For mathematical associative operations and a suitable identity, the two folds agree on finite inputs. Subtraction fails that condition. Floating-point addition also need not be associative because of rounding. Do not infer equivalence from one small sum.

This iterative right fold computes the same grouped value as the book's recursive definition for pure operations. It invokes `op` from the rightmost element toward the left. Its invariant says the current result is the right fold of the suffix already processed. Combining the preceding element extends that suffix. The invariant proves the final answer; loop termination follows from the finite number of elements.

Exercises 2.33–2.39 show how folds can build other sequence operations. Exercise 2.34 represents a polynomial by coefficients ordered from constant term upward. Processing from the highest coefficient lets each stage reuse the value already computed instead of separately evaluating every power. You will implement that calculation in the lab; it is not completed here.

The fold makes one callback per element. That alone is not a linear-time guarantee. If a callback repeatedly concatenates a growing Python list, copied elements can total a quadratic amount. A constant-time numeric callback over bounded-size numbers gives linear callback work; large integers and allocating callbacks need their own analysis.

## Nested mappings enumerate combinations

Section 2.2.3 also uses sequences to express nested loops. For each integer i, enumerate the smaller positive integers j; each inner sequence contains pairs beginning with that i. Joining those sequences is a `flatmap`: map each input to a sequence, then concatenate the resulting sequences in order. This is a sequence of combinations, not a traversal of hierarchical data.

The book filters these pairs by whether their sum is prime, then maps each retained pair to a triple containing its sum. A Python comprehension expresses the same ordered enumeration without constructing intermediate lists of lists.

```python
from math import isqrt

def is_prime(number):
    return number >= 2 and all(number % divisor for divisor in range(2, isqrt(number) + 1))

def prime_sum_pairs(n):
    return [(i, j, i + j) for i in range(1, n + 1)
            for j in range(1, i) if is_prime(i + j)]

assert prime_sum_pairs(6) == [(2, 1, 3), (3, 2, 5), (4, 1, 5), (4, 3, 7), (5, 2, 7), (6, 1, 7), (6, 5, 11)], "Enumerate in i-then-j order before selecting prime sums."
assert sum(len(range(1, i)) for i in range(1, 7)) == 15, "Six outer indices enumerate fifteen candidate pairs."
```

For general n, there are n times n minus one divided by two candidate pairs. That counts enumeration, not the internal work of primality testing or the number of outputs. Making the enumeration lazy could avoid storing all candidates, but requesting every answer still requires considering all these candidates in this design.

## Python extension: requesting values instead of storing them all

The book initially uses finite lists as its conventional interface. Python's built-in `map` and `filter` instead produce iterators. A generator adds a convenient way to produce values on demand: `yield` suspends a function, retaining the state needed to resume it. This is a Python extension to this lesson, not a claim that §2.2's list implementations are lazy.

```python
from itertools import islice

events = []
def readings():
    for value in [2, 5, 8, 11]:
        events.append(value)
        yield value

pipeline = map(lambda x: x + 1, filter(lambda x: x > 4, readings()))
assert events == [], "Building this generator pipeline has not requested source values."
assert next(pipeline) == 6, "Demand searches until the first accepted source value."
assert events == [2, 5], "The rejected first value still had to be read."
assert list(islice(pipeline, 1)) == [9], "A second request resumes the existing iterator."
assert events == [2, 5, 8], "Taking one more result does not request the last source value."
assert list(pipeline) == [12], "Consuming the rest continues from its current position."
assert list(pipeline) == [], "The same iterator is exhausted, not automatically replayed."
```

??? predict "A source yields 3, 7, 9, 12 and the filter keeps values above 8. How many source values are read to deliver the first result?"
    Three. The values 3 and 7 are read and rejected before 9 is accepted. The 12 is not read until someone asks for a second result.

The source may do work before yielding a value. A predicate may reject many values before the first result appears. Laziness limits demand; it does not make each request cheap. If no acceptable item ever occurs in an infinite source, asking for one cannot finish. A termination contract must account for that possibility.

A list can be traversed again because it stores its elements. An iterator is a cursor through a computation and is commonly consumed once. A generator function can create a fresh iterator when called again, but that does not rewind an existing one. This distinction affects debugging: printing `list(pipeline)` may consume what a later caller expected to read.

## Measure the work a prefix requires

Compare two designs: build all transformed results and then select a prefix, or request only the needed results. On a finite source of `n` items, the first design reads every item. The second reads through the source position of its last requested accepted result, or through exhaustion if there are too few.

If finding `k` results requires inspecting `p` source values, a lazy filter performs `p` predicate calls and its downstream map performs `k` transformation calls. Under constant-time stages that is work proportional to `p`, not necessarily to `k`. The source itself may have additional production costs. If all input is eventually consumed, both designs may do comparable work; the advantage concerns intermediate storage or early stopping.

The counts below come from a source that notes every value it hands over. Both designs return the squares of the first three multiples of five.

```python
def count_reads(n, k, lazy):
    reads = 0
    def numbers():
        nonlocal reads
        for value in range(1, n + 1):
            reads += 1
            yield value
    wanted = (x * x for x in numbers() if x % 5 == 0)
    result = list(islice(wanted, k)) if lazy else list(wanted)[:k]
    return result, reads

for n in (20, 40, 80):
    assert count_reads(n, 3, lazy=False) == ([25, 100, 225], n), "Building everything reads the whole source."
    assert count_reads(n, 3, lazy=True) == ([25, 100, 225], 15), "Asking for three stops at the third multiple of five."
```

| Source size | Reads, build everything | Reads, ask for three |
|---:|---:|---:|
| 20 | 20 | 15 |
| 40 | 40 | 15 |
| 80 | 80 | 15 |

The lazy count is 15 in every row because the third multiple of five is the fifteenth value, wherever the source ends. Had the accepted values been rarer, the same three results would have cost more reads.

For a prefix returned as a list, storage for those `k` output values is still required. A fixed number of generator stages can retain fixed-size cursor state under bounded-size values, but a generator may itself cache arbitrarily much data. Never conclude that any use of `yield` guarantees constant memory.

## A problem that looks different

A drawing program computes all candidate shapes, then shows just the first screenful. Which work could be delayed until another screenful is requested? Which ordering promise must stay unchanged? The answer depends on whether constructing one candidate requires information about every other candidate; a pipeline cannot remove a global dependency merely by changing syntax.

## Practise

Build the book's same-parity operation, trace requests through a lazy pipeline, evaluate a polynomial from ordered coefficients, and measure actual source pulls in two supplied designs. The last exercise is a preview of a live feed; its prompt says what the preview must contain and how much of the feed it may consume, and leaves the method to you. Predict the frames first, then compare them with what your own program records.

## Recap

**You can now:** Preserve list order, compose sequence stages, state fold direction, and explain the work needed to request a prefix.

**Invariant:** A completed prefix or suffix describes exactly the inputs already visited under the operation's stated ordering rule.

**Complexity achieved:** A finite fold makes one callback per element. Lazy filtering to produce `k` outputs after `p` examined inputs makes `p` predicate calls and `k` downstream map calls, excluding drawing and assuming the stages return normally. Arithmetic and allocation costs remain separate.

**Failure mode:** Consuming a source too early, reading one item past a requested prefix, or mistaking an exhausted iterator for an empty original collection.

**In real software:** Python's built-in `map` and `filter` return iterators that compute each value only when asked, and `itertools.islice` takes a prefix without reading past it.

**Retrieval:** Module 4: how can callers use the same sequence meanings even when the representation changes?

## Check yourself

1. Why can filtering require several source reads for one output?
2. What distinguishes a right fold from a left fold when the operation is subtraction?
3. Which part of a prefix cost depends on the positions of accepted items?

## Reference and licence

The lesson follows SICP §§2.2.1 and 2.2.3 by Harold Abelson and Gerald Jay Sussman with Julie Sussman. The shared [book reference](../../reading/05-sequences.html) also contains other sections; §2.2.2 is taught in Module 6. Examples are translated to Python, with new prose and figures. This lesson is shared under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); it is an independent course, not endorsed by MIT or UC Berkeley.

Python's iterator behavior and generator suspension are documented in the [built-in functions reference](https://docs.python.org/3/library/functions.html#map), [yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions), and [itertools.islice](https://docs.python.org/3/library/itertools.html#itertools.islice).
