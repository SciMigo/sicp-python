# Recursive Functions

A recursive function can be short and still generate a large process. A few lines may create a chain of waiting calls, branch into thousands of repeated requests, or visit only a small collection of distinct states. Reading the function definition tells you how answers depend on other answers. Understanding the process tells you how much work and storage those dependencies create.

This module assumes that you can follow function calls, loops, and dictionaries, and that you understand separate call contexts from module 2. We will start with a small sum, then count ways of filling a strip. The goal is to justify termination, identify repeated work, and choose an evaluation order that fits Python's runtime. Our drawings expose semantic state; they do not show the interpreter's literal memory layout.

## The problem: what is still waiting?

Suppose a workshop numbers its trays from 1 through n and wants the total of their numbers. One definition says that the total through n is n plus the total through n minus one. The total through zero is zero. This description gives both a base case and a dependency on a smaller instance.

```python
def tray_total(n):
    if n == 0:
        return 0
    return n + tray_total(n - 1)

assert tray_total(0) == 0
assert tray_total(4) == 10
```

For input 4, the outer call cannot perform its addition until the call for 3 returns. That call waits for 2, which waits for 1, which waits for 0. The answer eventually comes back through the waiting additions: zero becomes 1, then 3, then 6, then 10. The arithmetic is easy; the ordering of work is the new idea.

The contract matters. This function accepts nonnegative integers. On that domain, subtracting one reaches zero. A negative input would keep decreasing away from the base case, while some noninteger inputs would never equal zero. A base case written in the source is not by itself a termination argument. We must show that every permitted recursive step moves toward it.

## The direct approach: save pending work in calls

For the small sum, direct recursion is reasonable. Each call remembers its own n and waits to add it after receiving the smaller answer. The program's control flow stores the unfinished computation. This is a linear recursive process: the number of active calls grows with the input, even though every call has only one recursive child.

The recursive definition is not automatically inefficient. It performs one addition per positive tray number, just as a straightforward loop does. Its extra cost is the chain of pending calls. Time and storage are different questions; a program can have reasonable arithmetic work and still reach Python's recursion limit on a large input.

```figure
{"type":"environment_diagram","params":{"frame_width":240,"frames":[{"id":"a","label":"Call for n = 4","bindings":[{"name":"pending addition","value":"4 + child"}]},{"id":"b","label":"Call for n = 3","bindings":[{"name":"pending addition","value":"3 + child"}]},{"id":"c","label":"Call for n = 2","bindings":[{"name":"pending addition","value":"2 + child"}]},{"id":"d","label":"Call for n = 1","bindings":[{"name":"pending addition","value":"1 + child"}]},{"id":"e","label":"Base call for n = 0","bindings":[{"name":"returned value","value":"0"}]}]},"caption":"At the deepest point, four additions are waiting. These boxes show pending calls, not lexical parent links; no parent arrows are drawn."}
```

Notice the distinction from the environment diagrams in module 2. A lexical parent relationship answers where a free name comes from. Pending call work answers what must happen after a child returns. Those relationships need not have the same shape. Calling a globally defined function from another call does not make the caller its lexical parent.

## A visual trace and a correctness argument

A reliable trace records two kinds of event: entry into a smaller problem and return of a completed answer. On entry, n identifies the requested prefix. On return, the result must equal the sum of the integers from 1 through that n. The same call can therefore appear once while waiting and again when its answer is ready.

Correctness follows by induction on the permitted integer input. At zero, the empty sum is zero. Assume the recursive call correctly returns the sum through n minus one. Adding n includes the remaining tray exactly once and changes none of the earlier contributions, so the returned value is the sum through n. Termination and correctness are separate: the decreasing argument shows that a base case is reached, while the induction shows that the reached answers have the intended meaning.

A bad implementation can terminate and return the wrong answer. For example, returning n at every level avoids waiting but discards the smaller sum. Conversely, the mathematical recurrence can be correct while its implementation fails on a large input because the runtime cannot maintain the required depth. Tests should distinguish the numerical contract, the trace, and the resource assumptions.

## Turn pending work into explicit state

