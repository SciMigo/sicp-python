# Environment Diagrams

A name tells you which value a program uses only once you know where that name is bound. This module builds the model SICP uses to answer that question: the environment model of evaluation. It replaces "substitute the argument into the body", which stops working as soon as a function can remember something between calls.

You should be able to define and call functions, return a function from a function (module 1), use a dictionary, and follow a loop. We stay with ordinary nested functions: no classes, comprehensions or `exec`. The frames we draw are a model for predicting behaviour. They are not a picture of Python's memory.

## The problem: three functions, two values of x

Here is SICP's first example for the model, in Python. Two of the three functions have a parameter called `x`.

```python
def square(x):
    return x * x

def sum_of_squares(x, y):
    return square(x) + square(y)

def f(a):
    return sum_of_squares(a + 1, a * 2)

assert f(5) == 136
```

The answer is 36 + 100 = 136. On the way there, `x` is 6 inside `sum_of_squares`, 6 again inside the first call to `square`, and 10 inside the second, while the `x` of `sum_of_squares` is still 6 and still needed. That is three separate bindings of one name, two of them alive at the same moment. The question for this module is where each of them lives, and how the program finds the right one.

## The tempting approach: one table, or the caller's names

The simplest picture is a single table from names to values. It fails on this program at once. The second call to `square` would write `x = 10` over the `x = 6` that `sum_of_squares` owns. Here that happens to be harmless, because `sum_of_squares` has already read its `x`; swap the two calls and the answer would change. A model that is right only by luck is not a model.

A second picture gives every call its own table, and resolves a name that is missing there by looking at whoever made the call. That sounds reasonable, and it is wrong for Python.

```python
x = 3

def scale(y):
    return x * y

def run():
    x = 100
    return scale(2)

assert run() == 6
```

??? predict "Before reading on: why 6 and not 200?"
    `scale` was defined at the top level, so its free name `x` is looked up there, where `x` is 3. The `x = 100` inside `run` belongs to the call of `run`. Calling `scale` from inside `run` does not put `run`'s names on the path.

If the caller's names were used, renaming a private variable inside `run` could change what `scale` returns. No function could then be understood by reading it. The rule we need ties a function to the place where it was defined.

## The rules: frames, parents and function values

The environment model has three parts.

A **frame** is a table of bindings, each pairing one name with one value, plus a link to a parent frame. The global frame has no parent. An **environment** is a frame together with the chain of parents behind it.

A **function value** is a pair: the code (parameters and body) and the environment in which the `def` was evaluated. SICP draws it as two circles side by side, one pointing at the code and one at the environment. Evaluating `def square(x): ...` creates that pair and binds the name `square` to it in the current frame. Nothing in the body runs.

**Calling** a function creates a new frame. The frame binds the parameters to the argument values, which the caller has already computed. Its parent is the environment stored in the function value. The body then runs in this new environment.

The parent is the function's own environment, not the caller's frame. That one choice is what makes `run()` return 6. It is called **lexical scope**: the nesting of the program text decides where names are found, and the order of calls at run time does not.

## A visual trace of f(5)

Evaluating `f(5)` creates four frames. All three functions were defined at the top level, so every one of the four has the global frame as its parent.

| Frame | Call | Bindings |
|---|---|---|
| E1 | `f(5)` | a = 5 |
| E2 | `sum_of_squares(6, 10)` | x = 6, y = 10 |
| E3 | `square(6)` | x = 6 |
| E4 | `square(10)` | x = 10 |

```figure
{"type":"environment_diagram","params":{"frame_width":270,"frame_padding":16,"row_height":22,"frames":[{"id":"global","label":"Global","bindings":[{"name":"square","value":"function"},{"name":"sum_of_squares","value":"function"},{"name":"f","value":"function"}]},{"id":"e2","label":"E2: sum_of_squares(6, 10)","parent":"global","bindings":[{"name":"x","value":"6"},{"name":"y","value":"10"}]}],"highlights":{"frames":{"e2":"current"}}},"caption":"E2 while sum_of_squares runs. Its parent is the global frame, where sum_of_squares was defined. E1, E3 and E4 hang off the global frame in the same way."}
```

