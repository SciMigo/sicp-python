def make_account(initial,password):
    balance=initial
    def withdraw(amount):
        nonlocal balance
        if amount>balance:
            show_state('rejected withdrawal',[balance])
            return 'Insufficient funds'
        balance-=amount
        show_state('withdraw',[balance])
        return balance
    def deposit(amount):
        nonlocal balance
        balance+=amount
        show_state('deposit',[balance])
        return balance
    def wrong(amount):
        show_state('wrong password',[balance])
        return 'Incorrect password'
    def dispatch(given,request):
        if given!=password:return wrong
        if request=='withdraw':return withdraw
        if request=='deposit':return deposit
        raise ValueError('Unknown request')
    return dispatch

from scimigo import canvas,figure,text,frame

def show_state(label,values):
    canvas(600,260)
    text(15,35,label,size=19)
    figure('array_state',x=0,y=65,width=600,height=160,
           values=list(values) or ['empty'],indices=False,cell_width=110)
    frame()

account=make_account(60,'violet')
for pw,request,amount in [('violet','withdraw',15),('wrong','deposit',20),('violet','deposit',7),('violet','withdraw',90),('violet','withdraw',12)]:
    print(account(pw,request)(amount))
