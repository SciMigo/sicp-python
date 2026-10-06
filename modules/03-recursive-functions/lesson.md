# Recursive Functions

A recursive function can be six lines long and still start a process that makes two million calls. The definition tells you how one answer depends on other answers. The **process** is what actually unfolds when the definition runs: how many calls are waiting at once, how many are made in total, and how those numbers grow with the input. This module is about reading a definition and seeing its process.

It follows section 1.2 of *Structure and Interpretation of Computer Programs* and uses that section's examples, written in Python: factorial, Fibonacci numbers, counting change, fast exponentiation and Euclid's algorithm. You should be able to define and call functions, write a loop, and explain why two calls to one function have separate parameters (module 2).

## Learn recursion in three rounds

If recursion is new, take the module in three sittings. Each round asks one question.

1. **What is still waiting?** Follow one chain of calls down to its base case and back.
2. **What smaller input can I trust?** Inputs shrink in more than one way.
3. **Which work repeats?** A branching definition can ask the same question many times.

After each round, close the code and say one trace aloud. Predicting what a call returns before pressing Run tells you more than reading the output afterwards.

## Round 1: what is still waiting?

The factorial of $n$ is $n \cdot (n-1) \cdots 2 \cdot 1$, and the factorial of 0 is 1. One observation turns that into a program: $n!$ is $n$ times $(n-1)!$.

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

assert [factorial(n) for n in range(6)] == [1, 1, 2, 6, 24, 120]
assert factorial(6) == 720
```

Run `factorial(4)` by hand. The outer call cannot multiply until `factorial(3)` returns. That call waits for `factorial(2)`, which waits for `factorial(1)`, which waits for `factorial(0)`. Then the answers come back up: 1, 1, 2, 6, 24.

```figure
{"type":"environment_diagram","params":{"frame_width":240,"frames":[{"id":"a","label":"Call for n = 4","bindings":[{"name":"waiting to compute","value":"4 * child"}]},{"id":"b","label":"Call for n = 3","bindings":[{"name":"waiting to compute","value":"3 * child"}]},{"id":"c","label":"Call for n = 2","bindings":[{"name":"waiting to compute","value":"2 * child"}]},{"id":"d","label":"Call for n = 1","bindings":[{"name":"waiting to compute","value":"1 * child"}]},{"id":"e","label":"Base call for n = 0","bindings":[{"name":"returns","value":"1"}]}]},"caption":"The deepest moment of factorial(4): four multiplications are waiting. The boxes are active calls, not the lexical parents of module 2, so no arrows are drawn."}
```

This shape is a **linear recursive process**. The number of waiting multiplications grows in step with $n$, and the interpreter has to remember every one of them.

??? predict "Predict: what does factorial(-1) do?"
    It never reaches the base case: -1, -2, -3, ... move away from 0. Python stops it with a RecursionError. A base case in the source is not a termination argument. You also need every permitted input to move toward it, which is why the contract says "nonnegative integer".

## The same answer from a different process

There is another way to compute $n!$: keep a running product and a counter, and multiply from 1 upward.

```python
def factorial_loop(n):
    product, counter = 1, 1
    while counter <= n:
        product, counter = product * counter, counter + 1
    return product

assert all(factorial_loop(n) == factorial(n) for n in range(20))
```

!!! invariant "Invariant"
    Before each test of the loop condition, `product` equals the factorial of `counter - 1`.

It holds at the start, because $0! = 1$. One pass multiplies by `counter` and then advances it, so it still holds afterwards. The loop stops when `counter` is $n + 1$, and the invariant then says `product` is $n!$.

Here nothing is waiting. Two variables describe the whole computation at every moment; you could stop the machine, write the two numbers on a card, and resume later. SICP calls this a **linear iterative process**: the steps still grow with $n$, but the state does not.

SICP makes a further point that Python changes. In Scheme, a function whose last act is to call itself runs as an iterative process, because the implementation reuses the frame (tail-call optimization). CPython does not, and neither does the Python that runs in these labs: every call, in tail position or not, adds a frame. In Python, write the loop when you want the iterative process.

Correctness of the recursive version is an induction. `factorial(0)` returns 1, which is right. If `factorial(n - 1)` returns $(n-1)!$, then multiplying by $n$ gives $n!$. Termination is a separate fact: the argument decreases by one and is never negative, so it reaches 0. A function can terminate and be wrong (return `n` at every level), and it can be right on paper and still fail on a deep input.

## Round 2: the input can shrink in different ways

Subtracting one is only one way to make an input smaller.

**Shrink by a remainder.** The greatest common divisor of two numbers does not change when the larger is replaced by its remainder on division by the smaller. That is Euclid's algorithm:

```python
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def gcd_steps(a, b):
    return 0 if b == 0 else 1 + gcd_steps(b, a % b)

