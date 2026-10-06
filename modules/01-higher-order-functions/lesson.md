# Higher-order functions: pass the rule, keep the process

## The same work, a different rule

A community workshop receives contributions in units of effort: 2, 5, and 3. One sponsor credits three points per unit plus one point for each contribution. The individual credits are 7, 16, and 10; the total is 33. Another sponsor credits the square of each contribution. Its total is 38. The list stays the same, and the process of visiting each contribution and adding its credit stays the same. Only the rule changes.

```figure
{"type":"array_state","params":{"values":[2,5,3],"indices":true},"caption":"Workshop contributions, in their original order. A credit rule supplies the meaning of each contribution."}
```

This module assumes you can define a Python function, call it, write a loop, and return a value. It does not assume knowledge of closures or recursion. The goal is to recognize which part of a program is a reusable process and which part is a choice of behavior. You will also distinguish creating a function from executing it, trace the order of composed operations, and explain how much work a returned function performs when called.

A **higher-order function** accepts a function as an argument or returns a function as its result. This is a capability of ordinary Python functions, rather than a separate kind of object you must learn to construct. The name describes the role a function plays in a program.

## The obvious approach duplicates the process

We could write one loop that computes sponsor credits and another loop that computes squares. Both initialize a total, visit each element, compute a contribution, add it, and return the total. When we discover a bug in the visit order or need to support an empty list, we have two places to repair.

```python
units = [2, 5, 3]

def sponsor_total(values):
    total = 0
    for value in values:
        total += 3 * value + 1
    return total

def square_total(values):
    total = 0
    for value in values:
        total += value * value
    return total

assert sponsor_total(units) == 33
assert square_total(units) == 38
```

Copying a loop is sometimes a sensible first draft. It helps us see the common structure before choosing an interface. But the differences here are small and precise: two expressions compute the contribution of one value. We can give each expression a function name, then pass that function into one shared process.

This does not automatically make the process faster. We are separating responsibilities so that the rule can change without duplicating the traversal. An abstraction should earn its place by naming a real shared pattern; turning every line into a callback would make the program harder to follow.

## A function value is not its result

The name of a function refers to a callable object. Adding parentheses asks Python to invoke that object on arguments. Those are different operations. If a process needs a rule to apply to future values, give it the callable, not a number that one call happened to return.

```python
def sponsor_credit(value):
    return 3 * value + 1

rule = sponsor_credit
assert callable(rule)
assert rule(2) == 7
result = sponsor_credit(2)
assert result == 7
assert not callable(result)
```

Assigning `rule` does not copy the function's source or run its body. It gives another name to the same function object. A parameter can hold that value just as it can hold a number or a list. Inside a higher-order function, a call such as `rule(value)` uses whichever callable was supplied by the caller.

??? predict "What changes if we pass sponsor_credit(2) instead of sponsor_credit?"
    We pass the integer 7. A later attempt to call that value as a rule raises TypeError. The problem is the argument's role, not the spelling of its name.

## Follow the processed prefix

For the sponsor rule, the total begins at zero. After visiting the first contribution it is 7; after the second it is 23; after the third it is 33. At each point, the total describes exactly the part of the input already processed.

```figure
{"type":"array_state","params":{"values":[7,16,10],"brackets":[{"from":0,"to":1,"label":"processed"}],"indices":true},"caption":"Credits after applying the rule. After two contributions, the processed prefix totals 23; the final contribution has not yet been added."}
```

!!! invariant "The processed-prefix rule"
    Before each iteration, the total is the sum of the credits for exactly the values already visited, with each visited value credited once.

Initially there are no visited values, so zero satisfies the invariant. Suppose it holds before an iteration. Applying the rule to the next value and adding its result extends the total to the next prefix. When no values remain, the processed prefix is the whole input, so the invariant gives the required answer.

Termination has its own reason: a loop over a finite list finishes after one iteration per element, assuming each callback finishes. The invariant proves the meaning of the answer. A loop that terminates but adds each contribution twice would still be wrong.

