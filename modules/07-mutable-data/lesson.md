# Mutable data: the same call, a different history

## A withdrawal remembers

Call a square function twice with 25 and both answers are 625. Call a withdrawal function twice with 25 and the answers may be 75 and 50. The argument stayed the same; something else changed. Section 3.1 of *Structure and Interpretation of Computer Programs* introduces this problem with a bank balance. A program representing an account must remember what happened before the current call.

This lesson assumes the closures and environment frames from Module 2, and the sequence representations from Module 5. You will distinguish changing a binding from changing an object, trace independent and shared state, and explain why counting paths through a structure can differ from counting its objects. We use small integer balances and sequential calls. These examples are models for reasoning, not implementations of secure banking or concurrent transactions.

Start with an explicit state argument. The caller holds the current balance, passes it into a calculation, and keeps the new balance. A rejected withdrawal leaves the old balance intact.

```python
def withdrawal_step(balance, amount):
    if amount > balance:
        return balance, 'Insufficient funds'
    return balance - amount, balance - amount

balance = 100
balance, result = withdrawal_step(balance, 25)
assert (balance, result) == (75, 75), (balance, result)
balance, result = withdrawal_step(balance, 25)
assert (balance, result) == (50, 50), (balance, result)
balance, result = withdrawal_step(balance, 60)
assert (balance, result) == (50, 'Insufficient funds'), (balance, result)
```

The calculation is easy to test because all its inputs are visible. But every caller now has to carry the balance correctly. If two callers keep separate copies, both may believe they can spend the same money. We need one place that owns the current state, and operations that reach that place.

## Assignment reaches an enclosing frame

SICP's `make-withdraw` puts the balance in the environment created by the constructor call. Its returned procedure keeps access to that environment. The Python translation uses `nonlocal` to update the binding in the enclosing function call, rather than create a new local binding inside `withdraw`.

```python
def make_withdraw(balance):
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return 'Insufficient funds'
        balance -= amount
        return balance
    return withdraw

withdraw = make_withdraw(100)
assert withdraw(25) == 75, 'first withdrawal should leave 75'
assert withdraw(25) == 50, 'second withdrawal should leave 50'
assert withdraw(60) == 'Insufficient funds', 'reject overdraft'
assert withdraw(10) == 40, 'rejection must preserve the balance'
```

Module 2 drew this function's frames: the constructor's call creates the `balance` binding, the returned function keeps that frame as its parent, and `nonlocal` makes the assignment land there. Nothing in that picture changes here. What this module adds is the consequence: a function whose answer depends on what it was asked before. One distinction to carry forward: rebinding a captured name needs `nonlocal`; changing an object that a captured name refers to does not, and is a different operation.

!!! invariant "One balance, one history"
    After each completed call, the retained balance equals the initial balance minus all accepted withdrawals through this closure. Rejected withdrawals leave that balance unchanged.

Before any calls the sum of accepted withdrawals is zero. An accepted call subtracts its amount from both sides of the statement. A rejected call changes neither side. This establishes the invariant for any finite sequence of nonnegative withdrawals. It does not prove anything about simultaneous calls, negative amounts or failures halfway through an operation; those need additional contracts.

## Independent accounts and aliases

Two constructor calls create two environments, even when the initial balances are equal. Giving one returned function a second name creates no environment. That second name reaches the same function and, through it, the same retained balance.

??? predict "Two closures start at 100. One has two names. Which calls share a balance?"
    Calls through the two names for one closure share a balance. The separately constructed closure has its own balance, even though it began with the same number.

```python
w1 = make_withdraw(100)
w2 = make_withdraw(100)
alias = w1
results = [w1(40), alias(10), w2(30), w1(15)]
assert results == [60, 50, 70, 35], results
assert alias is w1 and w2 is not w1, 'alias shares; constructor creates'
```

