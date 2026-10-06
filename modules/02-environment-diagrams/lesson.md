# Environment Diagrams

A name tells you which object a program uses only when you know where that name is bound. Two functions can contain the same spelling and refer to different bindings. Two other functions can use different local parameters while reading and changing one shared binding. An environment diagram makes these relationships explicit, so a prediction becomes a sequence of justified steps rather than a guess about whichever value was assigned most recently.

This module assumes you can call functions, return functions, use dictionaries, and follow a loop. Module 1 introduced configured behavior. Here we explain why that behavior keeps the settings it needs and what changes when a setting can be rebound. We use small ordinary Python functions, not classes, comprehensions, annotation scopes, or dynamic evaluation. Our drawn frames are a semantic model; they are not a literal picture of Python's memory layout.

## The problem: which offset is used?

A calibration function adds a configured offset to a reading. A caller happens to have its own variable with the same name. Does the caller's variable override the calibration setting? Work through this program before looking at the assertion. The important question is not which value appears latest in the source file, but which binding the function's expression refers to.

```python
def configure_offset(offset):
    def adjust(reading):
        return reading + offset
    return adjust

adjust = configure_offset(8)

def report(fn):
    offset = 60
    return fn(5)

assert report(adjust) == 13
```

The reading is 5, the configured offset is 8, and the result is 13. The caller's 60 does not participate. Calling a function from somewhere does not redefine where the function's free names come from. This distinction explains many bugs in callbacks: a function can be called much later, by code that knows nothing about the place where it was created.

## The tempting approach: substitute the caller's values

A tempting prediction is to look around the current caller for every name. In `report`, an offset of 60 is easy to see; substituting it would give 65. That rule would make a function's meaning depend on arbitrary local names introduced by callers. Renaming a caller's private variable could change the behavior of an otherwise unchanged function. Ordinary Python functions do not work that way.

Another tempting shortcut is to keep one table of all names. This loses information as soon as two calls bind the same parameter. One invocation can use reading 5 while another uses reading 9, without overwriting each other's parameters. The same spelling is not evidence of the same storage location. We need separate contexts and explicit relationships between them.

Our model therefore has a table of bindings for each relevant context. A binding associates one name with one object. A parent link describes an enclosing lexical context. The word lexical means that nesting in the program determines the relationship, rather than the sequence of callers at runtime. For the subset we draw, those relationships give us a useful route for resolving free names.

## A visual trace

First, calling the configuration function binds its parameter to 8. Defining the nested adjustment function establishes which enclosing binding its free name uses. Returning the function gives the caller a function value; it does not replace that binding with the caller's local values. Later, calling the adjustment function binds its own reading parameter to 5.

```figure
{"type":"environment_diagram","params":{"frame_width":240,"frames":[{"id":"global","label":"Module","bindings":[{"name":"adjust","value":"configured function"}]},{"id":"settings","label":"Configuration context","parent":"global","bindings":[{"name":"offset","value":"8"}]},{"id":"call","label":"Adjustment call","parent":"settings","bindings":[{"name":"reading","value":"5"}]}],"highlights":{"bindings":{"settings.offset":"found","call.reading":"found"}}},"caption":"The adjustment uses its own reading binding and the enclosing offset binding. The caller's offset is outside this lookup path."}
```

For reading, the current call supplies the binding. For offset, the relevant enclosing function supplies it. Adding those values produces 13. The arrows point toward the contexts used to interpret free names. They are not return addresses, and they do not represent the whole call stack. The reporting function may still be running, but its private offset is not on the adjustment function's lexical lookup path.

Now compare two separate calls to the configuration function. They create separate bindings for the same parameter name. Configuring one adjustment with 8 and another with negative 2 gives different behavior without requiring different function bodies. The code is reusable; the remembered bindings distinguish the two configurations.

```python
first = configure_offset(8)
second = configure_offset(-2)
assert (first(5), second(5)) == (13, 3)
assert first(9) == 17
```

## The invariant: the nearest eligible binding owns the name