Here is an alternative way to express the same process using a generator expression and Python's `sum`. The lab asks you to write an explicit loop and expose its intermediate state; this expression is a compact oracle for the lesson's totals.

```python
def credit_total(values, rule):
    return sum(rule(value) for value in values)

assert credit_total(units, sponsor_credit) == 33
assert credit_total(units, lambda value: value * value) == 38
assert credit_total([], sponsor_credit) == 0
```

A **lambda expression** creates a function whose body is one expression. It is useful for a short rule used at one call site. It does not change the rules of evaluation or make a function faster. Prefer a named `def` when the rule needs explanation, multiple statements, or reuse.

## The interface carries a promise

The shared process expects a rule that accepts one input value and returns a numeric contribution. Not every callable meets that contract. A two-argument function is callable but cannot be used here without adapting its interface. A function returning a string is also callable, but its results cannot be added to the initial numeric zero.

Call order can matter. A callback may append to a log, read a changing external value, or raise an exception. Our process visits inputs in order and calls the rule once per visited element. If the rule raises on the second input, the process stops there and propagates the exception; it does not promise a total for the remaining inputs.

For explanations and basic examples we prefer rules without side effects. For checks, an instrumented rule that records its calls is useful: it can expose accidental repeated evaluation that a final numeric result would hide. Correct output on a few inputs is weaker evidence than correct output plus the promised call sequence.

## Return a configured rule

Sometimes the caller wants to set up a rule now and use it later. A workshop might charge at least a minimum amount, while still charging larger contributions at their face value. A factory receives that minimum and returns the rule.

```python
def make_minimum_charge(minimum):
    def charge(value):
        return max(minimum, value)
    return charge

small_event = make_minimum_charge(4)
large_event = make_minimum_charge(9)
assert callable(small_event) and callable(large_event)
assert small_event(2) == 4
assert large_event(2) == 9
assert small_event(11) == 11
assert small_event(2) == 4  # another factory did not overwrite its setting
```

The outer call creates the inner function and returns it. The inner body has not yet processed a contribution. When we call `small_event(2)`, its parameter is 2 and its free variable `minimum` refers to the binding associated with the outer call that created it. Each invocation of the factory creates its own such binding.

A function together with access to its enclosing bindings is called a **closure**. An environment diagram can show those bindings surviving for use by a returned function. That is a semantic model; CPython does not need to preserve an entire old call frame. In CPython, captured variables use cells referenced by the closure.

Closures capture bindings, rather than making an automatic deep copy of every object. If a captured binding refers to a mutable list, changing that list can change the returned function's behavior. A factory that promises a snapshot must copy or summarize the relevant settings deliberately. Module 7 will examine mutation and identity in detail.

## Order is part of composition

Suppose one operation doubles a value and another adds five. Doubling after adding five to 4 gives 18. Adding five after doubling 4 gives 13. The same two operations produce different answers because composition is ordered.

```python
def double(value):
    return 2 * value

def add_five(value):
    return value + 5

assert double(add_five(4)) == 18
assert add_five(double(4)) == 13
```

The notation `f(g(x))` means evaluate `g(x)` first, then give its returned value to `f`. It does not mean that `f` runs first because its name appears first. If a factory constructs the composed operation, construction should store or capture the operations without calling them on a made-up input.

??? predict "Would two adders expose reversed composition order?"
    Usually not: adding two fixed constants gives the same result in either order. Test with operations that do not commute, such as doubling and adding five.

That is a general testing lesson. An example should distinguish the behavior you intend from the plausible mistake you fear. Testing only two adders makes a reversed implementation look correct.

## Repeated behavior and identity

A returned function can also represent a request to apply one rule a chosen number of times. Define the zero case before coding: zero applications should return the original input and should not call the rule. This is the **identity** behavior. It works even when the input is a string, tuple, or object rather than a number.

Each use of the returned function should begin a fresh sequence. Calling it twice must not keep increasing the repetition count or carry the previous result into the next call. The configuration belongs to the factory; the current input and current intermediate result belong to each invocation.

