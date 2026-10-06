# Data abstraction: choose a contract before a representation

## Rational arithmetic without knowing the storage

SICP section 2.1 begins with rational numbers. A rational number is a ratio of two integers with a nonzero denominator. We want to add, subtract, multiply, divide and compare these numbers exactly. We could put two integers in a tuple and spread indexing throughout the program. That would work until we changed which integer occupied which position, or decided to store an unreduced fraction instead.

This module assumes functions, tuples, loops and closures from modules 1–3. Its central question is what a caller needs to know about a value. By the end you should be able to specify a constructor and its selectors, explain why a client survives a representation change, and measure where normalization work happens. The examples follow the book: rational numbers, points and segments, pairs implemented with functions, and arithmetic on uncertain intervals.

Start with **wishful thinking**, the book's name for designing with operations we have not implemented yet. Suppose `make_rat(n, d)` constructs a rational number, and `numer(r)` and `denom(r)` select its numerator and denominator. Arithmetic can then be written before we decide how the rational number is stored.

```python
def add_rat(x, y):
    return make_rat(numer(x) * denom(y) + numer(y) * denom(x),
                    denom(x) * denom(y))

def sub_rat(x, y):
    return make_rat(numer(x) * denom(y) - numer(y) * denom(x),
                    denom(x) * denom(y))

def mul_rat(x, y):
    return make_rat(numer(x) * numer(y), denom(x) * denom(y))

def div_rat(x, y):
    if numer(y) == 0:
        raise ZeroDivisionError("cannot divide by a zero rational")
    return make_rat(numer(x) * denom(y), denom(x) * numer(y))

def equal_rat(x, y):
    return numer(x) * denom(y) == numer(y) * denom(x)
```

These bodies can be defined now, but cannot be called until the three interface functions exist. Their formulas follow ordinary fraction arithmetic. Cross multiplication tests equality without converting to a floating-point approximation. Neither equality nor addition needs to know that the parts might be inside a tuple, a dictionary or a function.

## A first representation, then a better one

A tuple is enough for the first implementation. Here the constructor rejects a zero denominator; allowing one would violate the domain before any later arithmetic began.

```python
def make_rat(n, d):
    if d == 0:
        raise ZeroDivisionError("denominator must be nonzero")
    return (n, d)

def numer(r):
    return r[0]

def denom(r):
    return r[1]

one_half, one_third = make_rat(1, 2), make_rat(1, 3)
assert add_rat(one_half, one_third) == (5, 6), "The sum is five sixths."
assert mul_rat(one_half, one_third) == (1, 6), "The product is one sixth."
assert add_rat(one_third, one_third) == (6, 9), "Raw construction leaves the result unreduced."
assert equal_rat(make_rat(6, 9), make_rat(2, 3)), "Different parts can represent the same value."
```

??? predict "Is make_rat(6, 9) == make_rat(2, 3) true with this tuple package?"
    No. The tuples are `(6, 9)` and `(2, 3)`, which Python compares part by part. `equal_rat` says they are equal, because it compares the ratios.

The last two assertions distinguish an abstract value from its concrete parts. Six ninths and two thirds are the same rational number. They are different tuples. Tuple equality is therefore the wrong equality operation for this first package, even though it sometimes happens to agree.

For positive arguments we can reduce in the constructor, using the greatest common divisor from module 3. Integer division by that divisor keeps the parts integral. Normalizing negative arguments requires an additional sign policy; that is exercise 2.1 in the lab, rather than a completed exercise here.

```python
from math import gcd

def make_positive_rat(n, d):
    if n < 0 or d <= 0:
        raise ValueError("this example accepts only n >= 0 and d > 0")
    g = gcd(n, d)
    return (n // g, d // g)

assert make_positive_rat(6, 9) == (2, 3), "Reduction divides both parts by their gcd."
assert make_positive_rat(0, 9) == (0, 1), "Zero has a canonical positive denominator."
```

Dividing both parts by the same nonzero factor preserves the ratio. For zero numerator, the gcd is the positive denominator, giving zero over one. Reduction provides a convenient canonical form, but preserving the ratio is the fundamental requirement. A package may add a canonical-form promise; its clients must know whether that stronger promise is present.

## The barrier is a responsibility boundary

An **abstraction barrier** is the rule that separates callers from storage details. Rational arithmetic calls the constructor and selectors. Those operations alone deal with tuples. Code above that boundary may depend on what a selector means, but may not depend on where it finds its answer.

```figure
{"type":"tree","params":{"node_radius":48,"node_spacing_x":150,"node_spacing_y":115,"root":{"value":"add_rat","children":[{"value":"numer"},{"value":"denom"},{"value":"make_rat"}]}},"caption":"The arithmetic client calls these interface operations. Only their implementations need to know the storage layout; the lines are dependencies, not a recursive call trace."}
```

