# Higher-order functions: pass the rule, keep the process

## Three sums that are one sum

Add the integers from 1 to 10 and you get 55. Add their cubes and you get 3025. Add the terms $\frac{1}{1\cdot 3} + \frac{1}{5\cdot 7} + \frac{1}{9\cdot 11} + \dots$ up to a first factor of 1000, multiply by 8, and you get 3.1395…, which creeps towards $\pi$. These are the three sums that open section 1.3 of *Structure and Interpretation of Computer Programs*, and they are the same program written three times.

```figure
{"type":"array_state","params":{"values":[1,8,27,64],"indices":false,"brackets":[{"from":0,"to":2,"label":"added so far: 36"}]},"caption":"The cubes of 1, 2, 3 and 4. After three terms the running total is 36; the fourth term, 64, has not been added yet."}
```

This module assumes you can define a Python function, call it, write a loop and return a value. It does not assume closures or recursion. By the end you will be able to pass a function to another function, return a function from a function, say which of the two is happening in a line of code, and count how much work a returned function does when it is finally called.

A **higher-order function** takes a function as an argument or returns one as its result. It is an ordinary Python function; the name describes what it does with other functions.

## Writing it three times

Here are the three sums as a first draft.

```python
def sum_integers(a, b):
    total = 0
    while a <= b:
        total += a
        a += 1
    return total

def sum_cubes(a, b):
    total = 0
    while a <= b:
        total += a * a * a
        a += 1
    return total

def pi_sum(a, b):
    total = 0
    while a <= b:
        total += 1 / (a * (a + 2))
        a += 4
    return total

assert sum_integers(1, 10) == 55
assert sum_cubes(1, 10) == 3025
assert abs(8 * pi_sum(1, 1000) - 3.139592655589782) < 1e-12
```

Lay the three bodies side by side. Each starts a total at zero, visits points from `a` while `a <= b`, adds something computed from the current point, and moves to the next point. Only two things differ: **what is added** (`a`, `a * a * a`, `1 / (a * (a + 2))`) and **how to step** (`a + 1` or `a + 4`).

Copying a loop is a reasonable way to find out what the copies share. Leaving it copied means a mistake in the loop, such as `<` where `<=` was meant, has to be found and fixed three times. Mathematicians saw the same pattern long ago and gave it a name, the sigma notation $\sum_{n=a}^{b} f(n)$, so that they could talk about sums in general. We want the same thing in code: one function that is the sum, with the two differences passed in.

## A function value is not its result

To pass "what is added" into a function, we have to hand over the rule itself, not a number the rule once produced. In Python a function's name refers to a callable object. Putting parentheses after it calls the object. Those are different things.

```python
def cube(x):
    return x * x * x

rule = cube
assert callable(rule)
assert rule(3) == 27

result = cube(3)
assert result == 27
assert not callable(result)
```

`rule = cube` does not run `cube` and does not copy it. It gives the same function object a second name. A parameter can hold a function in exactly the way it can hold a number or a list.

??? predict "What happens if a function that expects a rule is given cube(3) instead of cube?"
    It receives the integer 27. The first time it tries `term(a)` Python raises `TypeError: 'int' object is not callable`. The call that built the argument ran too early.

## One process, two parameters

Give the two differences names, `term` for what is added and `next` for how to step, and the three loops collapse into one.

```python
def summation(term, a, next, b):
    total = 0
    while a <= b:
        total += term(a)
        a = next(a)
    return total

def identity(x):
    return x

def inc(x):
    return x + 1

assert summation(identity, 1, inc, 10) == 55
assert summation(cube, 1, inc, 10) == 3025
assert summation(cube, 5, inc, 4) == 0      # an empty range adds nothing
```

!!! invariant "The running total"
    Before each test of `a <= b`, `total` is the sum of `term(x)` over exactly the points already visited, each counted once.

Before the first test no point has been visited and the total is zero, so the statement holds. If it holds before an iteration, the body adds `term(a)` for the one new point and moves on, so it holds before the next test. When the test fails, every point from the start up to `b` has been visited, and the invariant says the total is the answer.

Termination is a separate question, and here it is the caller's responsibility: `next` has to move `a` past `b` eventually. Pass `identity` as `next` and the loop never ends, although the invariant stays true the whole time.

## Lambda: a rule without a name

`pi_sum` needs a term and a step that nothing else will use. Naming them `pi_term` and `pi_next` would work. A **lambda expression** writes a small function in place, with no name.

