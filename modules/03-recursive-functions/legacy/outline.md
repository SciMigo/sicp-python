# Recursive Functions — Slide Outline

## Slide 1: Self-Reference
- "How would you define factorial without a loop?"
- `def fact(n): return 1 if n == 0 else n * fact(n - 1)`
- Key insight: a function can call itself — that's recursion

## Slide 2: Tracing Recursive Calls
- Trace `fact(4)` → `4 * fact(3)` → `4 * 3 * fact(2)` → ... → 24
- Call stack visualization: frames stacking up, then unwinding
- **Checkpoint**: Predict the order of print statements in `def fact(n): print(n); return 1 if n == 0 else n * fact(n - 1)` for `fact(4)`

## Slide 3: Anatomy of Recursion
- Every recursive function needs: base case (when to stop) + recursive case (how to reduce)
- `fact(0) = 1` (base), `fact(n) = n * fact(n-1)` (recursive)
- What happens without a base case? → infinite recursion → stack overflow

## Slide 4: Linear vs Tree Recursion
- Linear: each call makes one recursive call → `fact(n)` makes n calls
- Tree: each call makes multiple recursive calls → `fib(n)` makes two
- `def fib(n): return n if n <= 1 else fib(n-1) + fib(n-2)`

## Slide 5: The Fibonacci Tree
- Visualize `fib(5)` as a tree of calls
- Count the nodes: `fib(5)` requires 15 calls, `fib(1)` computed 5 times
- Growth is O(2^n) — exponential!
- **Checkpoint**: How many times is `fib(1)` called when computing `fib(6)`?

## Slide 6: Taming the Tree — Memoization
- Store results in a dictionary: `memo = {}; def fib(n): ...`
- Same recursive structure, but O(n) time
- Each `fib(k)` computed exactly once
- Trade-off: time vs space

## Slide 7: Iteration via Recursion
- `def fib_iter(a, b, count): return a if count == 0 else fib_iter(b, a+b, count-1)`
- O(n) time, O(1) space — no stack buildup
- "State" carried in arguments instead of stack frames
- Python doesn't optimize tail calls, but the idea matters

## Slide 8: Counting Change
- "How many ways to make change for $1.00?"
- Elegant tree recursion: use a coin or skip it
- `count_change(amount, kinds_of_coins)` — recursive decomposition
- Shows the power of recursive thinking for combinatorial problems

## Slide 9: The Recursive Mindset
- Summary: trust the recursion — if the base case is right and each step reduces the problem, it works
- Linear vs tree: understand the shape of your computation
- Memoization: cache to avoid redundant work
- Preview: Next we'll build compound data structures (data abstraction)
