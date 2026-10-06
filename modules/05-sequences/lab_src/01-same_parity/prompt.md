This is SICP's exercise 2.20. Implement `same_parity(first, *rest)`: return a new list of every argument that is even when `first` is even, or odd when `first` is odd. Keep them in their original order and keep repeats. There are at most 20 integer arguments.

Keep a `visited` list as you go, and call `show_parity(visited, result)` after each argument, including the first. The upper row shows what has been visited and the lower row what has been kept so far.

Predict the last frame of the demo before you press Run.