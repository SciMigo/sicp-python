# Interpreters

## SICP Reference
- Chapter 4.1: The Metacircular Evaluator

## Core Concepts
- What is an interpreter? Programs that run programs
- Parsing: text → tokens → abstract syntax tree (AST)
- The Eval/Apply cycle — the heart of interpretation
- Environments in the interpreter: frames and variable lookup
- Special forms: `if`, `define`, `lambda` (or Python equivalents)
- Extending the language: adding new special forms
- The metacircular insight: an interpreter written in the language it interprets

## Key Examples (Python)
1. **Calculator language**: Parse and evaluate `(+ 1 (* 2 3))` → 7
2. **Eval function**: dispatch on expression type — number, name, call, special form
3. **Apply function**: create a new frame, bind parameters, evaluate body
4. **Adding `unless`**: Extend the interpreter with a new special form
5. **Full mini-interpreter**: ~100 lines of Python that interpret a Scheme-like language

## Reference Files
- `4.1-metacircular-evaluator.md`

## Speaker Persona
- Professor Dana: Reverent about the Eval/Apply cycle, "This is the deepest idea in CS"
- Alex (student): Amazed that interpreters are "just functions", adds a feature to the language
