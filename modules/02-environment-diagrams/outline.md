# Environment Diagrams — Slide Outline

## Slide 1: What Happens When Python Runs Code?
- Show a simple program: `x = 2; y = x + 1; print(y)`
- "Where does Python store `x`? How does it find `y`?"
- Motivate: We need a mental model for how names and values work

## Slide 2: Frames — The Fundamental Unit
- A frame is a table: names → values
- The global frame holds top-level bindings
- Diagram: global frame with `x: 2`, `y: 3`
- Every name lives in exactly one frame

## Slide 3: Function Calls Create Frames
- `def square(x): return x * x` → function object in global frame
- `square(3)` → new frame with `x: 3`, parent = global
- Trace: evaluate `x * x` → look up `x` in local frame → 9
- **Checkpoint**: Predict what frame diagram looks like for `square(square(3))`

## Slide 4: Name Lookup Rules
- Rule: look in current frame first, then parent, then parent's parent...
- `x = 1; def f(): return x` → `f()` finds `x` in global frame
- Name shadowing: `x = 1; def f(x): return x + 1` → `f(10)` uses local `x`

## Slide 5: Nested Functions and Closures
- `make_adder(n)` → inner function's parent is `make_adder` frame
- `add_three = make_adder(3)` → `add_three` remembers frame where `n: 3`
- `add_three(4)` → new frame, parent is `make_adder` frame, finds `n: 3`
- Diagram with three frames: global → make_adder → (inner call)

## Slide 6: Lambda Expressions in the Environment
- `f = lambda x: x + 1` — same as `def f(x): return x + 1` in environment terms
- Lambda creates a function object with parent = current frame
- `(lambda x: x * x)(5)` — creates and immediately calls

## Slide 7: Multiple Closures, Shared Frame
- `def make_counter(): n = 0; def inc(): nonlocal n; n += 1; return n; def get(): return n; return inc, get`
- Both `inc` and `get` share the same parent frame
- Preview: `nonlocal` modifies the binding (mutation topic later)
- **Checkpoint**: Draw the environment diagram for `inc, get = make_counter(); inc(); inc(); get()`

## Slide 8: Why This Matters
- Environment model explains: closures, scope, variable lookup, debugging
- Tools: Python Tutor visualizes exactly these diagrams
- Summary: frames form a tree, lookup walks toward the root
- Preview: Next we'll explore recursion — where functions create many frames
