def connect(service,old_password,new_password):
    return service

from scimigo import canvas,figure,text,frame

def show_state(label,values):
    canvas(600,260)
    text(15,35,label,size=19)
    figure('array_state',x=0,y=65,width=600,height=160,
           values=list(values) or ['empty'],indices=False,cell_width=220)
    text(15,245,'route count / latest result',size=18)
    frame()

def supplied_account(initial,password):
    balance=initial
    def dispatch(given,request):
        if request=='check':return given==password
        if given!=password:return lambda amount:'Incorrect password'
        def operation(amount):
            nonlocal balance
            if request=='withdraw':
                if amount>balance:return 'Insufficient funds'
                balance-=amount
            elif request=='deposit':balance+=amount
            else:raise ValueError('Unknown request')
            return balance
        return operation
    return dispatch

def run_access(account,program):
    routes={'owner':account}
    outputs=[]
    for event in program:
        if event[0]=='join':
            _,name,parent,old,new=event
            try:
                route=connect(routes[parent],old,new)
            except ValueError:
                result='Incorrect password'
            else:
                routes[name]=route
                result='Joined'
        else:
            _,name,password,request,amount=event
            result=routes[name](password,request)(amount)
        outputs.append(result)
        show_state('access result',[len(routes),result])
    return outputs

account=supplied_account(75,'first')
program=[('join','guest','owner','first','second'),
         ('use','guest','second','withdraw',18),
         ('use','owner','first','deposit',5),
         ('join','third','guest','second','third-key'),
         ('use','third','third-key','withdraw',7),
         ('use','guest','wrong','deposit',100),
         ('use','owner','first','withdraw',0)]
print(run_access(account,program))