The sum also has a compact iterative process. Keep the total already processed and the next tray number. At the start of each iteration, total contains exactly the numbers smaller than next_tray. Adding next_tray extends that completed prefix by one; advancing next_tray preserves the relationship.

```python
def tray_total_loop(n):
    total = 0
    next_tray = 1
    while next_tray <= n:
        total += next_tray
        next_tray += 1
    return total

assert [tray_total_loop(n) for n in range(7)] == [0, 1, 3, 6, 10, 15, 21]
assert all(tray_total_loop(n) == tray_total(n) for n in range(20))
```

When the loop ends, next_tray is n plus one, so the invariant says that total covers the whole requested prefix. The loop has a constant number of integer state variables and no growing Python call chain. This does not mean constant storage in bits: the integers become larger as n grows. We must say which resource model a space claim describes.

An accumulator written with a recursive tail call can describe similarly compact logical state. In a language implementation with suitable tail-call optimization, that need not create a growing stack. CPython and the Python runtime used in these labs do not provide that optimization for these functions. A tail-position call still consumes recursive depth here. Use a loop when you need the corresponding large-input process in Python; raising the recursion limit does not remove the underlying stack growth.

## A branching problem: fill a strip

Now fill a strip of length n with pieces of length 1 or 2. The order of pieces matters: a short piece followed by a long one is a different arrangement from the reverse. There is one arrangement for an empty strip, because choosing no pieces is a valid completed arrangement. Length one also has one arrangement.

For a longer strip, separate arrangements by their last piece. A final piece of length 1 leaves an arrangement of length n minus one; a final piece of length 2 leaves an arrangement of length n minus two. These categories are disjoint and cover every arrangement. Their counts therefore add, giving a recurrence whose recursive calls branch.

```python
def strip_count(n):
    if n < 2:
        return 1
    return strip_count(n - 1) + strip_count(n - 2)

assert [strip_count(n) for n in range(7)] == [1, 1, 2, 3, 5, 8, 13]
```

This function also assumes nonnegative integer n. The expression for n equal to 4 requests lengths 3 and 2; the request for 3 requests 2 and 1. The answer for length 2 is computed more than once. The algorithm sees call occurrences, while the mathematical problem has only a small number of distinct lengths.

```figure
{"type":"tree","params":{"node_radius":32,"node_spacing_x":110,"node_spacing_y":95,"root":{"value":"4","children":[{"value":"3","children":[{"value":"2","children":[{"value":"1"},{"value":"0"}]},{"value":"1"}]},{"value":"2","children":[{"value":"1"},{"value":"0"}]}]}},"caption":"Direct branching for length 4 creates nine call occurrences, but only five distinct lengths (0 through 4). The two occurrences of length 2 repeat the same work."}
```

## Reuse answers without changing the question

Memoization stores an answer after computing it, then returns that answer if the same subproblem is requested again. The cache key must identify everything that determines the result. Here the piece lengths are fixed within the function, so n is sufficient. If the allowed pieces or other settings changed, caching only by n in one shared global dictionary could reuse answers for the wrong problem.

```python
def strip_count_cached(n):
    cache = {0: 1, 1: 1}
    def solve(k):
        if k not in cache:
            cache[k] = solve(k - 1) + solve(k - 2)
        return cache[k]
    return solve(n)

assert strip_count_cached(12) == 233
assert all(strip_count_cached(n) == strip_count(n) for n in range(13))
```

The invariant is that every stored answer is correct for its key. The base entries satisfy it initially. A new entry is stored only after the smaller dependencies return correct answers, so their sum is correct for the new key. A cache hit can safely reuse that completed answer. Partially completed work must not be mistaken for a finished answer; in more general dependency graphs, cycles require a different treatment.

Memoization removes repeated computation, but it does not automatically remove recursive depth. This implementation still initially descends through a chain of smaller lengths. It improves how often a state is computed, not how many ancestors may be waiting. That distinction matters when the largest input is thousands rather than a small classroom example.

## Complexity: call occurrences versus computed states

