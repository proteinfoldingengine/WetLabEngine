"""Predeclared post-freeze shuffle and local-identifiability checks."""
from fractions import Fraction
import json
from pathlib import Path
import random
import argparse
import numpy as np
import check_bracket_ports as audit

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path)
    args=parser.parse_args()
    source=args.source or Path(__file__).resolve().parents[5]/audit.HISTORICAL_PATH
    fn=audit.original_functions(source)
    data=fn['build_base']()
    gates={k:Fraction((i+1)%11+2,(2*i+1)%7+3) for i,k in enumerate(data['gates'])}
    x,b,c,d=([int(val) for val in j] for j in data['branches'])
    op=audit.apply_exact
    gamma=gates['g1234r']
    rows=[]
    for seed in range(-1,128):
        rng=random.Random(seed)
        B,C,D=[v.copy() for v in (b,c,d)]
        if seed!=-1:
            for v in (B,C,D):rng.shuffle(v)
        q3=op(op(B,C,gates['g23']),D,gates['g234'])
        q4=op(B,op(C,D,gates['g34']),gates['g234'])
        before=[np.array(j,dtype=object) for j in (x,B,C,D)]
        outputs=fn['bracket4_all'](before,gates)
        reconstructed=[]
        for i in range(audit.N):
            delta=before[0].copy()
            delta[(i-1)%audit.N]+=1
            trial=fn['bracket4_all']([delta,*before[1:]],gates)
            diff=(trial[audit.LEFT][i]-outputs[audit.LEFT][i])-(trial[audit.RIGHT][i]-outputs[audit.RIGHT][i])
            reconstructed.append(diff/gamma)
        assert reconstructed == [u-v for u,v in zip(q3,q4)]
        local=gamma*reconstructed[3]
        rows.append(dict(seed=seed,site3_contrast=str(local),nonzero_matrix=any(reconstructed)))
    # Two uncoupled, externally supplied static backgrounds; no inner brackets.
    # They give the identical absolute slopes at 2->3 and contrast at 2->2.
    rates=[]
    for qr in (-21,-90):
        static=[0]*audit.N
        static[3]=qr
        probe=x.copy();probe[2]+=1;probe[10]-=1
        baseout=fn['recombine'](np.array(x,dtype=object),np.array(static,dtype=object),gamma)
        out=fn['recombine'](np.array(probe,dtype=object),np.array(static,dtype=object),gamma)
        rates.append([int(out[i]-baseout[i]) for i in (3,2)])
    assert rates == [[-63,64],[-270,271]]
    assert rows[0]['site3_contrast']=='207'
    shuffled=rows[1:]
    print(json.dumps(dict(shuffles=shuffled,trials=len(shuffled),
          nonzero_local=sum(Fraction(r['site3_contrast'])!=0 for r in shuffled),
          equal_207=sum(r['site3_contrast']=='207' for r in shuffled),
          nonzero_full=sum(r['nonzero_matrix'] for r in shuffled),
          original=rows[0],static_control_gains=rates),sort_keys=True,indent=2))
if __name__=='__main__':main()
