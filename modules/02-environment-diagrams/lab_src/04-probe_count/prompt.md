The lesson claimed that a lookup on a chain of depth d makes at most d probes. Measure it on a lookup you write.

Implement `measured_lookup(frames, current, name)`. It looks `name` up from the frame at index `current`, following parent links, and returns `(value, probes)`, where `probes` is the number of membership tests it made on binding tables. Write each test as `name in bindings`: the checks count those tests themselves and compare. On a miss, return `(None, probes)` in this exercise, so that a miss can be measured too. Do not draw inside the function.

The demo looks up a name bound only in the root, from the deepest frame of chains of depth 2, 5 and 9, and draws your three counts as bars. This measures the dictionary-chain model, not the speed of Python's own variable access.
