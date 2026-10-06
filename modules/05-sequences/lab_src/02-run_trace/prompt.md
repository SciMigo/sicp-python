The supplied `source`, `accept` and `transform` each record an event when they run: a pull, a test, or a map. Complete `run_trace(items, k)` so that it returns the first `k` accepted and transformed values, and no more work happens than that needs.

The starter already resets the trace and emits `('start', k)`. Build the pipeline from the three supplied stages, in that order, without reading the source up front. Each time a result arrives, call `emit("output", value)` straight away. Stop at the `k`-th result or when the source runs out. With `k` equal to 0, nothing is pulled at all.

`items` has at most 20 integers and `k` is between 0 and 20. Answer the question before you run the demo.