assert gcd(206, 40) == 2
assert gcd_steps(206, 40) == 4
```

The pairs are (206, 40), (40, 6), (6, 4), (4, 2), (2, 0): four remainders. The second number strictly decreases and never goes below zero, which is the termination argument. In `gcd` nothing waits, since the recursive call's value is returned unchanged; the process is iterative in shape even though the definition is recursive.

**Shrink a window.** To decide whether a sequence reads the same in both directions, compare the two outside values. If they differ, the answer is settled. If they match, only part of the claim is established: the inside may still disagree, so the question passes to the window between them. A window of zero or one elements has nothing left to compare.

```figure
{"type": "environment_diagram", "params": {"frames": [{"bindings": [{"name": "left", "value": "0"}, {"name": "right", "value": "5"}, {"name": "waiting", "value": "inside answer"}], "id": "0", "label": "outside call"}, {"bindings": [{"name": "left", "value": "1"}, {"name": "right", "value": "4"}, {"name": "waiting", "value": "inside answer"}], "id": "1", "label": "inside call"}, {"bindings": [{"name": "left", "value": "2"}, {"name": "right", "value": "3"}, {"name": "waiting", "value": "inside answer"}], "id": "2", "label": "smaller call"}, {"bindings": [{"name": "left", "value": "3"}, {"name": "right", "value": "2"}, {"name": "returns", "value": "True"}], "id": "3", "label": "base call"}]}, "caption": "A six-element sequence whose pairs all match. Each call owns one inclusive window; the window loses two elements per call until left passes right."}
```

**Shrink to a child.** A package holds numbers or other packages. A number is its own total. A package asks each thing inside it for a total and adds the answers. The call for a package does not need to understand everything below it, only how to combine correct answers from its children.

```figure
{"type":"tree","params":{"node_radius":32,"node_spacing_x":115,"node_spacing_y":95,"root":{"value":"total 12","children":[{"value":"4"},{"value":"total 6","children":[{"value":"1"},{"value":"5"}]},{"value":"2"}]}},"caption":"A package holding 4, a package holding 1 and 5, and 2. The inner package finishes with 6 before the outer one can finish with 12."}
```

Before writing any recursive function, write three sentences: what one call promises to return, which inputs need no recursive call, and why every recursive input is smaller. Then trace the smallest example that is not a base case.

## Round 3: tree recursion

The Fibonacci numbers start 0, 1, and each later one is the sum of the two before it. The definition translates directly:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def fib_calls(n):
    if n < 2:
        return 1
    return 1 + fib_calls(n - 1) + fib_calls(n - 2)

assert [fib(n) for n in range(9)] == [0, 1, 1, 2, 3, 5, 8, 13, 21]
assert [(n, fib(n), fib_calls(n)) for n in (5, 10, 20)] == [
    (5, 5, 15), (10, 55, 177), (20, 6765, 21891)
]
assert all(fib_calls(n) == 2 * fib(n + 1) - 1 for n in range(21))
```

This call branches. `fib(4)` asks for `fib(3)` and `fib(2)`; `fib(3)` asks for `fib(2)` again. `fib_calls` counts every call the same recursion makes.

```figure
{"type":"tree","params":{"node_radius":32,"node_spacing_x":110,"node_spacing_y":95,"root":{"value":"4","children":[{"value":"3","children":[{"value":"2","children":[{"value":"1"},{"value":"0"}]},{"value":"1"}]},{"value":"2","children":[{"value":"1"},{"value":"0"}]}]}},"caption":"The calls made by fib(4), labelled by argument: nine calls for five distinct arguments. The whole subtree for 2 appears twice."}
```

??? predict "Predict: fib(20) is 6765. Roughly how many calls does it take?"
    21,891. The count is exact: computing fib(n) this way takes $2 \cdot \text{fib}(n+1) - 1$ calls, and fib(21) is 10,946.

The formula follows by induction. It holds for 0 and 1 (one call each). Write $F_n$ for fib($n$). For larger $n$ the count is one plus the two smaller counts:

$$1 + (2F_n - 1) + (2F_{n-1} - 1) = 2F_{n+1} - 1 .$$

Since fib($n$) grows like $\varphi^n$ with $\varphi \approx 1.618$, so does the number of calls: about 62% more work for each increase of $n$ by one. That is exponential, though slower than doubling. The number of calls *waiting* at any moment is only the depth of the tree, at most $n$. Steps and space are different questions.

The iterative process needs two numbers of state, exactly as `factorial_loop` did:

```python
def fib_loop(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

assert all(fib_loop(n) == fib(n) for n in range(21))
assert fib_loop(90) == 2880067194370816120
assert 2 * fib_loop(91) - 1 == 9320093220751060617
```

Before each pass, `a` and `b` are two consecutive Fibonacci numbers; the simultaneous assignment slides that pair one place along. `fib_loop(90)` takes 90 additions. `fib(90)` would take about $9.3 \times 10^{18}$ calls.

## Counting change

Tree recursion is not just a slow way to compute Fibonacci numbers. Sometimes it is the natural way to see a solution at all. How many ways are there to make change for a dollar from half-dollars, quarters, dimes, nickels and pennies?

Split the ways into two groups that cannot overlap: those that use no coin of the first kind, and those that use at least one. The first group is the same problem with one fewer kind of coin. The second is the same problem for the amount left after handing over one such coin.

```python
def count_change(amount, coins=(1, 5, 10, 25, 50)):
    calls = 0

    def ways(amount, kinds):
        nonlocal calls
        calls += 1
        if amount == 0:
            return 1
        if amount < 0 or kinds == 0:
            return 0
        return ways(amount, kinds - 1) + ways(amount - coins[kinds - 1], kinds)

    return ways(amount, len(coins)), calls

assert count_change(11) == (4, 55)
assert count_change(100) == (292, 15499)
```

There are 292 ways, found with 15,499 calls. An amount of exactly 0 counts as one way (hand over nothing more); a negative amount or no kinds of coin left counts as none. Order does not matter here: a dime then a nickel is the same change as a nickel then a dime, and the "one fewer kind" branch is what prevents counting it twice.

## Remember answers already computed

`fib` repeats work because it forgets. Storing each answer the first time it is computed is called **memoization**. (SICP introduces it later, in chapter 3; it belongs here because it repairs exactly the waste the tree shows.)

```python
def fib_memo(n):
    known = {0: 0, 1: 1}

    def solve(k):
        if k not in known:
            known[k] = solve(k - 1) + solve(k - 2)
        return known[k]

    return solve(n)

assert all(fib_memo(n) == fib(n) for n in range(21))
assert fib_memo(90) == fib_loop(90)
```

Every stored answer is correct for its key, and an answer is stored only after the two it depends on have returned. Each argument from 2 to $n$ is computed once, so there are $n - 1$ additions. Two cautions. The key must name everything the answer depends on; here that is only $n$. And memoization removes repeated work, not depth: `solve` still descends $n$ calls on its first trip down.

## Orders of growth

To compare processes, ask how a resource grows with a measure $n$ of the input. Writing $\Theta(f(n))$ means the resource stays between two constant multiples of $f(n)$ for all large $n$. The model below counts one step per call or loop pass and one unit of space per waiting call or state variable. It treats each arithmetic operation as one step, which ignores that Python integers get longer.

| Process | Steps | Space |
|---|---|---|
| `factorial` | $\Theta(n)$ | $\Theta(n)$ waiting calls |
| `factorial_loop` | $\Theta(n)$ | $\Theta(1)$ variables |
| `fib` | $\Theta(\varphi^n)$ | $\Theta(n)$ waiting calls |
| `fib_loop` | $\Theta(n)$ | $\Theta(1)$ variables |
| `fib_memo` | $\Theta(n)$ | $\Theta(n)$ stored answers |

Doubling $n$ doubles the work of a $\Theta(n)$ process. For a $\Theta(\log n)$ process, doubling $n$ adds a constant amount of work. Exponentiation shows how to get one.

## Exponentiation by squaring

Computing $b^n$ as $b \cdot b^{n-1}$ takes $n$ multiplications. But $b^8$ needs only three: square $b$, square the result, square again. In general $b^n = (b^{n/2})^2$ when $n$ is even, and $b^n = b \cdot b^{n-1}$ when it is odd.