E2 is created while E1 is still in use, and E3 while E2 is still in use, yet neither is the other's parent. The three `x` bindings sit in three frames, so none can overwrite another. When the body of `sum_of_squares` needs `square`, it does not find it in E2 and follows the parent link to the global frame.

??? predict "Suppose square were defined inside sum_of_squares instead. What would the parent of E3 be?"
    E2. The `def` would run while E2 is the current frame, so the function value would store E2 as its environment, and each call would hang its frame there.

## The invariant: the nearest binding owns the name

To look a name up, begin at the current frame. If its table contains the name, stop. Otherwise move to its parent and repeat, until a binding is found or the chain ends. A nearer binding **shadows** one farther away. Shadowing does not delete or change the farther binding; it only decides which one this lookup selects.

!!! invariant "Every frame already passed lacks the name"
    At each step of a lookup, every frame visited so far has been tested and does not bind the requested name.

Before the first test no frame has been passed, so the statement holds. Moving to a parent keeps it true, because the frame being left was tested first. So when a binding is found, every nearer frame has been ruled out, and the binding is the nearest one on the chain. When the chain ends, every frame on it has been ruled out, and reporting the name as unbound is justified.

The argument assumes a finite chain with no cycles. Those are conditions on the input. The loop does not check them, and the invariant does not make a cyclic chain terminate.

!!! note "Presence is different from truth"
    A binding may hold zero, `False` or `None`. Test whether the name is present, not whether its value is truthy. A missing name and a name bound to `None` are different states.

## Implement a small model

The model is small enough to run. A frame is a record with a `bindings` dictionary and a `parent` index, where `None` marks the end of the chain. The lookup returns the value and the index of the frame that owns it, because ownership is usually what a debugging question is about.

```python
frames = [
    {"bindings": {"x": 3, "unset": None}, "parent": None},
    {"bindings": {"x": 100}, "parent": 0},
    {"bindings": {"y": 2}, "parent": 1},
]

def find_owner(frames, current, name):
    while current is not None:
        bindings = frames[current]["bindings"]
        if name in bindings:
            return bindings[name], current
        current = frames[current]["parent"]
    raise NameError(name)

assert find_owner(frames, 2, "x") == (100, 1)
assert find_owner(frames, 2, "y") == (2, 2)
assert find_owner(frames, 2, "unset") == (None, 0)
assert find_owner(frames, 0, "x") == (3, 0)
```

From frame 2 the name `x` resolves to 100, because frame 1 shadows the root. From frame 0 the same name resolves to 3. `unset` is found at the root although its value is `None`.

SICP's evaluator has two more operations on environments. **Definition** adds a binding to the first frame of the environment, or replaces the binding that frame already has; it never touches a parent. **Assignment** finds the nearest frame that already binds the name and changes that binding; if no frame binds it, that is an error. Lookup, definition and assignment are the whole interface. The lab asks you to build the last two.

## Where Python needs a more precise rule

Python does not walk a chain of dictionaries on every variable read. It decides, when it compiles a function, which names are local to it: any name the body assigns is local, for the whole body. A read that comes before the local has a value raises `UnboundLocalError`. It does not fall back to an outer binding.

```python
level = 11

def broken_level():
    result = level
    level = 3
    return result

try:
    broken_level()
except UnboundLocalError:
    pass
else:
    raise AssertionError("the early read of a local must fail")
```

This is the boundary of the simple model, and worth knowing. When you draw real Python, first classify each name as local (a parameter or an assigned name), enclosing, global or builtin. Then the nearest-binding rule tells you which binding it is.

## Frames as the home of local state

Substitution cannot explain a function whose answers change from call to call. The environment model can. This is SICP's bank-withdrawal example.