Writing `x[0]` inside `add_rat` crosses the barrier. Putting that indexing inside `numer` is appropriate: selecting the numerator is exactly its responsibility. The goal is not to eliminate representation knowledge. It is to keep that knowledge in a small place so a change has a small effect.

Here is a second package. It stores named parts rather than tuple positions. The original arithmetic functions are unchanged and still call the same interface names.

```python
def make_rat(n, d):
    if d == 0:
        raise ZeroDivisionError("denominator must be nonzero")
    return {"top": n, "bottom": d}

def numer(r):
    return r["top"]

def denom(r):
    return r["bottom"]

answer = add_rat(make_rat(1, 2), make_rat(1, 3))
assert (numer(answer), denom(answer)) == (5, 6), "Unchanged arithmetic works with the new package."
assert equal_rat(answer, make_rat(10, 12)), "Equality still compares values, not dictionaries."
```

This demonstration replaces the package as a whole. It does not make old tuple values compatible with the new dictionary selectors. A real migration must also convert existing values or supply a documented compatibility layer. A barrier makes changing representation manageable; it does not magically adapt old objects.

## What must the operations promise?

The book asks what is meant by data. A collection of functions with plausible names is not sufficient. They must satisfy laws. For integer `n` and nonzero integer `d`, let `r` be the constructor's result. The exact preservation law can be checked without division:

$$\operatorname{numer}(r)\,d = n\,\operatorname{denom}(r).$$

!!! invariant "The law every representation must keep"
    Whatever `make_rat(n, d)` stores, the parts its selectors return stand for the same ratio as `n` over `d`, and the denominator they return is not zero.

The selected denominator must also remain nonzero. If the interface promises lowest terms and a positive denominator, those are additional laws to test. Checking only one friendly positive example cannot establish them.

A useful test varies signs, zero numerator, reducible inputs and repeated calls. It also checks the clients against a different representation. Otherwise a client that quietly indexes a tuple can pass every arithmetic example and still fail the main purpose of the interface.

A selector also needs a stability promise. Reading the numerator twice should not silently change the rational number. If selecting a part is meant to mutate state, that behavior belongs in the contract rather than appearing as a surprise to arithmetic clients.

The correctness argument for `add_rat` is short. The selectors deliver parts representing the two input values. The numerator formula and denominator product represent their sum. A valid constructor preserves that ratio, even if it changes the concrete parts by reduction. Thus the client produces the correct abstract result without assuming any one layout.

## Points and segments: one boundary above another

Exercise 2.2 builds a line segment from two points, each built from two coordinates. There are two layers. A segment client uses segment selectors; a coordinate calculation uses point selectors. Neither reaches through both layers at once.

```python
def make_point(x, y):
    return (x, y)

def x_point(p):
    return p[0]

def y_point(p):
    return p[1]

def make_segment(start, end):
    return (start, end)

def start_segment(s):
    return s[0]

def end_segment(s):
    return s[1]

def midpoint_segment(s):
    a, b = start_segment(s), end_segment(s)
    return make_point((x_point(a) + x_point(b)) / 2,
                      (y_point(a) + y_point(b)) / 2)

mid = midpoint_segment(make_segment(make_point(1, 2), make_point(5, 8)))
assert mid == (3.0, 5.0), "Average the endpoints independently in each coordinate."
```

```figure
{"type":"tree","params":{"node_radius":44,"node_spacing_x":120,"node_spacing_y":110,"root":{"value":"segment","children":[{"value":"start","children":[{"value":"x = 1"},{"value":"y = 2"}]},{"value":"end","children":[{"value":"x = 5"},{"value":"y = 8"}]}]}},"caption":"Three layers. midpoint_segment asks the segment for its two points and each point for its two numbers. It never looks at how a segment stores points, or how a point stores numbers."}
```

Notice that `midpoint_segment` can keep its body if point storage changes and the point operations preserve their laws. Changing segment storage similarly affects its constructor and selectors. Exercise 2.3 applies this idea to rectangles: perimeter and area should describe geometry while width and height operations describe the chosen representation.

The same principle scales to a hierarchy of types. A point interface hides coordinates; a segment interface hides points; a drawing interface might hide segments. At each layer ask what the next layer needs to know. Exposing a fact because a caller needs it is different from exposing an incidental storage choice.

## A pair does not have to be a tuple

SICP's next surprise is that a function can represent a pair. The representation keeps two values in a closure and responds to a request for one of them. This version uses numeric requests, matching the book's first procedural representation.

```python
def pair(x, y):
    def dispatch(message):
        if message == 0:
            return x
        if message == 1:
            return y
        raise ValueError("pair request must be 0 or 1")
    return dispatch

def first(p):
    return p(0)

def second(p):
    return p(1)

p = pair("north", "south")
assert callable(p), "A pair can be represented by a callable object."
assert first(p) == "north" and second(p) == "south", "The selectors recover the original parts."
```

