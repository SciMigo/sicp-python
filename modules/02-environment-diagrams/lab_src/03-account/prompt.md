The lesson's `make_withdraw` returned one function with private state. Write `make_account(balance)`, which returns two: `(withdraw, deposit)`. Both must work on the same balance.

`deposit(amount)` adds to the balance and returns the new balance. `withdraw(amount)` subtracts and returns the new balance, unless the amount is more than the balance; then it returns the string `"Insufficient funds"` and the balance stays as it was. Withdrawing exactly the balance is allowed and leaves 0. Amounts are non-negative integers.

Each call to `make_account` is a separate account: nothing done to one may show in another. Every operation, including a refused withdrawal, calls `show_account(operation, amount, balance)` once, after its effect, with the operation's name (`"withdraw"` or `"deposit"`) and the balance as it now stands.

Before you run the demo, work out the four values it should print for an account opened with 20.
