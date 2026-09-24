"""Exact v15.55 defect datum derived from the frozen v15.54 operational table."""
from fractions import Fraction

CTX=("x0y0","x0y1","x1y0","x1y1")
OUT=("00","01","10","11")
ALLOWED={"id","control_role","carrier","operations","operational_table"}

def _parse(candidate):
    if not isinstance(candidate,dict) or set(candidate)-ALLOWED:
        raise ValueError("candidate_schema")
    table=candidate.get("operational_table")
    if not isinstance(table,dict) or set(table)!=set(CTX):
        raise ValueError("context_domain")
    parsed={}
    for c in CTX:
        row=table[c]
        if not isinstance(row,dict) or set(row)!=set(OUT):
            raise ValueError("outcome_domain")
        rr={}
        for o in OUT:
            v=row[o]
            if not isinstance(v,list) or len(v)!=2 or type(v[0]) is not int or type(v[1]) is not int or v[1]<=0:
                raise ValueError("rational")
            q=Fraction(v[0],v[1])
            if q<0: raise ValueError("negative")
            rr[o]=q
        if sum(rr.values(),Fraction())!=1: raise ValueError("normalization")
        parsed[c]=rr
    return parsed

def _chsh(t):
    e=[]
    for c in CTX:
        r=t[c]
        e.append(r["00"]+r["11"]-r["01"]-r["10"])
    return e[0]+e[1]+e[2]-e[3]

def derive_defect(contract,candidate):
    t=_parse(candidate)
    score=abs(_chsh(t))
    bound=Fraction(2,1)
    excess=max(Fraction(),score-bound)
    return {
        "schema":"uqcf-v1555-defect-v1",
        "active":bool(excess),
        "operational_score":[score.numerator,score.denominator],
        "frozen_bound":[bound.numerator,bound.denominator],
        "excess_over_frozen_bound":[excess.numerator,excess.denominator],
        "datum_basis":"EXACT_OPERATIONAL_EXCESS_ONLY"
    }