```python
def pi_sum(a, b):
    return summation(lambda x: 1 / (x * (x + 2)), a, lambda x: x + 4, b)

assert abs(8 * pi_sum(1, 1000) - 3.139592655589782) < 1e-12
assert (lambda x: x + 4)(1) == 5
```

`lambda x: x + 4` is a function whose body is the single expression `x + 4`. It behaves like the `def` version in every way except that it has no name and can hold only one expression. Use `def` when the rule needs several statements, a docstring, or a second caller.

Once the sum exists as a function, other ideas can be built on it. The area under a curve between `a` and `b` is close to the sum of the curve's height at the middle of each small strip, times the strip's width `dx`:

```python
def integral(f, a, b, dx):
    return summation(f, a + dx / 2, lambda x: x + dx, b) * dx

assert abs(integral(cube, 0, 1, 0.01) - 0.2499875) < 1e-9
assert abs(integral(cube, 0, 1, 0.001) - 0.249999875) < 1e-9
```

The exact area under $x^3$ from 0 to 1 is $\frac14$. Notice that `integral` is itself higher-order: it takes the curve `f` as an argument.

## Functions as general methods

Passing a function is more than a way to shorten sums. A number $x$ is a **fixed point** of $f$ when $f(x) = x$. For some functions you can find one by guessing and applying $f$ again and again until the value stops moving.

```python
import math

def fixed_point(f, guess, tolerance=1e-5):
    while True:
        new = f(guess)
        if abs(new - guess) < tolerance:
            return new
        guess = new

assert abs(fixed_point(math.cos, 1.0) - 0.7390822985224024) < 1e-9
```

`fixed_point` knows nothing about cosines. It is a method for a whole family of problems, and the function you pass selects the problem.

The square root of 2 is a fixed point of $y \mapsto 2/y$, because $y = 2/y$ means $y^2 = 2$. But the search fails: from a guess of 1 the next guess is 2, then 1, then 2, for ever. The repair is to move only half-way each time, replacing $y$ by the average of $y$ and $2/y$.

??? predict "Starting from 1.0, what are the first two guesses when each new guess is the average of y and 2/y?"
    1.5, then about 1.4167. The average of 1 and 2 is 1.5; the average of 1.5 and 2/1.5 = 1.333… is 1.41666….

## Returning a function

Averaging a value with $f$ of that value is a transformation that works for any $f$. So write it as a function that takes $f$ and returns the averaged function.

```python
def average_damp(f):
    def damped(x):
        return (x + f(x)) / 2
    return damped

def square(x):
    return x * x

assert average_damp(square)(10) == 55.0

def sqrt(x):
    return fixed_point(average_damp(lambda y: x / y), 1.0)

assert abs(sqrt(2) - math.sqrt(2)) < 1e-9
```

Read `average_damp(square)(10)` from the left. `average_damp(square)` runs the outer body, which defines `damped` and returns it without calling it. The trailing `(10)` then calls `damped`, which computes the average of 10 and `square(10)`: 55.

When `damped` finally runs, long after `average_damp` has returned, it still finds `f`. A function that keeps access to the variables of the call that created it is a **closure**. Each call of `average_damp` creates its own `f`, so two damped functions do not interfere. Module 2 draws this as a diagram and explains exactly which variable a name refers to.

The same move gives the derivative. The derivative of a function is another function, so `deriv` takes one and returns one; and Newton's method for solving $g(x) = 0$ is then a fixed-point search on a function built from `g`.

```python
def deriv(g, dx=1e-5):
    return lambda x: (g(x + dx) - g(x)) / dx

assert abs(deriv(cube)(5) - 75) < 1e-3

def newtons_method(g, guess):
    return fixed_point(lambda x: x - g(x) / deriv(g)(x), guess)

assert abs(newtons_method(lambda y: y * y - 2, 1.0) - math.sqrt(2)) < 1e-9
```

The body of `newtons_method` uses three ideas from this page: a function passed in (`g`), a function returned (`deriv(g)`), and a general method (`fixed_point`) that neither knows nor cares what it is searching for.

## Order is part of composition

Writing `f(g(x))` means: call `g` first, then give its result to `f`. The name that appears first runs last.

```python
assert square(inc(6)) == 49
assert inc(square(6)) == 37
```

??? predict "Would inc and a function that adds 5 show which of two compositions was reversed?"
    No. Adding 1 then 5 gives the same result as adding 5 then 1. To test order, use two operations that do not commute, such as `square` and `inc`.

