This is SICP's exercise 3.3. You built an account with `deposit` and `withdraw` in Module 2; the new part here is a password in front of it and a dispatch on the request.

Implement `make_account(initial, password)`. Calling `account(given_password, request)` returns a function of one amount. With the right password, `'withdraw'` subtracts the amount if the balance covers it and otherwise returns `'Insufficient funds'`; `'deposit'` adds it. Both return the new balance. With the right password and any other request, raise `ValueError`. With a wrong password, return a function that returns `'Incorrect password'` and changes nothing.

Every function the account hands out works on the same balance, including one saved earlier and called later. Two accounts never share a balance. Compare passwords with `==`.

Each amount function draws one frame with `show_state(label, [balance])`, where the label is `'withdraw'`, `'deposit'`, `'rejected withdrawal'` or `'wrong password'`. Asking the account for a function draws nothing.