In our explicit frame model, begin at the current frame. If its binding table contains the requested name, stop. Otherwise follow its parent. Keep going until a binding is found or the chain ends. A nearer binding shadows one farther away. Shadowing does not delete or change the farther binding; it changes which one this lookup selects.

The invariant is that every frame already passed has been checked and contains no binding for the requested name. Initially none has been passed, so the statement is true. Moving to a parent preserves it because the current frame was tested before moving. If a binding is found, all nearer frames have already been ruled out; it is therefore the nearest binding on this chain. If the chain ends, every eligible frame has been checked, so reporting an unbound name is justified.

!!! note "Presence is different from truth"
    A binding can legitimately hold zero, False, or None. Test whether the name is present, not whether its value is truthy. A missing name and a present name holding None are different states.

This reasoning assumes a finite chain without cycles and valid parent links. The invariant does not make an invalid cyclic model terminate. Those are input conditions, not consequences of the loop. When reasoning about a program, state which relationships you assume before using a traversal proof.

## Implement a small model

The following model uses a list of frame records. Each record has a bindings dictionary and a parent index; None marks the end. It returns both the value and the owning frame index, because ownership is often what a debugging question asks. It deliberately leaves out Python's builtins and many language features.

```python
frames = [
    {"bindings": {"offset": 40, "empty": None}, "parent": None},
    {"bindings": {"offset": 8}, "parent": 0},
    {"bindings": {"reading": 5}, "parent": 1},
]

def find_owner(frames, current, name):
    while current is not None:
        bindings = frames[current]["bindings"]
        if name in bindings:
            return bindings[name], current
        current = frames[current]["parent"]
    raise NameError(name)

assert find_owner(frames, 2, "offset") == (8, 1)
assert find_owner(frames, 2, "reading") == (5, 2)
assert find_owner(frames, 2, "empty") == (None, 0)
```

The root's offset of 40 remains present, but the middle frame shadows it. Reading is local to the innermost frame. Empty is present in the root even though its value is None. A good test includes all three cases; testing only a positive local integer can let a wrong lookup rule look correct.

A call in this model creates a fresh parameter table and uses the function's definition environment as its parent. It does not reuse the caller's table. Reusing that table would confuse separate invocations, while linking to the caller would confuse lexical scope with calling order. Argument values are evaluated by the caller before parameter binding; this is distinct from the later resolution of free names inside the function body.

## Where Python needs a more precise rule

The dictionary-chain model is useful, but Python does not perform this exact traversal for every variable read. Python determines which names are local to a function from binding operations in its body. An assignment can make a name local even when the assignment appears after a read. A read before that local binding has received a value raises UnboundLocalError; it does not simply fall back to an outer name.

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
    raise AssertionError("The early local read must fail")
```

This example is a boundary of the simple lookup model, not an exception to be hidden. When drawing real Python, first classify the name: parameter or local, enclosing function name, module global, or builtin. Then apply the appropriate rule. Our lab's frame traversal is an explicit little model with a stated contract; it should not be mistaken for a complete Python interpreter.

A closure likewise does not need to retain an entire finished execution frame. Python functions can retain cells associated with the enclosing variables they use. Our persistent configuration box represents those bindings and their relationships. It says what must remain accessible for the behavior to work, not how much interpreter memory remains allocated. A finished call and an accessible captured binding are different ideas.

## Shared state without global state

Read-only settings are one case. Two returned functions can also share a changing binding. Consider a small register that starts at 12. One operation changes it and another reports it. The modifying operation declares the binding nonlocal, so rebinding affects the enclosing function's variable rather than creating an unrelated local variable.

```python
def make_register(start):
    value = start
    def change(delta):
        nonlocal value
        value += delta
        return value
    def read():
        return value
    return change, read

