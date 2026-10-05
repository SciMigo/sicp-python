import random,copy
saved=show_call;show_call=lambda *a:None
rng=random.Random(921)
for _ in range(40):
    count=rng.randrange(0,5)
    fn={'params':['p'+str(i) for i in range(count)],'parent':rng.randrange(10)}
    args=[rng.randrange(-20,21) for _ in range(count)]
    oldfn=copy.deepcopy(fn);oldargs=list(args)
    caller=(fn['parent']+1)%10
    a=call_frame(fn,caller,args);b=call_frame(fn,caller,args)
    assert a=={'bindings':dict(zip(fn['params'],args)),'parent':fn['parent']},"Free names use the definition environment, not caller locals."
    assert a is not b and a['bindings'] is not b['bindings'],"Each call needs a fresh parameter table."
    assert fn==oldfn and args==oldargs
show_call=saved