```python
def make_withdraw(balance):
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "Insufficient funds"
        balance = balance - amount
        return balance
    return withdraw

W1 = make_withdraw(100)
assert W1(50) == 50
assert W1(60) == "Insufficient funds"
assert W1(40) == 10
```

Follow the frames. Calling `make_withdraw(100)` creates a frame E1 that binds `balance` to 100, with the global frame as parent. The inner `def` runs while E1 is current, so the function value it creates stores E1 as its environment. That value is returned and bound to `W1` in the global frame.

Calling `W1(50)` creates a frame that binds `amount` to 50. Its parent is E1, the environment stored in the function value. The body finds `amount` in the new frame and `balance` one step up, in E1. The assignment changes the binding in E1 to 50.

```figure
{"type":"environment_diagram","params":{"frame_width":270,"frame_padding":16,"row_height":22,"frames":[{"id":"global","label":"Global","bindings":[{"name":"make_withdraw","value":"function"},{"name":"W1","value":"function, env E1"}]},{"id":"e1","label":"E1: make_withdraw(100)","parent":"global","bindings":[{"name":"balance","value":"50"}]},{"id":"call","label":"W1(50)","parent":"e1","bindings":[{"name":"amount","value":"50"}]}],"highlights":{"frames":{"e1":"found"}}},"caption":"At the end of W1(50). The call frame's parent is E1, so the assignment changed balance in E1 from 100 to 50."}
```

When the call returns, its frame is no longer needed: nothing refers to it. E1 is still needed, because the function value bound to `W1` points at it. The next call to `W1` creates a fresh frame for `amount` and finds `balance` at 50. `balance` is a local state variable of this one function value.

The `nonlocal` line is Python's way of asking for assignment in the model's sense: change the nearest enclosing function's binding. Without it, the assignment would make `balance` a local of `withdraw`, and the comparison on the line above would raise `UnboundLocalError`. `nonlocal` cannot create a binding; the enclosing function must already have one.

Now make a second withdrawal function.

```python
W2 = make_withdraw(100)
assert W2(70) == 30
assert W1(5) == 5
```

??? predict "W1 had 10 left. Why did W2(70) return 30 rather than refuse?"
    The second call to `make_withdraw` created its own frame E2, with its own `balance` of 100. `W2`'s environment is E2. `W1` and `W2` share their code and nothing else.

```figure
{"type":"environment_diagram","params":{"frame_width":270,"frame_padding":16,"row_height":22,"frames":[{"id":"e1","label":"E1: environment of W1","bindings":[{"name":"balance","value":"5"}]},{"id":"e2","label":"E2: environment of W2","bindings":[{"name":"balance","value":"30"}]}]},"caption":"After the calls above: W1 has 5 left and W2 has 30. Each call to make_withdraw made one frame; both frames have the global frame as parent (not drawn)."}
```

Two things made the accounts independent: each call to `make_withdraw` created a frame, and each returned function stored the frame it was created in. The two frames spell the variable the same way and that does not matter.

One caution about the picture. Python does not keep the whole frame of a finished call alive for a closure. It keeps a cell for each variable the inner function uses. The diagram says which bindings stay reachable, and that is all a prediction needs.

## Internal definitions

The same rules explain helper functions defined inside a function. This is SICP's square-root procedure, with a loop where the book uses recursion (module 3).

```python
def sqrt(x):
    def good_enough(guess):
        return abs(guess * guess - x) < 0.001

    def improve(guess):
        return (guess + x / guess) / 2

    guess = 1.0
    while not good_enough(guess):
        guess = improve(guess)
    return guess

assert abs(sqrt(2) - 1.4142) < 0.001
assert abs(sqrt(9) - 3) < 0.001
```

