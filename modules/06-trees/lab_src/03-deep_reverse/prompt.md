Implement `deep_reverse(t)`. It returns a **new** hierarchy with the same labels in which the children of every node appear in the opposite order: at the root, and inside every child, all the way down. The input must be left exactly as it was, and the result must not share any node with it.

The demo draws the original and then whatever your function returns. In the original, node names such as `1.0:9` read position, then label. In a correct mirror the root's children read -3, 0, 7 from the left, and the two grandchildren read 2, 9. Reversing only the root's children leaves them as 9, 2.
