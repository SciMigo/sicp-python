import random,copy
saved=show_report;show_report=lambda *args:None
try:
    rng=random.Random(404)
    for length in (0,1,2,7,30):
        raw=[('item'+str(i),rng.randrange(20)) for i in range(length)]
        expected=(sum(w for name,w in raw),max(raw,key=lambda x:x[1])[0] if raw else None)
        for records,getw,getl in [(raw,lambda r:r[1],lambda r:r[0]),([{'payload':{'kg':w,'name':name}} for name,w in raw],lambda r:r['payload']['kg'],lambda r:r['payload']['name'])]:
            before=copy.deepcopy(records)
            assert manifest_report(records,getw,getl)==expected,"Use the provided access operations and preserve the first label on a maximum-weight tie."
            assert records==before,"Do not modify records or their order."
    assert manifest_report([('a',0),('b',0)],lambda r:r[1],lambda r:r[0])==(0,'a'),"Zero weights are valid; ties retain the first record."
finally:show_report=saved
