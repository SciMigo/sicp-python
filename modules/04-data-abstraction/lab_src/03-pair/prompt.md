This is SICP's exercise 2.4, a second way to build a pair out of nothing but functions. The selector `car` is supplied: it hands the pair a function of two arguments that returns its first. Read it, then write the two missing pieces.

`cons(x, y)` returns a pair. A pair here is a function that takes one argument, `choose`, calls `choose(x, y)` exactly once and returns what it returns. Building a pair calls nothing. `cdr(z)` returns the second part of a pair, in the same style as `car`.

The parts can be any objects, and two pairs must not interfere with each other. The demo draws `car` and `cdr` of one pair; predict both cells before you press Run.