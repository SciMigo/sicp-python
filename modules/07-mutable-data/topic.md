# Mutable Data

## SICP Reference
- Chapter 3.1: Assignment and Local State
- Chapter 3.3: Modeling with Mutable Data

## Core Concepts
- Assignment changes the value bound to a name
- `nonlocal` — modifying bindings in enclosing scopes
- Identity vs equality: `is` vs `==`
- Mutable default arguments pitfall
- Lists are mutable: `append`, `extend`, `pop`, `sort`
- Aliasing: two names pointing to the same object
- The cost of mutation: reasoning becomes harder

## Key Examples (Python)
1. **Bank account**: `make_account(balance)` with `withdraw` and `deposit` — state via closure + `nonlocal`
2. **Aliasing**: `a = [1, 2, 3]; b = a; b.append(4)` — both see the change
3. **Identity vs equality**: `[1, 2] == [1, 2]` is True, `[1, 2] is [1, 2]` is False
4. **Mutable default trap**: `def f(x, lst=[])` — shared across calls

## Reference Files
- `3.1-assignment-local-state.md`
- `3.3-mutable-data.md`

## Speaker Persona
- Professor Dana: Careful about the trade-offs of mutation, draws environment diagrams
- Alex (student): Gets bitten by aliasing, learns to distinguish identity from equality