Let C(n) count every call occurrence in the direct strip function, including base calls. The base counts are one. For larger n, the current call contributes one and its children contribute their counts. For this particular recurrence, the total is twice the number of strip arrangements minus one. We can verify representative values without treating measurements as a proof of the general formula.

```python
def strip_calls(n):
    if n < 2:
        return 1
    return 1 + strip_calls(n - 1) + strip_calls(n - 2)

assert [(n, strip_count(n), strip_calls(n)) for n in (4, 8, 12)] == [
    (4, 5, 9), (8, 34, 67), (12, 233, 465)
]
assert all(strip_calls(n) == 2 * strip_count(n) - 1 for n in range(13))
```

The formula follows by induction: both base cases satisfy it, and substituting the two smaller formulas into the call-count recurrence gives twice the sum of the two arrangement counts minus one. With length n at least two, its arrangement count grows at least as fast as doubling every two increases of length, and at most as fast as doubling at every increase. Thus direct branching creates exponentially many call occurrences as n grows.

The memoized version computes each positive non-base length from 2 through n once, doing one recurrence addition for each such state. It uses linear many additions and cache entries in n under the unit-cost state model. These are not bit-cost claims: exact counts grow in size, so addition and retained integers are not fixed-size objects. Drawing all call occurrences would also add substantial work; our measured algorithm counts exclude drawing.

## Choose an order with no waiting chain

The same strip recurrence can be evaluated from shorter strips toward longer ones. Once the answers for the two preceding lengths are known, the next answer can be computed immediately. Keeping just those two answers avoids both repeated branching and a deep call chain.

```python
def strip_count_bottom_up(n):
    previous, current = 1, 1
    for length in range(2, n + 1):
        previous, current = current, previous + current
    return previous if n == 0 else current

assert all(strip_count_bottom_up(n) == strip_count_cached(n) for n in range(30))
assert strip_count_bottom_up(12) == 233
```

The loop's state window must be described precisely: before processing length k, previous and current hold answers for k minus two and k minus one. Simultaneous assignment uses the old values on the right-hand side. Updating previous first and then adding the already changed previous would lose a dependency. For recurrences that use a wider or irregular set of earlier indices, keep the required table or window rather than assuming two variables always suffice.

## A problem that looks different

A production planner asks how many ordered schedules consume an exact amount of material using permitted batch sizes. Zero remaining material is one completed schedule; a negative remainder is impossible. Different last batches partition the schedules into disjoint categories. Once you identify those dependencies, you can ask whether to recompute them, cache them, or evaluate them in an order that makes all required predecessors available.

The largest input and output representation affect the choice. A small exact calculation may work recursively. A large one may need an iterative order, and a requirement to report a remainder modulo a positive integer keeps intermediate counts bounded. Reducing after each addition preserves the final remainder, but it changes the reported quantity from an exact count to a residue. State that change explicitly.

## Practise

The lab records real descent and return events, traces a different branching recurrence, and checks whether each subproblem is expanded once. You will measure actual non-base expansions of naive and cached processes, then solve a large scheduling-style task under an addition budget. The last prompt states its behavior and constraints without naming the technique.

## Recap

**You can now:** Justify termination, trace pending work, distinguish call occurrences from distinct states, and choose an order that avoids repeated computation and deep Python call chains.

**Invariant:** Each completed cached state has the correct answer; each iterative state window holds the dependencies needed for the next result.

**Complexity:** Direct branching for this strip recurrence has exponentially many calls. Cached or bottom-up evaluation uses linear many recurrence additions in n under a unit-cost arithmetic model, excluding drawing.

**Failure mode:** Missing domain conditions, confusing memoization with stack removal, or reusing cached answers with incomplete keys.

**In real Python:** Recursion depth is limited. A constant number of integer variables does not imply constant bit storage.

**Retrieval:** Module 2: why do two calls to the same function have distinct local parameter bindings?

## Check yourself

1. Can a function terminate on every permitted input yet still compute the wrong answer?
2. Which resource does memoization improve, and which can remain linear in input depth?
3. When would a cache key containing only n be insufficient?

## Optional background

The [original SICP-derived reading](../../reading/03-recursive-functions.html) is preserved separately. This is an independent Python learning module, not an endorsed university offering.
