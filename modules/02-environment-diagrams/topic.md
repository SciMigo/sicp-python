# Environment diagrams: author plan

Follows SICP 3.2 (the environment model of evaluation) with the book's own examples in Python. The original reading (reading/02-environment-diagrams.html) is a reference link only.

## Seven beats
Problem: square / sum_of_squares / f, f(5) = 136, three bindings of x. Naive: one table of names; then "look in the caller" (x = 3 global, x = 100 in run, run() == 6). Rules: frame, environment, function value = code + environment, a call's frame hangs on the function's environment. Trace: the four frames of f(5), as a table plus one figure. Invariant: every frame already passed lacks the name. Implementation: find_owner on a list of frame records. State: make_withdraw, W1 and W2 (SICP 3.2.3). Internal definitions: sqrt with good_enough and improve (SICP 3.2.4), with a loop because recursion is module 3. Complexity: probes per lookup. Transfer teaser: a shared next_ticket() counter across two test files (unsolved, and not the lab's mastery problem).

## Instances
Lesson: f(5) = 136; x = 3 / 100; frames with x = 3, 100 and y = 2; make_withdraw(100) with W1(50), W1(60), W1(40), W2(70), W1(5); sqrt(2), sqrt(9); probe depths 3, 6, 12.
Lab: rate 80 / 6 and reading 3; add_rate defined in frame 0, called from frame 1 (prints 9, not 83); account opened with 20 (demo) and 9 (check); probe depths 2, 5, 9 (demo) and 3, 6, 12 plus 1 to 53 (checks); badge prefixes 4, 9, 2.

## Exercises
1. Build `define` and `assign` (SICP's define and set! on the frame model). The lesson shows lookup only.
2. Trace `call_frame(frames, function, arguments, caller)`: append the call's frame with the function's `env` as parent. Prediction: 9 or 83.
3. Implement `make_account(balance)` returning `(withdraw, deposit)` (SICP 3.1.1), two closures over one binding. The lesson shows the single-function make_withdraw.
4. Measure `measured_lookup`: count `name in bindings` tests; the lesson measures with an instrumented dict stand-in, not a counter in the loop.
5. Mastery `prepare_badges`: deferred callables must keep distinct prefixes. Tell: behaviour must stay distinct after setup has finished. The prompt, hints and questions do not name the technique; the lesson does not mention loops and saved callbacks.

## Check design and limits
Every starter is a stub (the mastery starter is the naive version, as the format allows) and fails every one of its checks. Checks use seeded random chains whose parent links are not always index - 1, values None / False / 0, and compare whole frame lists before and after. Frame checks count pictures from a baseline and read the figure params (highlighted frame, shown bindings before the write). The probe check counts `__contains__` on a dict subclass, so a lookup written with `.get` or try/except is reported as making no membership tests; the prompt says to write `name in bindings`. Attacks tried and rejected: define into the nearest owner, assign by truthiness, assign along index - 1, assign that defines on a miss, call frame hung on the caller, shared bindings dict across calls, account refusing an exact withdrawal, account state in a global, a refused withdrawal that changes the balance, probes computed without `in`, probes not counting the hit. The default-argument solution to the mastery passes, as it should. Checks are feedback, not secure grading.

Model scope: ordinary nested functions, globals, parameters, closures, nonlocal. No classes, comprehensions or exec. Frame inputs are finite, acyclic, with valid parents. Builtins are not modelled. The lesson states that CPython does not walk dictionaries per read and keeps cells, not whole frames.

Figures: straightedge 0.8.0 draws a binding-row highlight band 8 px into the frame header and over the descenders of the row above (row rect top = header + padding - row_height + 4). The lesson avoids it by highlighting whole frames and setting frame_padding 16; the lab helpers do the same.

## Sources
Checked 2026-10-05: Python language reference, https://docs.python.org/3/reference/executionmodel.html (binding, scope, UnboundLocalError); https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement; https://docs.python.org/3/reference/datamodel.html#user-defined-functions (`__closure__` cells). SICP 3.2 from reference/3.2-environment-model.md (examples and the define / set! rules; no prose reused).

Oral anchors: parent of the square(10) frame and why; what keeps E1 reachable after make_withdraw returns; what removing nonlocal changes.