```figure
{"type":"environment_diagram","params":{"frame_width":250,"frame_padding":16,"frames":[{"id":"global","label":"Global","bindings":[{"name":"w1","value":"function, parent E1"},{"name":"alias","value":"the same function"},{"name":"w2","value":"function, parent E2"}]},{"id":"e1","label":"E1: make_withdraw(100)","bindings":[{"name":"balance","value":"35"}]},{"id":"e2","label":"E2: make_withdraw(100)","bindings":[{"name":"balance","value":"70"}]}]},"caption":"After the four calls. Two calls of make_withdraw made two frames, each with its own balance. w1 and alias are two names for one function, so they reach the same frame; w2 reaches the other. Both frames have Global as their parent; those arrows are left out."}
```

An account is therefore more than its current numeric balance. Two accounts can contain equal balances while remaining different objects with different future histories. Conversely, two names can refer to one account. Equality of current contents does not settle identity.

## Why substitution stops being enough

For a pure function, replacing a call by its result preserves the value of a surrounding expression, assuming the function terminates normally. A withdrawal has an additional effect. Replacing it by a number erases the change that later calls observe. You must describe evaluation order and retained state as well as returned values.

SICP contrasts a decrementer that computes from an unchanged initial value with a withdrawal that updates it. The decrementer remembers configuration; the withdrawal remembers history. Closures are capable of either. Returning a function does not automatically make that function stateful.

```python
def make_decrementer(initial):
    return lambda amount: initial - amount

d = make_decrementer(100)
w = make_withdraw(100)
assert [d(20), d(20)] == [80, 80], 'configuration stays fixed'
assert [w(20), w(20)] == [80, 60], 'history changes'
```

This difference matters when designing tests. Checking a fresh account once cannot detect a function that always subtracts from its initial balance. Checking two consecutive operations can. Checking a rejected operation followed by an accepted one can detect an implementation that subtracts before checking available funds. Test histories that distinguish the intended model from a plausible wrong one.

The price of local state is a larger description of behavior. For a pure function, an input-output table may suffice. For an object with history, the same input-output pair can be right or wrong depending on the preceding calls. The benefit is that the owner of the state can enforce its rules in one place.

## Rebinding is not mutation

Python assignment makes a name refer to an object. It does not generally copy that object. A list can change while its aliases keep referring to it. Rebinding one alias to a new list changes only that binding.

```python
a = [1, 2]
b = a
b.append(3)
assert a == [1, 2, 3] and a is b, (a, b)
b = [9]
assert a == [1, 2, 3] and b == [9] and a is not b, (a, b)
```

When `b.append(3)` runs, the object reached through both names grows. When `b = [9]` runs, a new list is created and only `b` is redirected. Drawing two separate boxes after the first assignment would give the wrong prediction. Drawing one box forever after the second would also give the wrong prediction.

A shallow copy gives a new outer container while retaining references to its elements. If those elements are themselves mutable, some sharing remains. The word “copy” is incomplete unless you say which level was copied.

```python
inner = ['a', 'b']
outer = [inner, inner]
copy = outer.copy()
copy[0].append('c')
assert copy is not outer, 'outer container was copied'
assert outer == [['a', 'b', 'c'], ['a', 'b', 'c']], outer
assert copy[0] is outer[1], 'nested object is still shared'
```

??? predict "Would copying outer prevent a later append to inner from appearing in the copy?"
    No. Both outer containers still reach the same inner list. A shallow copy separates the outer container, not all reachable mutable objects.

## Mutable pairs expose the links

SICP section 3.3.1 makes sharing explicit using mutable pairs and operations that replace a pair's first or second field. Our earlier tuple representation cannot replace a field. For this lesson a pair is a two-element Python list. This is an instructional representation of a pair, not Python's own list storage implementation.

```python
def cons(first, rest):
    return [first, rest]

def car(pair):
    return pair[0]

def cdr(pair):
    return pair[1]

def set_car(pair, value):
    pair[0] = value

def set_cdr(pair, value):
    pair[1] = value

shared = cons('a', cons('b', None))
z1 = cons(shared, shared)
z2 = cons(cons('a', cons('b', None)),
          cons('a', cons('b', None)))
set_car(car(z1), 'wow')
set_car(car(z2), 'wow')
assert car(cdr(z1)) == 'wow', 'both fields reach the same pair'
assert car(cdr(z2)) == 'a', 'separate equal structures stay separate'
```