Applying one function several times is composition with itself. Zero applications should return the input untouched and call nothing. One practical point for Python: building "apply `f` 3000 times" as 3000 nested calls can exceed the interpreter's recursion limit (about 1000 frames by default in CPython), while a loop inside the returned function has no such limit.

## Count calls, not seconds

How much work does a higher-order function do? Count the calls it makes to the function it was given. `summation` calls `term` once per point, so `integral` with strip width `dx` over an interval of length 1 makes about $1/dx$ calls. Wrapping the function in a counter measures it without changing the answer.

```python
def counted(f):
    calls = [0]
    def wrapper(x):
        calls[0] += 1
        return f(x)
    return wrapper, calls

rows = []
for dx in (0.1, 0.01, 0.001):
    f, calls = counted(cube)
    area = integral(f, 0, 1, dx)
    rows.append((dx, calls[0], abs(area - 0.25)))

assert [calls for _, calls, _ in rows] == [10, 100, 1000]
assert [round(error / dx ** 2, 3) for dx, _, error in rows] == [0.125, 0.125, 0.125]
```

| Strip width `dx` | Calls to `f` | Error |
|---:|---:|---:|
| 0.1 | 10 | 0.00125 |
| 0.01 | 100 | 0.0000125 |
| 0.001 | 1000 | 0.000000125 |

Ten times the calls buys a hundred times less error on this curve: the error is $0.125\,dx^2$ in all three rows. That is a measurement on $x^3$ over $[0, 1]$, not a theorem about every function.

For `summation` the count is exact. With $n$ points it makes $n$ calls to `term` and $n$ to `next`, so its running time is $\Theta(n)$ when each of those calls takes constant time and the numbers stay small enough for arithmetic to be constant-time. It keeps one running total, so it needs $O(1)$ extra space.

`fixed_point` is different: nothing in its code says how many calls it will make. That depends on the function and the tolerance.

```python
def calls_to_converge(f, guess, tolerance=1e-5):
    g, calls = counted(f)
    fixed_point(g, guess, tolerance)
    return calls[0]

assert calls_to_converge(math.cos, 1.0) == 29
assert calls_to_converge(average_damp(lambda y: 2 / y), 1.0) == 4
```

Cosine needs 29 calls from a guess of 1.0; the damped square-root search needs 4. Always say whether a cost belongs to building a function or to calling it: `average_damp(f)` does a constant amount of work, and all the cost arrives when the function it returned is called.

## A problem that looks different

A contact list has to be shown sorted three ways: by surname, by most recent message, and by distance from the viewer. The sorting procedure is the same each time. What would you pass in so that one sort serves all three, and how many times would you expect it to be called for a list of $n$ contacts?

## Practise

In the lab your own code generalises the sum one step further, traces which function runs first in a composition, builds a function that applies another one $n$ times, and measures the calls a fixed-point search really makes. The last exercise describes a service with a work budget and does not say which idea from this page meets it.

## Recap

**You can now:** Pass a function as an argument, return a function configured by its creator, tell creating a function from calling it, and count the calls a higher-order function makes.

**Invariant:** Before each test, the running total is the sum of `term` over exactly the points already visited.

**Complexity achieved:** `summation` over $n$ points makes exactly $n$ calls to `term` and $n$ to `next`: $\Theta(n)$ time with constant-time callbacks and bounded-size numbers, $O(1)$ extra space. Building a function and calling it are costed separately.

**Failure mode:** Passing `f(x)` where `f` was meant; reading `f(g(x))` left to right; a `next` that never passes `b`.

**In real software:** Python's `sorted(items, key=f)` takes the rule as an argument and calls it once per item.

**Retrieval:** From your earlier Python: how does `return` differ from `print`, and which one lets a caller use the value?

## Check yourself

1. In `average_damp(square)(10)`, which call runs the body of `damped`, and what has already finished by then?
2. `summation` terminates on your input. Does that tell you its total is right?
3. Why can the number of calls made by `fixed_point` not be read off its code the way `summation`'s can?

## Reference and licence

This lesson follows section 1.3 of the book, with its examples rewritten in Python. The [book's own text for this section](../../reading/01-higher-order-functions.html) is kept as a reference; it also covers the half-interval method and `let`, which this lesson leaves out.

The examples and exercise statements are adapted from *Structure and Interpretation of Computer Programs*, second edition, by Harold Abelson and Gerald Jay Sussman with Julie Sussman. This lesson is shared under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); its prose, Python translations and figures are this course's changes. Independent course; not endorsed by MIT or UC Berkeley.
