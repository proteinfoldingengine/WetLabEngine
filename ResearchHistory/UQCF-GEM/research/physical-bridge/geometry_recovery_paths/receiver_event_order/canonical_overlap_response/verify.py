"""Independent certificate check: exclusive energy transfer, no historical Python imports."""
import json, sys
from collections import Counter
from hashlib import sha256
from pathlib import Path

def audit(raw, result):
    assert sha256(raw).hexdigest()=='319c43442aee53b9da4e94bc2005841bcaba39629318d285b2b4f9d11838f515'
    archive=json.loads(raw); got=json.loads(result)
    assert len(archive)==len(got)==288
    counts=Counter()
    for row,out in zip(archive,got,strict=True):
        steps=[e[0] for e in row['path']]
        if len(steps)==1:
            assert out is None
            counts['idle']+=1
            continue
        assert type(out) is list and len(out)==4
        idx,branch,lo,hi=out
        n=row['order']; R=row['receiver']; C=1-R
        sites={v:1<<i for i,v in enumerate(n)}
        leaves={v for v in n if v[0] in 'XY'}
        copies=[(j,x) for j in range(1,len(steps)) for x in leaves
                if not steps[j-1][R]&sites[x] and steps[j][R]&sites[x]]
        lead=min(j for j,_ in copies)
        leaf,=(x for j,x in copies if j==lead)
        assert (lead,leaf[0])==(idx,branch)
        v=sites[leaf]
        old,mid,post=steps[lead-1:lead+2]
        assert old[C]&v and not old[R]&v
        assert mid[C]==old[C] and mid[R]==old[R]|v
        assert post[C]==old[C]^v and post[R]==mid[R]
        for z in (0,1):
            # z=0 has grade 1 at the actually copied leaf in this certificate.
            d=dict(Pin=80,P=24,Q=28,A=2,B=6,b1=2,b2=2)
            d.update({x: (1+7*z if x[0]==branch else 8-7*z) for x in leaves})
            def uv(cut):
                return tuple(sum(d[x]**2 for x,b in sites.items() if m&b and not other&b)
                    for m,other in ((cut[R],cut[C]),(cut[C],cut[R])))
            prior_A,prior_B=uv(steps[0])
            a,b=uv(old)
            assert (prior_A,prior_B)==(48,130)
            assert (a,b)=={1:(48,130),3:(44,134),7:(4,174)}[idx]
            q=d[leaf]**2
            expected=[]
            for A,B in ((prior_A,prior_B),(a,b),(a,b-q),(a+q,b-q)):
                assert A>0 and B>0
                g=[[0,2]] if A<B else [[1,2]] if A>B else [[0,2],[1,2]]
                expected.append([[A+B,A,B],g])
            assert expected==(hi if z else lo)
        assert lo[2][1]==hi[2][1]==[[0,2]]
        changed=lo[3][1]!=hi[3][1]
        assert changed==(idx!=7)
        counts[f"{idx}:{branch}:{'split' if changed else 'no-split'}"]+=1
    assert counts=={'idle':16,'1:X:split':104,'1:Y:split':104,'3:X:split':32,'7:Y:no-split':32}
    return dict(sorted(counts.items()))

if __name__=='__main__':
    raw=Path(sys.argv[1]).read_bytes(); work=Path(sys.argv[2]).read_bytes()
    answer=audit(raw,work)
    outcomes=json.loads(work)
    idx=next(k for k,r in enumerate(outcomes) if r)
    # A fabricated after-cut weight and a manufactured geometry edge must both be rejected.
    for element in (0,1):
        outcomes=json.loads(work)
        outcomes[idx][3][3][element]=[-42] if element==0 else [[0,1]]
        try: audit(raw,json.dumps(outcomes).encode())
        except AssertionError: pass
        else: raise AssertionError("independent checker admitted falsified output")
    print(json.dumps({'counts':answer,'rejecting_controls':2,'output_sha256':sha256(work).hexdigest()}, sort_keys=True))
