# Sequences

## SICP Reference
- Chapter 2.2: Hierarchical Data and the Closure Property (sequence operations subset)

## Core Concepts
- Lists as the universal sequence
- Indexing, slicing, list comprehensions
- Sequence processing: map, filter, reduce
- Signal processing metaphor: pipeline of transformations
- Iterators and generators (Python-specific)
- Nested sequences and deep mapping

## Key Examples (Python)
1. **Map/filter/reduce**: `list(map(square, [1,2,3,4]))`, `list(filter(is_even, range(10)))`, `reduce(add, [1,2,3,4])`
2. **List comprehensions**: `[x*x for x in range(10) if x % 2 == 0]` — Python's idiomatic approach
3. **Signal flow**: `sum(map(square, filter(is_odd, range(1, 11))))` — pipeline processing
4. **Generators**: `def naturals(): n = 1; while True: yield n; n += 1` — lazy sequences

## Reference Files
- `2.2-hierarchical-data.md`

## Speaker Persona
- Professor Dana: Shows the elegance of the signal processing view
- Alex (student): Appreciates how pipelines replace loops, builds confidence with comprehensions
