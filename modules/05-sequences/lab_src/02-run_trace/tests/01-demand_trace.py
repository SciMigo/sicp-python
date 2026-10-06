saved=draw;draw=lambda *args:None
try:
    for items,k in [([1,3,4,6,9],2),([0,0,2],2),([-2,-3,4,6],1),([],3),([1,2],5),([3,6],0),([3,6],5)]:
        expected=[];wanted=[('start',k)]
        if k:
            for item in items:
                wanted += [('pull',item),('test',item)]
                if item%3==0:
                    value=item+100;expected.append(value);wanted += [('map',item),('output',value)]
                    if len(expected)==k:break
        assert run_trace(items,k)==expected,"Produce only the requested accepted prefix, or all available matches if fewer exist."
        assert events==wanted,"Do not transform rejected items or advance after the final requested result."
finally:draw=saved
