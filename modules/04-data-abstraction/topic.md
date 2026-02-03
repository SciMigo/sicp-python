# Data Abstraction

## SICP Reference
- Chapter 2.1: Introduction to Data Abstraction
- Chapter 2.2: Hierarchical Data and the Closure Property

## Core Concepts
- Abstraction barriers: separating use from implementation
- Constructors and selectors (the interface)
- Pairs and tuples as the simplest compound data
- Rational number arithmetic as a case study
- Data abstraction violations: reaching through the barrier
- The closure property: combining data to make more data

## Key Examples (Python)
1. **Rational numbers**: `make_rat(n, d)`, `numer(r)`, `denom(r)` — full abstraction barrier
2. **Pairs via functions**: `pair(x, y)` using closures — data without data structures
3. **Points and segments**: Layered abstraction — segments built on points built on pairs
4. **Violation example**: Accessing `r[0]` instead of `numer(r)` — why barriers matter

## Reference Files
- `2.1-data-abstraction.md`
- `2.2-hierarchical-data.md`

## Speaker Persona
- Professor Dana: Emphasizes "program to the interface, not the implementation"
- Alex (student): Tempted to skip the abstraction, learns why barriers matter
