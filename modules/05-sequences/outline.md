# Sequences — Slide Outline

## Slide 1: Lists Are Everywhere
- Show three different problems: summing, filtering, transforming
- All share the same pattern: process a sequence of values
- Python lists as the universal container: `[1, 2, 3, 4, 5]`

## Slide 2: Map — Transform Every Element
- `def my_map(f, s): return [f(x) for x in s]`
- `my_map(square, [1, 2, 3, 4])` → `[1, 4, 9, 16]`
- Built-in: `list(map(square, [1, 2, 3, 4]))`
- Key idea: separate "what to do" from "how to traverse"

## Slide 3: Filter — Select Elements
- `def my_filter(pred, s): return [x for x in s if pred(x)]`
- `my_filter(is_even, range(10))` → `[0, 2, 4, 6, 8]`
- **Checkpoint**: Predict `list(filter(lambda x: x > 3, [1, 5, 2, 7, 3]))` → `[5, 7]`

## Slide 4: Reduce — Combine All Elements
- `from functools import reduce`
- `reduce(add, [1, 2, 3, 4])` → 10
- `reduce(mul, [1, 2, 3, 4])` → 24
- Trace: `reduce(add, [1,2,3,4])` → `add(add(add(1,2),3),4)`

## Slide 5: The Signal Processing View
- Diagram: source → filter → map → reduce → result
- Example: sum of squares of odd numbers from 1 to 10
- `reduce(add, map(square, filter(is_odd, range(1, 11))))` → 165
- "Each stage processes a stream of values"

## Slide 6: List Comprehensions — Python's Way
- `[expr for var in iterable if condition]`
- Same power as map + filter, often more readable
- `[x*x for x in range(1, 11) if x % 2 == 1]` → `[1, 9, 25, 49, 81]`
- Nested comprehensions: `[(x, y) for x in range(3) for y in range(3) if x != y]`

## Slide 7: Generators — Lazy Sequences
- `def naturals(): n = 1; while True: yield n; n += 1`
- Generators produce values on demand — no list in memory
- `gen = naturals(); next(gen)` → 1, `next(gen)` → 2, ...
- Compose with `map`/`filter` for lazy pipelines
- **Checkpoint**: Write a generator for Fibonacci numbers

## Slide 8: Putting It All Together
- Example: Find all Pythagorean triples with hypotenuse ≤ 20
- `[(a,b,c) for c in range(1,21) for b in range(1,c) for a in range(1,b) if a*a+b*b==c*c]`
- Sequences as a thinking tool: enumerate → filter → transform
- Preview: Next we'll explore trees — hierarchical sequences