change_a, read_a = make_register(12)
change_b, read_b = make_register(30)
assert change_a(4) == 16
assert change_a(-7) == 9
assert (read_a(), read_b()) == (9, 30)
```

The two functions from the first factory call share its value binding. The second factory call supplies another binding. Changing the first register cannot affect the second simply because both functions spell the variable `value`. Independence comes from distinct binding ownership, not from different variable names.

```figure
{"type":"environment_diagram","params":{"frame_width":240,"frames":[{"id":"a","label":"Register A: captured bindings","bindings":[{"name":"start","value":"12"},{"name":"value","value":"9"}]},{"id":"b","label":"Register B: captured bindings","bindings":[{"name":"start","value":"30"},{"name":"value","value":"30"}]}],"highlights":{"bindings":{"a.value":"found"}}},"caption":"After changes of +4 and -7 to A, its value is 9. B still reads 30. These are independent captured bindings; unrelated details are omitted."}
```

Without nonlocal, assigning to value in the modifying function would make it local there. The read needed by the augmented assignment would then fail before the update. Nonlocal is not a search through callers: it refers to an existing binding in an enclosing function scope. It cannot create an arbitrary outer variable that does not exist.

## Complexity: measure the model you actually built

Suppose a requested binding lies in the seventh frame visited. Our loop performs seven membership tests. If a chain has twelve frames and the name is absent, it performs twelve membership tests and then raises an error. A local hit performs one test regardless of how many parents exist. These are exact counts for the explicit loop, not timing estimates for Python closures.

```python
def count_probes(depth, owner):
    tables = [{} for _ in range(depth)]
    if owner is not None:
        tables[owner]["key"] = 1
    probes = 0
    for table in tables:
        probes += 1
        if "key" in table:
            return probes
    return probes

assert count_probes(12, 6) == 7
assert count_probes(12, None) == 12
assert count_probes(12, 0) == 1
assert [count_probes(d, None) for d in (3, 6, 12)] == [3, 6, 12]
```

For a chain of depth $d$, there are at most $d$ membership tests and parent steps. Under a model where a dictionary membership test and a parent step each have unit cost, this gives worst-case linear work in the chain depth. We are counting those operations rather than asserting that every real dictionary access has a deterministic constant running time. Drawing and copying whole diagrams add costs that are excluded from this measurement.

## A problem that looks different

Imagine saving callbacks while configuring several display panels. Each callback must later report that panel's own label. The callbacks may all run after configuration has finished. If they all read one changing loop variable, they can end up reporting the final label rather than the label from their own setup. The key debugging question is whether the callbacks refer to distinct bindings or one shared binding.

Creating behavior now is different from evaluating it now. Saving a function does not automatically save a separate snapshot of every object it might later read. Default argument values and separate factory calls can establish different semantics, and mutable objects need additional care. Explain which binding or object is retained before choosing a repair. Renaming the loop variable alone cannot change sharing.

## Practise

The lab makes lookup ownership visible, distinguishes a function's defining environment from its caller, and builds a shared-state service with independent instances. You will instrument actual membership tests at several depths. A final deferred-callback task asks you to preserve distinct behavior after setup ends without naming the method you should use.

## Recap

**You can now:** Identify a name's owner, trace definition-linked calls, distinguish shared bindings from independent factory calls, and explain a read before local assignment.

**Invariant:** Every frame already passed lacks the requested binding; the first hit is the nearest owner on the model's chain.

**Complexity:** At most $d$ membership probes for depth $d$ in the explicit model, excluding drawing. This is not CPython's variable-access cost.

**Failure mode:** Using caller locals for free names, testing values rather than presence, or accidentally sharing one binding among deferred callbacks.

**In real programs:** Python's nonlocal statement lets nested functions rebind an existing enclosing function variable. Its scope is lexical, even when callbacks are invoked elsewhere.

**Retrieval:** Module 1: why is returning a function different from returning the result of calling that function?

## Check yourself

1. What does shadowing change, and what does it leave untouched?
2. Why can a captured variable remain usable after its creating call returns?
3. Which part of your explanation changes when an inner function assigns to a name that it previously only read?

## Optional background

The [original SICP-derived reading](../../reading/02-environment-diagrams.html) remains separate. This independent Python module is not an endorsed university offering.
