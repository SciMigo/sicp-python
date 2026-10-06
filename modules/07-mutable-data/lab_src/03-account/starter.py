def make_account(initial,password):
    def dispatch(given,request):
        def operation(amount):
            show_state('account not implemented',[initial])
            return initial
        return operation
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
