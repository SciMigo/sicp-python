These are SICP's exercises 3.1 and 3.2: two small functions that each keep something between calls.

`make_accumulator(initial)` returns a function that adds its argument to a running total of its own and returns the new total. After each addition call `show_state('accumulated total', [total])`.

`make_monitored(f)` returns a function of one argument that counts how often it is used. For an ordinary argument it adds one to its count, calls `f` once, and returns what `f` returned; after a call that returns normally it draws `show_state('attempted calls', [count])`. If `f` raises, the exception passes through and the attempt still counts. Two arguments are commands and never reach `f`: `'how-many-calls?'` returns the count and draws nothing; `'reset-count'` sets the count to zero, draws `show_state('monitor reset', [0])` and returns 0.

Two accumulators must not share a total, and two monitors must not share a count. Before you press Run, predict the count the demo prints.