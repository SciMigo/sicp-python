SICP's exercise 3.16 shows a pair counter that gives 3, 4 or 7 for structures that all contain three pairs, because it counts a pair again every time another path reaches it. Exercise 3.17 asks for one that is right. Write it.

Implement `count_pairs(root, fields)`: the number of distinct pairs reachable from `root`. A pair is a two-element list; anything else is not a pair and is not counted. Read a pair's two parts only by calling `fields(pair)`, and call it at most once for each pair. Each time you count a new pair, call `show_state('pairs counted', [count_so_far])`.

Two pairs with equal contents are still two pairs, so you need to remember which objects you have met, not which values. A structure may contain a cycle, so remember a pair before you follow its parts.

The demo compares the supplied path-counting version with yours on stacks of 3, 5 and 7 pairs. Answer the question before you run it.