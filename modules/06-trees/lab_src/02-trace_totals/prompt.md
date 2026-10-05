`totals(t)` returns the sum of every label in the hierarchy, internal labels included. Answer the two predictions first, on paper, from the demo hierarchy drawn by the starter: root 4 with children 7, 0 and -3, where the child labelled 0 has two children labelled 9.

Then implement `totals`. Pass `path + (i,)` and `whole` when you descend, and call `show(whole, path, result)` once per call, after that call's sum is known. The frames show completion, not entry into a call. Step through them and compare the order with your prediction.
