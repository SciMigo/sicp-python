# Recursive Functions

## SICP Reference
- Chapter 1.2: Procedures and the Processes They Generate

## Core Concepts
- Recursive function definition: a function that calls itself
- Base case and recursive case
- Linear recursion vs tree recursion
- The substitution model / tracing recursive calls
- Iteration as a special case of recursion (tail calls)
- Memoization to tame exponential recursion

## Key Examples (Python)
1. **Factorial**: `fact(n)` — simplest linear recursion, trace the call stack
2. **Fibonacci**: `fib(n)` — tree recursion, exponential blowup
3. **Counting change**: Elegant tree recursion solving a real problem
4. **Iterative Fibonacci**: `fib_iter(n)` — same result, O(n) time, O(1) space

## Reference Files
- `1.2-procedures-and-processes.md`

## Speaker Persona
- Professor Dana: Patient, "Let's trace through this step by step"
- Alex (student): Traces call stacks, surprised by exponential growth, appreciates memoization
