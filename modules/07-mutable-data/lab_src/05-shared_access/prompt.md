A bank service holds one balance behind one password. Its owner wants to give a colleague access under a different password, and that colleague may later do the same for a third person. There is still only one balance: a deposit made by anyone is seen by everyone, and every password that worked before keeps working.

A service is called as `service(password, request)`. The request `'check'` returns `True` or `False` for that password and changes nothing. The requests `'withdraw'` and `'deposit'` return a function of one amount, as in the previous exercise; with a wrong password that function returns `'Incorrect password'`.

Implement `connect(service, old_password, new_password)`. If `old_password` is not valid for `service`, raise `ValueError`. Otherwise return a new service, used in exactly the same way, that answers to `new_password` and to no other. Setting it up must not deposit or withdraw anything, not even zero.

The supplied `run_access` replays a list of joins and operations through your `connect` and draws the number of routes and the latest result after each one. The supplied account is the only place a balance is kept; you cannot read it directly.