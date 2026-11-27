"""Locate two exact records from the original v16.29 five-site extension."""
import json
import lzma
from hashlib import sha256
from pathlib import Path
import sys

from replay import D26, module, pinned, route

def compact(x):
    return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def locate(demos):
    stage = demos/'v16.29-local-profile-closure'
    pinned(stage/'producer.py','fc4a77fc4f01fce33fdb562423eca274cfb0c648')
    pinned(demos/D26/'engine.py','c10ac57f988a439144e21898bd2b33ece0838a9b')
    producer = module(stage/'producer.py')
    native = module(demos/D26/'engine.py')
    evidence = stage/'evidence'
    raw = lzma.decompress(pinned(evidence/'FULL_CERTIFICATES.json.xz','45cefa46e2d0f50ecde74bab9bc3d498edc69752'))
    official = json.loads(pinned(evidence/'PRODUCTION.json','220e7644381df8e9f213a36a8f401bd18634cc69'))
    assert len(raw)==official['raw_bytes'] and sha256(raw).hexdigest()==official['raw_sha256']
    p = (-1,0,0,1,1)
    # Native extension uses ascending chart masks: E, D, A, C.
    ys = ((0,2),(0,1,3),(0,1,2,3),(0,1,2,4))
    code = producer.code(p)
    end_token = b'],"code":'+compact(code)+b',"parents":'+compact(p)+b',"variant":"original"}'
    ext = raw.index(b'"extension":[')
    stop = raw.index(end_token,ext)
    assert b',"parent":[' not in raw[ext:stop]
    group_start = raw.rindex(b'{"cases":[',ext,stop)
    group = json.loads(raw[group_start:stop+len(end_token)])
    assert group['variant']=='original' and group['parents']==list(p)
    begin = group_start + len(b'{"cases":[')
    out=[]
    for a in (2,3):
        events = ((2,a),(3,2))
        live = route(native,p,ys,events)
        row = producer.certify(p,ys,events)
        encoded = compact(row)
        assert raw.count(encoded,begin,stop)==1
        start = raw.index(encoded,begin,stop)
        archived = json.loads(raw[start:start+len(encoded)])
        assert live[1]['before']==archived['states'][1] and live[1]['after']==archived['states'][3]
        v = live[1]['parent']
        before,after = archived['profiles'][1][v],archived['profiles'][3][v]
        assert (before,after)==(live[1]['tau_before'],live[1]['tau_after'])
        assert after-before==int(live[1]['trigger'])
        assert archived['heights'][3]-archived['heights'][1]==live[1]['delta_h']==0
        out.append(dict(ordinal_zero_based=group['cases'].index(archived),
                        byte_offset=start,certificate_sha256=sha256(encoded).hexdigest(),
                        first_event=events[0],second_event=events[1],receiver_bit=live[1]['trigger'],
                        profiles=archived['profiles'], heights=archived['heights'],mechanism=archived['mechanism']))
    assert [x['receiver_bit'] for x in out]==[True,False]
    return dict(group_code=code,variant='original',archive_raw_sha256=official['raw_sha256'],rows=out)


if __name__=='__main__':
    print(json.dumps(locate(Path(sys.argv[1])),sort_keys=True,indent=2))
