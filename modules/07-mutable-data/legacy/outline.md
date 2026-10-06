# Mutable Data — Slide Outline

## Slide 1: The World Changes
- So far, our functions have been pure — no side effects
- But real programs need state: bank balances, game scores, caches
- "How do we model things that change over time?"

## Slide 2: Assignment — The `nonlocal` Keyword
- `make_withdraw(balance)` — a function that "remembers" and modifies state
- `nonlocal balance` allows the inner function to rebind `balance`
- `wd = make_withdraw(100); wd(25)` → 75; `wd(25)` → 50
- Environment diagram: `balance` changes in the enclosing frame

## Slide 3: The Bank Account
- Full example: `make_account(balance)` returns `dispatch(message)`
- `dispatch('deposit')(50)` and `dispatch('withdraw')(25)`
- Message passing: functions as objects (preview of OOP)
- **Checkpoint**: Predict the sequence of balances after `acc = make_account(100); acc('deposit')(50); acc('withdraw')(30)`

## Slide 4: Mutable Lists
- Lists support mutation: `lst.append(x)`, `lst.pop()`, `lst[i] = v`
- `a = [1, 2, 3]; a.append(4)` → `a` is now `[1, 2, 3, 4]`
- Contrast with tuples: tuples are immutable

## Slide 5: Aliasing — The Danger
- `a = [1, 2, 3]; b = a` — `a` and `b` point to the SAME list
- `b.append(4)` → `a` is also `[1, 2, 3, 4]`
- Box-and-pointer diagram showing two names, one object
- **Checkpoint**: Predict the output: `a = [1, 2]; b = [a, a]; a.append(3); print(b)`

## Slide 6: Identity vs Equality
- `==` checks value equality: `[1, 2] == [1, 2]` → True
- `is` checks identity (same object): `[1, 2] is [1, 2]` → False
- `a = [1, 2]; b = a; a is b` → True
- Rule: use `is` for `None`, `==` for everything else

## Slide 7: The Mutable Default Trap
- `def f(x, lst=[]): lst.append(x); return lst`
- `f(1)` → `[1]`; `f(2)` → `[1, 2]` (!!)
- The default list is created ONCE, shared across all calls
- Fix: `def f(x, lst=None): if lst is None: lst = []; ...`

## Slide 8: The Cost of Mutation
- With mutation, order of operations matters
- Same expression can give different results at different times
- Harder to reason about, harder to test, harder to parallelize
- Trade-off: mutation enables efficient algorithms and modeling state
- Summary: use mutation deliberately, understand aliasing
- Preview: Next we'll organize mutable state into classes (OOP)
