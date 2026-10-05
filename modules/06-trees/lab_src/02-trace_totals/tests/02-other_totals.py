show=lambda *args: None
assert totals(tree(3,[tree(4,[tree(-10)])])) == -3, "Include descendants at every depth."
assert totals(tree(0)) == 0, "Zero is a valid label."