Calling `sqrt(2)` creates a frame that binds `x` to 2. The two inner `def`s run in that frame, so `good_enough` and `improve` are bound there, and both function values store that frame as their environment. This gives two properties the model predicts. The helper names are local to the call, so they cannot collide with a `good_enough` defined elsewhere in the program. And the helpers can use `x` without receiving it as an argument: a call to `improve` gets a frame whose parent is the `sqrt` frame, where `x` is found.

## Complexity: count the probes

How much work is a lookup in the explicit model? Count **probes**, the membership tests on binding tables. The check below wraps each table in an instrumented dictionary that counts those tests. It is a stand-in for measuring; in the lab you will count inside a loop you write yourself.

```python
class CountingTable(dict):
    probes = 0
    def __contains__(self, name):
        CountingTable.probes += 1
        return super().__contains__(name)

def probes_for(depth, owner):
    chain = [{"bindings": CountingTable(), "parent": i - 1 if i else None}
             for i in range(depth)]
    if owner is not None:
        chain[owner]["bindings"]["key"] = 1
    CountingTable.probes = 0
    try:
        find_owner(chain, depth - 1, "key")
    except NameError:
        pass
    return CountingTable.probes

assert probes_for(12, 11) == 1
assert probes_for(12, 5) == 7
assert probes_for(12, None) == 12
assert [probes_for(d, None) for d in (3, 6, 12)] == [3, 6, 12]
```

| Chain depth | Name bound in | Probes |
|---:|---|---:|
| 12 | the starting frame | 1 |
| 12 | the seventh frame visited | 7 |
| 12 | no frame | 12 |
| 3, 6, 12 | no frame | 3, 6, 12 |

A lookup visits each frame on the chain at most once, so a chain of depth $d$ costs at most $d$ probes, and a miss costs exactly $d$. If a probe and a parent step each count as one unit, lookup is linear in the depth of the chain in the worst case and constant for a local name. This is a statement about the dictionary-chain model. It is not the cost of a variable read in CPython, which resolves locals and closure variables to fixed slots at compile time.

## A problem that looks different

A test suite uses a helper, `next_ticket()`, that returns 1, 2, 3 and so on. Two test files call it. Each file passes when run alone. Run together, the second file fails: its first ticket is 4, not 1. Nobody edited either file.

Which frame holds the count? Which function values have that frame on their chain? What would have to be true of the environments for each test file to get a sequence of its own? Answer in terms of frames and parents before you think about code.

## Practise

The lab runs on the frame model from this lesson, with different numbers. You will build definition and assignment, create the frame for a call and decide its parent, write a small account whose two operations share one binding, and count probes in a lookup you write. The last task describes a dashboard whose panels misbehave, and leaves the diagnosis to you.

## Recap

**You can now:** Draw the frames a call creates, say which frame owns a name, explain why a function finds its free names where it was defined, and explain how a returned function keeps private state.

**Invariant:** During a lookup, every frame already passed lacks the name, so the first hit is the nearest binding.

**Complexity achieved:** At most $d$ probes for a chain of depth $d$ in the explicit model, and exactly $d$ on a miss. This is not CPython's variable-access cost.

**Failure mode:** Resolving a free name in the caller's frame, testing a value's truth when you meant the name's presence, or expecting an assignment to reach an outer binding without `nonlocal`.

**In real software:** Python's `nonlocal` statement rebinds a variable of the nearest enclosing function, and a function's `__closure__` holds one cell per captured variable.

**Retrieval:** Module 1: why is returning a function different from returning the result of calling it?

## Check yourself

1. `f(5)` creates four frames. Which of them is the parent of the frame for `square(10)`, and why is it not the frame for `sum_of_squares`?
2. After `W1 = make_withdraw(100)` returns, which frame is still reachable, and through what?
3. What changes in your diagram of `withdraw` if the `nonlocal` line is removed?

## Optional background

This lesson follows section 3.2 of *Structure and Interpretation of Computer Programs*; the [book's text with Python translations](../../reading/02-environment-diagrams.html) is kept as a reference.