This translates the book's shared-versus-unshared example. Before mutation, a recursive comparison of contents would not explain the difference. After mutation, the difference is observable. A structural picture needs arrows to objects, not just the values currently printed along a path.

```figure
{"type":"linked_list","params":{"type":"singly","nodes":[{"id":"n1","value":"a"},{"id":"n2","value":"b"},{"id":"n3","value":"c"},{"id":"n4","value":"d"}],"highlights":{"n2":"current"},"pointers":[{"node":"n1","label":"x"},{"node":"n3","label":"y"}],"show_null":true},"caption":"Chains x = (a b) and y = (c d) after the rest field of x's last pair, highlighted, was set to y. No pair was created. Every name for x's first pair now reaches four values."}
```

Consider the last link of a chain. Replacing its second field can attach another chain without rebuilding the earlier pairs. Every alias to the first chain now sees the attachment. Copying pairs before attaching would produce the same displayed values for the returned chain but a different effect on aliases. A test that checks only the returned values misses that distinction.

For a proper finite chain of $n$ pairs, finding its last pair needs $n-1$ link traversals when $n>0$. Replacing that final link needs one field update. The whole operation is linear in the first chain's length; the update alone is constant work. These counts assume constant-cost field access. They exclude drawing and do not apply to a cyclic chain, where no last pair exists.

## Count objects, not paths

Sharing also changes traversal costs. SICP exercises 3.16 and 3.17 ask why a naive pair counter can return different counts for structures containing the same number of pairs. The naive rule is to count a pair, then recursively count both fields. It counts a shared object again every time another path reaches it.

Let the first object have two fields containing numbers. Make a second object whose two fields both reach the first; make a third whose two fields both reach the second. There are three distinct objects, but recursive expansion counts seven pair encounters: the top one, two encounters with the middle one, and four with the bottom one.

```figure
{"type":"tree","params":{"node_radius":40,"node_spacing_x":92,"node_spacing_y":100,"root":{"value":"top","children":[{"value":"middle (1st)","children":[{"value":"bottom (1st)"},{"value":"bottom (2nd)"}]},{"value":"middle (2nd)","children":[{"value":"bottom (3rd)"},{"value":"bottom (4th)"}]}]}},"caption":"What the naive counter walks: seven encounters. There are only three pairs. The two middle circles are one object reached by two routes, and the four bottom circles are one object reached by four."}
```

For a stack of $n$ such objects, the naive encounter count is $2^n-1$. You can compute it without running an exponentially large traversal: start at one for the bottom object and double the old count plus one for each new object. The number of distinct objects is just $n$.

```python
rows = []
encounters = 0
for n in range(1, 6):
    encounters = 1 + 2 * encounters
    rows.append((n, encounters))
assert rows == [(1, 1), (2, 3), (3, 7), (4, 15), (5, 31)], rows
```

Remembering which identities have already been expanded avoids this repeated work. Record an identity before following its outgoing fields; otherwise a link back to the current object can recurse forever. Compare identity, not equal contents. Two different pairs can have the same fields and must still both be counted.

Python gives every object an identity you can ask for. `a is b` is true only when both names reach one object, and `id(a)` is a number that is the same only for the same object. Lists cannot be put in a set, but their ids can.

```python
first, second = [1, 2], [1, 2]
assert first == second and first is not second, 'equal contents, two objects'
met = {id(first)}
assert id(first) in met and id(second) not in met, 'a set of ids tells them apart'
```

With a hash set of visited identities, constant-cost field access and expected constant-cost set operations, exploring $V$ distinct pairs follows exactly $2V$ fields and takes expected $O(V)$ time. The visited set uses $O(V)$ space; recursive traversal may also use $O(V)$ stack space and can exceed Python's recursion limit. An explicit work list removes reliance on that limit. Finite cycles are safe only when the traversal remembers identities before expansion.

## State can be observed without changing the worker