Module 2 explains why `dispatch` can still find `x` and `y` after `pair` returns: it keeps access to the defining call's bindings. Different pairs have different bindings. Creating a pair does not call a selector; it creates behavior that a selector can call later.

This establishes the pair laws, not a claim that Python implements tuples with closures. The function representation is a teaching device showing that behavior can define a data abstraction. Exercise 2.4 uses a different request: a function passed to the pair decides what to do with its two parts. You will write that version yourself.

## The placement of work matters

The book compares reducing a rational number at construction with reducing when a selector is called. Both can implement the same ratio law. Their costs differ when the same value is selected repeatedly.

??? predict "A fraction is built once and each of its parts is read five times. How many gcd calls does each plan make?"
    Reducing at construction makes one. Reducing at every read makes ten: one for each of the five numerator reads and five denominator reads.

For `n` newly created fractions with `k` later selections of each part, eager reduction performs `n` gcd calls; lazy reduction performs `2nk` gcd calls if each selector recomputes it. If no parts are ever selected, lazy reduction does none. Neither statement counts the internal work of gcd. We measure calls to it, not seconds, and do not treat large-integer arithmetic as constant time.

The choice also affects the canonical-form contract. A lazy package may keep raw parts internally yet always return reduced parts. A client reading the storage directly would observe something outside the public promise, and would defeat both the correctness boundary and the intended cost model.

There is no universally best placement of work. The usage pattern matters. The lab supplies both packages and asks you to measure the calls they really make, because a count worked out on paper measures nothing.

## Uncertain values need a different contract

The extended example in section 2.1.4 represents uncertainty as an interval. Ordered endpoints describe all possible values between them. Addition combines lower endpoints and upper endpoints. Multiplication needs the extremes of all four endpoint products; negative values make choosing only the two visually corresponding endpoints incorrect.

```python
def make_interval(low, high):
    if low > high:
        raise ValueError("endpoints must be ordered")
    return (low, high)

def lower_bound(interval):
    return interval[0]

def upper_bound(interval):
    return interval[1]

def mul_interval(x, y):
    products = [a * b for a in (lower_bound(x), upper_bound(x))
                     for b in (lower_bound(y), upper_bound(y))]
    return make_interval(min(products), max(products))

assert mul_interval(make_interval(-2, 3), make_interval(4, 5)) == (-10, 15), "All four endpoint products determine the bounds."
```

Dividing by an interval containing zero needs an explicit policy; there is no finite bounded reciprocal interval for it. Another subtlety is dependence. If a nonzero uncertain value is divided by itself, the exact expression is one. Treating the two occurrences as independently varying intervals generally widens the result. More occurrences of the same uncertainty can therefore change the bound even when algebra says two exact expressions agree. The interval contract must state whether dependence is tracked. This simple package does not track it.

## A problem that looks different

A map renderer receives either coordinates in pixels or coordinates in meters. Should its drawing loop know both layouts, or should a small set of coordinate operations provide the meaning it needs? Which promises must those operations make about units before representation independence is useful? Do not confuse changing storage with changing the meaning of a coordinate.

## Practise

In the lab you reduce signed fractions and watch Euclid's algorithm do it step by step, write a rectangle and a client that works on someone else's rectangle too, build a pair out of functions, and count where the gcd calls happen in an eager and a lazy package. The last exercise is a small electrical problem with an answer that is correct and still not good enough; its prompt does not say what to change.

## Recap

**You can now:** Specify constructor-selector laws, keep clients above their representation boundary, layer compound types, and measure where an interface performs work.

**Invariant:** Every constructed value satisfies its public laws; clients combine the meanings returned by the interface rather than incidental storage positions.

**Complexity achieved:** Eager reduction makes one gcd call per fraction constructed; uncached lazy reduction makes one per part selected. Those are operation counts, not fixed-cost arithmetic claims. Drawing is excluded.

**Failure mode:** Testing arithmetic on one tuple layout while the client secretly depends on that layout.

**In real software:** Python's `fractions.Fraction` reduces in its constructor and keeps the sign on the numerator, so `Fraction(8, -12)` is `Fraction(-2, 3)`.

**Retrieval:** Module 2: why does each procedural pair retain its own two captured values after its creator returns?

## Check yourself

1. Does the ratio law alone require lowest terms or a positive denominator?
2. When may a constructor implementation index its input, while an arithmetic client may not?
3. Why can two equivalent exact formulas give different interval bounds?

## Reference and licence

This Python lesson follows SICP §§2.1.1–2.1.4, including its rational-number, segment, procedural-pair and interval examples. The book text is [optional reference](../../reading/04-data-abstraction.html). Adapted examples and exercise statements credit Harold Abelson and Gerald Jay Sussman with Julie Sussman, *Structure and Interpretation of Computer Programs*, second edition. This lesson is shared under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), with new prose, Python translations and figures identified as this course's changes. Independent course; not endorsed by MIT or UC Berkeley.
