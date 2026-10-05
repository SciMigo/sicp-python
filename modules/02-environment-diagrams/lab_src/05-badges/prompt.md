A dashboard is given a list of integer panel prefixes once, at setup. Later, each panel is asked to label readings. Implement `prepare_badges(prefixes)`: return a list with one callable per prefix, in the original order. Calling the callable at position i with a reading x returns the pair `(prefix_i, x)`, where `prefix_i` is the prefix that position had at setup.

Setup finishes before any reading arrives. The caller may change its list afterwards, and that must not change what the panels return. Duplicate prefixes are allowed, separate setups are independent, and an empty list gives an empty list.

The supplied version returns the right number of callables. Run it and look at what they report. The demo draws the prefix each of your callables returns.
