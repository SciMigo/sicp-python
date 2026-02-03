# Environment Diagrams

## SICP Reference
- Chapter 3.2: The Environment Model of Evaluation

## Core Concepts
- Frames: tables of name-value bindings
- The global frame and function-local frames
- Name lookup: walk the parent chain
- How function calls create new frames
- Nested `def` and closure environments
- Mutation and `nonlocal` (preview for later modules)

## Key Examples (Python)
1. **Simple assignment**: `x = 2; y = x + 1` — single frame diagram
2. **Function call**: `square(3)` — new frame with parameter binding
3. **Higher-order function**: `make_adder(3)(4)` — nested frames, parent pointers
4. **Name shadowing**: `x = 1; def f(x): return x + 1` — which `x`?

## Reference Files
- `3.2-environment-model.md`

## Speaker Persona
- Professor Dana: Draws diagrams step by step, "Let's trace through the environment"
- Alex (student): Traces lookups, sometimes confused by shadowing, has "aha" moment about closures