It is tempting to build a chain of nested composed functions. That is mathematically valid, but calling a sufficiently long chain in Python may exceed the recursion limit. An ordinary loop inside the returned function can perform many applications with constant auxiliary storage for the intermediate value. That approach also gives a straightforward place to count calls.

## Count callbacks, not stopwatch readings

Let $n$ be the number of input values. The total-credit process makes exactly $n$ callback calls on a successful traversal. If callback $i$ costs $c_i$, total work includes the traversal plus all of those callback costs. Calling an expensive function through an abstraction does not make its computation constant-time.

Under the teaching model of constant-time callbacks and bounded-size numeric arithmetic, traversal takes $\Theta(n)$ time. An explicit loop needs $O(1)$ auxiliary storage when it keeps only a running total. Recording every prefix for visualization adds storage and drawing work, which is excluded from this bound. The input list's storage is also separate.

```python
def count_credit_calls(values):
    calls = []
    def recorded_rule(value):
        calls.append(value)
        return value + 2
    answer = credit_total(values, recorded_rule)
    assert calls == list(values)
    return answer, len(calls)

for size in (6, 18, 54):
    answer, calls = count_credit_calls(list(range(size)))
    assert calls == size
    assert answer == size * (size - 1) // 2 + 2 * size
```

| Input values | Callback calls | Calls per value |
|---:|---:|---:|
| 6 | 6 | 1 |
| 18 | 18 | 1 |
| 54 | 54 | 1 |

These counts illustrate the invariant and call contract; three measurements do not prove a bound for every input. The loop argument supplies that proof. Python integer arithmetic can take more time as integers grow, so the unit-cost model should not be mistaken for a guarantee about arbitrarily large numeric values.

A repeated operation configured for $k$ applications similarly makes exactly $k$ callback calls each time it is invoked. Creating the returned function can be constant-time if it stores the rule and count, while invoking it has work proportional to $k$ under the same callback model. Always say whether a cost describes setup or later execution.

## A problem that looks different

A display system accepts a formatting rule from each caller. One caller wants a compact label, another wants a verbose label, and another wants to conceal personal information. The system must preserve the order of records and apply the chosen rule once per displayed record. Which responsibility belongs in the shared process, and which belongs in the caller's rule?

This is also the role of Python's `sorted` key argument: the caller supplies a way to obtain a comparison key for each element. A key function computes a value; it does not directly decide the whole ordering process. Recognizing this interface is more useful than memorizing a special syntax for one example.

## Practise

In the visual lab, your own code will expose intermediate totals and the inputs and outputs of composed operations. You will construct a callable, check that repeated invocations remain independent, and measure actual callback calls on unfamiliar sizes. The final task uses fixed settings and later incoming readings; its prompt asks for the behavior and budget without naming the technique.

## Recap

**You can now:** Pass behavior as a function value, return configured behavior, distinguish creation from invocation, and trace ordered composition.

**Invariant:** A processed prefix includes exactly one contribution from each visited input.

**Complexity achieved:** A successful traversal makes exactly $n$ callback calls; it is $\Theta(n)$ time with constant-time callbacks and bounded-size arithmetic. Setup and execution costs are separate.

**Failure mode:** Supplying a function's result instead of the function, reversing composition, or keeping invocation state across calls.

**In real software:** Python's `sorted` accepts a key function. This is a standard example of separating caller-supplied behavior from a shared process.

**Retrieval:** From prerequisite Python: how does `return` differ from `print`, and which one lets a caller use a computed value?

## Check yourself

1. Why can two functions that both add constants be a weak composition test?
2. Does a callback that terminates guarantee that its enclosing traversal computes the intended total?
3. Which costs change if a callback begins sorting a large list internally?

## Optional background

The [original SICP-derived reading](../../reading/01-higher-order-functions.html) is preserved separately. It ranges more widely, including numerical examples not required for this module. This is an independent Python learning module, not an endorsed university offering.
