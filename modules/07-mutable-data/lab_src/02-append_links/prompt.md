This is the destructive append of SICP's exercise 3.12. A chain is made of pairs `[value, rest]` and ends with `rest` equal to `None`. Implement `append_in_place(first, second)`: walk to the last pair of the first chain and make its `rest` the second chain. Build no new pairs and change no values. Return `first`, or `second` if the first chain is empty.

Answer the question before you run anything.

As you walk, call `show_links(first, second, current)` for each pair you visit, passing the pair itself, starting with the first pair. After changing the link, call `show_links(first, second, 'linked')`. If the first chain is empty, call `show_links(first, second, 'empty')` once and change nothing.

The two chains are separate and have no cycles. Pictured chains have at most eight pairs.