```python
def fast_expt(b, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        half = fast_expt(b, n // 2)
        return half * half
    return b * fast_expt(b, n - 1)

def expt_multiplications(n):
    if n == 0:
        return 0
    if n % 2 == 0:
        return 1 + expt_multiplications(n // 2)
    return 1 + expt_multiplications(n - 1)

assert fast_expt(2, 10) == 1024 and fast_expt(3, 13) == 3 ** 13
assert [expt_multiplications(n) for n in (10, 100, 1000)] == [5, 9, 15]
```

An odd exponent becomes even after one step, and an even one is halved, so the exponent at least halves every two steps. That gives at most $2\log_2 n + 2$ multiplications for $n \ge 1$, which is $\Theta(\log n)$ counting each multiplication as one step.

## Measure the claim

Calls made by `fib`, additions made by `fib_loop`, and multiplications made by `fast_expt`:

| $n$ | `fib` | `fib_loop` | `fast_expt` |
|---:|---:|---:|---:|
| 10 | 177 | 10 | 5 |
| 20 | 21,891 | 20 | 6 |
| 30 | 2,692,537 | 30 | 8 |

```python
assert [fib_calls(n) for n in (10, 20, 30)] == [177, 21891, 2692537]
assert [expt_multiplications(n) for n in (10, 20, 30)] == [5, 6, 8]
```

Three rows are an illustration. The induction and the halving argument above are what establish the growth.

## Recursion depth in Python

Python limits how many calls may be waiting at once. CPython's default limit is 1,000 frames, and the Python that runs in your browser has its own, different limit. `factorial(5000)` fails in standard Python with a RecursionError although the definition is correct, while `factorial_loop(5000)` is fine. Raising the limit with `sys.setrecursionlimit` moves the wall; it does not make deep recursion safe. When the depth grows with the input, and the input may be large, use a process whose state is explicit.

## A problem that looks different

Someone picks a whole number from 1 to 1,000 and will answer only "higher", "lower" or "correct". How many questions do you need in the worst case, and what happens to that number when the range becomes 1 to 1,000,000? Say which input measure shrinks with each question, and by how much, before you compute anything.

## Practise

The lab has three rounds, like the lesson, on different functions. In round 1 your own code draws its stack of waiting calls. In round 2 you write a shrinking-window recursion and a nested-container recursion. In round 3 you trace a branching recurrence that is not Fibonacci, make it compute each state once, measure both versions, and finish with a counting problem whose inputs are far too deep to recurse on.

## Recap

**You can now:** Tell a recursive definition from the process it generates, trace waiting calls, argue termination and correctness separately, and recognise repeated work in a branching recursion.

**Invariant:** In the iterative factorial, `product` equals the factorial of `counter - 1` before every test of the loop condition. In a memo table, every stored answer is correct for its key.

**Complexity achieved:** Counting one step per call or loop pass: recursive factorial takes $\Theta(n)$ steps and $\Theta(n)$ waiting calls; tree-recursive fib makes exactly $2\,\text{fib}(n+1) - 1$ calls, which is $\Theta(\varphi^n)$; the loop and the memoized version take $\Theta(n)$ additions; exponentiation by squaring takes $\Theta(\log n)$ multiplications.

**Failure mode:** A base case that some permitted input never reaches; assuming memoization or a tail call removes Python's call depth; a memo key that leaves out something the answer depends on.

**In real software:** CPython enforces a recursion limit (1,000 by default, read with `sys.getrecursionlimit()`) and does not optimize tail calls.

**Retrieval:** Module 2: why do two calls to the same function have distinct local parameter bindings?

## Check yourself

1. `factorial` and `factorial_loop` both take $\Theta(n)$ steps. What exactly differs between their processes?
2. Why does `count_change` not count "dime then nickel" and "nickel then dime" as two ways?
3. Which resource does memoizing `fib` improve, and which one stays proportional to $n$?

## Reference and licence

This lesson follows section 1.2 of the book and uses its examples. The [book's own text](../../reading/03-recursive-functions.html), with the Scheme originals, is kept as a reference; it goes further, into testing for primality.

The examples and exercise statements are adapted from *Structure and Interpretation of Computer Programs*, second edition, by Harold Abelson and Gerald Jay Sussman with Julie Sussman. This lesson is shared under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); its prose, Python translations and figures are this course's changes. Independent course; not endorsed by MIT or UC Berkeley.