A monitoring wrapper receives a function, records each ordinary call and delegates to that function. Its count belongs to the wrapper's own environment. Passing the wrapped function as an argument makes the dependency visible and avoids replacing a module-level name. Two wrappers around the same function should keep independent counts.

An observation is itself stateful. Querying or resetting a count is a different kind of request from calling the worker. A protocol must say whether those requests count, whether exceptions count as attempted calls, and how argument values that resemble commands are handled. The lab fixes those choices explicitly instead of leaving the learner to guess.

Measurements of a mutable structure must also avoid disturbing it. If a counter marks nodes by overwriting their fields, the second run may see a different graph. Keeping the visited identities separately lets the structure remain usable after measurement. Reset that set for each run; yesterday's visited objects do not belong to today's measurement.

## A rejected request is a control path

Python uses `raise` to report an exceptional request and `try`/`except` to handle one at a chosen boundary. An exception skips the normal return path. Handle the specific failure you expect; catching every exception could hide a broken implementation. Here is a separate validation example, not an account operation:

```python
def positive_width(value):
    if value <= 0:
        raise ValueError('width must be positive')
    return value

reports = []
for value in (3, 0, 5):
    try:
        width = positive_width(value)
    except ValueError:
        reports.append('rejected')
    else:
        reports.append(width)
assert reports == [3, 'rejected', 5], reports
```

The `else` suite runs only if the `try` suite completed without the handled exception. In a stateful program, decide what must already have changed when an exception happens. Recording an attempted call before delegation deliberately counts a failed attempt. Installing a new object only after validation deliberately avoids exposing a rejected object. These are different policies; neither follows automatically from the syntax.

## A problem that looks different

A document editor offers a duplicate-view command. Editing a paragraph through either view should update both, but closing one view should leave the other open. Which things should be shared, and which state should belong separately to each view? Sketch objects and references before choosing a class or a function representation.

## Practise

In the lab you build the book's accumulator and monitored function, watch a destructive append change one link while every alias follows, put a password in front of an account, and write the pair counter that counts objects, not paths. The last exercise describes a bank service that several people must share; its prompt says what each of them must be able to do and leaves the design to you.

## Recap

**You can now:** Trace captured state, distinguish identity from equal contents, explain aliasing after mutation and separate distinct objects from repeated traversal encounters.

**Invariant:** The retained balance equals the initial balance minus all accepted withdrawals through every alias to that closure; rejected withdrawals leave it unchanged.

**Complexity achieved:** A finite proper chain needs linear work to find its last pair. A visited-identity traversal of $V$ pairs follows $2V$ fields in expected $O(V)$ time under constant-cost field access and hash-set operations, using $O(V)$ extra space.

**Failure mode:** Copying a value when the model requires shared history, confusing rebinding with mutation, or remembering an object only after following its links.

**In real software:** Python's `nonlocal` declaration targets an enclosing function binding. Mutable default arguments are evaluated when a function is defined, so callers can accidentally share one object; use a `None` default and create the object inside the call when each caller needs its own.

**Retrieval:** Module 2: which environment does a returned function retain, and why can it still find a binding after its creator returns?

## Check yourself

1. Why can two functions with equal initial balances behave differently from two names for one function?
2. A shallow copy passes an equality check. What extra experiment would expose retained sharing?
3. Why must a traversal record an identity before following its fields, and why does equality of contents not replace identity?

## Reference and licence

This lesson follows SICP §§3.1.1 and 3.1.3 and the mutable-pair material in §3.3.1. The [book text for this module](../../reading/07-mutable-data.html) is a separate reference. The Monte Carlo example of §3.1.2, queues, tables, circuit simulation and constraint propagation are outside this lesson's scope. Python's [nonlocal statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement) and [mutable default discussion](https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects) specify the language details used here.

Examples and exercises are adapted from *Structure and Interpretation of Computer Programs*, second edition, by Harold Abelson and Gerald Jay Sussman with Julie Sussman. Shared under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); new prose, Python translations and figures are this course's changes. Independent course; not endorsed by MIT or UC Berkeley.
