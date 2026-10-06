This is SICP's exercise 2.34. `coefficients` lists a polynomial's coefficients from the constant term upward, so `[2, -1, 3]` means 2 - x + 3x². Implement `horner(x, coefficients)` to evaluate it. An empty list is the zero polynomial.

Work from the highest coefficient down to the constant. At each one, the new result is that coefficient plus `x` times the result so far. Call `show_horner(index, coefficient, result)` after each combination, once per coefficient. The starter's `show_nothing_yet()` frame is not counted; keep it or delete it. Do not change the caller's list.

There are at most 20 integer coefficients. Predict the value of the demo polynomial before you press Run.