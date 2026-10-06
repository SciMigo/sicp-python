Two supplied packages store the same fraction. `eager` reduces once, when the fraction is built. `lazy` stores the raw parts and reduces each time a part is read. Both take the gcd function to use as their last argument, and both then read the numerator and the denominator `k` times.

Implement `measure(strategy, n, d, k)` returning `(result, calls)`: the list the strategy returns, and the number of times it really called the gcd function you gave it. Give it a function that behaves exactly like the supplied `gcd`. Count calls as they happen; the checks also run strategies you have not seen.

The demo measures both packages at 0, 3 and 12 reads. Blue bars are eager, purple are lazy. Answer the question before you run it.