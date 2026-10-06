The lesson built lookup. Build the other two operations of the frame model. A frame is `{"bindings": {...}, "parent": index_or_None}` and `frames` is a list of them.

`define(frames, current, name, value)` binds `name` in the frame at index `current`. It adds the binding or replaces the one that frame already has, and it never changes any other frame, even when a parent binds the same name.

`assign(frames, current, name, value)` changes an existing binding. Starting at `current`, call `show_scope(frames, index, name)` once for each frame you visit, **before** you test it. At the first frame that binds `name`, store the new value there, stop, and return that frame's index. A binding whose value is `None`, `False` or zero is still a binding. If the chain ends without one, raise `NameError(name)` and leave every frame as it was.

Parent links are indices into the list and are not always the previous index. Chains are finite and have no cycles. Before you press Run: the demo assigns `rate` from frame 2. Which frame's `rate` should change, 0 or 1?
