from scimigo import _frame_count, _frame
withdraw, deposit = make_account(9)
before = _frame_count()
got = [deposit(4), withdraw(20), withdraw(13), deposit(2)]
assert got == [13, "Insufficient funds", 0, 2], f"Opened with 9: deposit(4), withdraw(20), withdraw(13), deposit(2) must return [13, 'Insufficient funds', 0, 2]; got {got}."
recorded = _frame_count() - before
assert recorded == 4, f"Each of the four operations, including the refused withdrawal, draws once; {recorded} pictures were recorded."
steps = [("deposit", 4, 13), ("withdraw", 20, 13), ("withdraw", 13, 0), ("deposit", 2, 2)]
for j, (operation, amount, balance) in enumerate(steps):
    objects = _frame(before + j)
    fig = next(o for o in objects if o["kind"] == "figure")["params"]
    shown = fig["frames"][0]["bindings"]
    assert shown == [{"name": "balance", "value": str(balance)}], f"Picture {j + 1} ({operation} {amount}) must show balance = {balance}, the balance after the operation; it shows {shown}."
    caption = operation + " " + str(amount) + ": balance is " + str(balance)
    assert any(o["kind"] == "text" and o["value"] == caption for o in objects), f"Picture {j + 1} must be captioned '{caption}'. Pass the operation's name, the amount and the current balance to show_account."
