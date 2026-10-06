import random
show_account = lambda *args: None
rng = random.Random(3301)
for _ in range(25):
    starts = [rng.randrange(0, 60), rng.randrange(0, 60)]
    accounts = [make_account(s) for s in starts]
    for pair in accounts:
        assert isinstance(pair, tuple) and len(pair) == 2 and all(callable(f) for f in pair), "make_account returns the pair (withdraw, deposit)."
    expected = starts[:]
    log = []
    for _ in range(30):
        i = rng.randrange(2); withdraw, deposit = accounts[i]
        amount = rng.choice([0, expected[i], expected[i] + 1, rng.randrange(0, 40)])
        if rng.random() < .5:
            expected[i] += amount; want = expected[i]; got = deposit(amount); op = "deposit"
        else:
            op = "withdraw"
            if amount > expected[i]: want = "Insufficient funds"
            else: expected[i] -= amount; want = expected[i]
            got = withdraw(amount)
        log.append(f"account {i}: {op}({amount})")
        assert got == want, "Opened with " + str(starts) + ". After " + "; ".join(log[-4:]) + f" the last call must return {want!r}; it returned {got!r}. Both operations of one account work on one balance, a refused withdrawal changes nothing, and the other account is untouched."
