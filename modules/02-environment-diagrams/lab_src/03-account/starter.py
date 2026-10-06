def make_account(balance):
    def withdraw(amount):
        show_account("withdraw", amount, balance)
        return balance

    def deposit(amount):
        show_account("deposit", amount, balance)
        return balance

    return withdraw, deposit

from scimigo import canvas, figure, frame, text

def show_account(operation, amount, balance):
    canvas(360, 240)
    figure("environment_diagram", x=0, y=0, width=360, height=190,
           frame_width=240, frame_padding=16, row_height=22,
           frames=[{"id": "account", "label": "Frame of make_account",
                    "bindings": [{"name": "balance", "value": str(balance)}]}])
    text(12, 222, operation + " " + str(amount) + ": balance is " + str(balance), size=16)
    frame()

withdraw, deposit = make_account(20)
print(deposit(15), withdraw(30), withdraw(30), deposit(1))
