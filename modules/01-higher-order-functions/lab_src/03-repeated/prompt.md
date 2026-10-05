This is SICP's exercise 1.43. Implement `repeated(f, n)`: it returns a function that applies `f` to its input `n` times, so `repeated(square, 2)(5)` is 625. `n` is a whole number, zero or more. With `n` equal to 0 the returned function gives back its input and never calls `f`. Calling the returned function twice gives two independent runs.

It must cope with `n = 3000`. Python allows only about 1000 nested calls by default, so 3000 functions wrapped inside one another will fail; find another way.

When `n` is at most 12, call `show_step(i, value)` after the i-th application. The starter already shows step 0, the input. For larger `n`, draw nothing.