Two supplied strategies return the same thing: the first `k` multiples of four, each with 10 added. `eager` builds every result and then takes a prefix; `lazy` asks only for what it needs. Each takes the source function to read from as its last argument.

Implement `profile(strategy, items, k)` returning `(answer, pulls)`: the strategy's answer, and how many items it really pulled from the source. Hand the strategy a function that behaves like the supplied `source` and counts each item as it is yielded. Start every measurement from zero. The checks also run strategies you have not seen.

The demo asks for three results from sources of 16, 40 and 80 items. Before you run it, decide whether the lazy bar should grow with the source.