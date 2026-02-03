# Interpreters — Slide Outline

## Slide 1: Programs That Run Programs
- "When you type `python my_script.py`, what actually happens?"
- An interpreter reads your code and executes it step by step
- We're going to build one — in about 100 lines of Python
- This is the crown jewel of SICP

## Slide 2: Parsing — From Text to Structure
- Input: `"(+ 1 (* 2 3))"` (a string)
- Tokenize: `['(', '+', '1', '(', '*', '2', '3', ')', ')']`
- Parse: `['+', 1, ['*', 2, 3]]` (a nested list / AST)
- Parsing is mechanical — the interesting part is evaluation

## Slide 3: A Calculator Language
- Start simple: numbers and arithmetic operations
- `calc_eval(exp)` — if number, return it; if list, evaluate operator and operands
- `calc_eval(['+', 1, ['*', 2, 3]])` → 7
- **Checkpoint**: Predict `calc_eval(['*', ['+', 1, 2], ['+', 3, 4]])` → 21

## Slide 4: The Eval Function
- Eval dispatches on expression type:
  - Number/string literal → return the value
  - Name → look up in the environment
  - Call expression → eval operator, eval operands, apply
  - Special form → handle specially (if, define, lambda)
- "Eval is a universal function — it can handle any expression"

## Slide 5: The Apply Function
- Apply takes a function and arguments:
  1. Create a new frame (child of the function's definition frame)
  2. Bind parameter names to argument values
  3. Evaluate the function body in the new frame
- This is exactly the environment model from Module 02!

## Slide 6: The Eval/Apply Cycle
- Diagram: Eval calls Apply (for function calls), Apply calls Eval (for the body)
- This mutual recursion is the heart of every interpreter
- "Eval reduces expressions to values, Apply extends the environment"
- **Checkpoint**: Trace `eval(define(square, lambda(x, *(x, x))))` then `eval(square(5))`

## Slide 7: Special Forms
- `if`: evaluate the condition, then evaluate one branch (not both!)
- `define`: add a binding to the current frame
- `lambda`: create a function object (closure) with the current environment
- Special forms are NOT function calls — they have their own evaluation rules

## Slide 8: Building the Interpreter
- Show the complete mini-interpreter: ~100 lines
- `make_frame`, `lookup`, `define`, `eval_all`
- `eval` + `apply` + special form handlers
- Run a program: define functions, call them, get results

## Slide 9: Extending the Language
- Add `unless`: `(unless condition body alternative)`
- Just add a new case to `eval` — three lines of code
- "You're not just using a language anymore — you're designing one"
- More ideas: `let`, `cond`, `and`/`or`, tail call optimization

## Slide 10: The Metacircular Insight
- A Python interpreter written in Python — it works!
- "The language is powerful enough to describe itself"
- This is what makes programming languages special
- Summary of the full SICP journey: functions → data → state → objects → interpreters
- "You now understand computation from the ground up"
