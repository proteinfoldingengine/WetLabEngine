"""Compare every original scientific field and all outputs covered by the numpy checker."""
import copy
from fractions import Fraction
import json
from pathlib import Path
import sys

def require(ok, message):
    if not ok:
        raise ValueError(message)

def equivalent(a,b,path='root'):
    require(type(a) is type(b), 'type '+path)
    if isinstance(a,dict):
        require(set(a)==set(b),'keys '+path)
        for k in a:
            if path=='root' and k in ('python','sympy','numpy','mpmath'):
                continue
            equivalent(a[k],b[k],path+'.'+k)
    elif isinstance(a,list):
        require(len(a)==len(b),'length '+path)
        for i,(x,y) in enumerate(zip(a,b)): equivalent(x,y,path+'.'+str(i))
    elif isinstance(a,float) and path.startswith('root.haar_R_untouched_max_p_value.'):
        require(abs(a-b)<=1e-10,'Haar '+path)
    else:
        require(a==b,'value '+path)

def check(produced, independent, archived):
    equivalent(produced,archived)
    require(set(independent)=={'tau_q','tau_half','swapped_world_realizes_C','dE4_rank2_R_untouched_realizes_C','dE4_rank3_p_value'},'independent field universe')
    comparisons=0
    def number(x,y,label):
        nonlocal comparisons
        require(abs(float(Fraction(x))-y)<=1e-10,label); comparisons+=1
    for name, old in [('tau_q','tau_q=diag(2/3,1/3)'),('tau_half','tau_half=I/2')]:
        a=produced['controls_TB'][old]; b=independent[name]
        require(set(b)=={'KF','W_Bell^c','W_E^c','W_E_fixed_mirror','W_R(x)I_E','W_R;SWAP','W_W^c'},'writer universe')
        number(a['KF_bound_R_untouched'],b['KF'],'Ky Fan')
        for writer in sorted(set(b)-{'KF'}):
            ao=a[writer if writer!='W_E_fixed_mirror' else 'W_E_fixed_mirror(R-untouched)']; bo=b[writer]
            require(set(bo)=={'realizes_C','p_value'},'writer fields')
            require(ao['realizes_C'] is bo['realizes_C'],'independent channel '+writer); comparisons+=1
            number(ao['p_value_rho_star'],bo['p_value'],'p-value '+writer)
    sw=produced['jointly_swapped_mirror_tau_q_on_R']
    require(set(independent['swapped_world_realizes_C'])=={'W_E(x)I_R','W_R(x)I_E'},'swapped universe')
    for k,v in independent['swapped_world_realizes_C'].items():
        require(sw[k]['realizes_C'] is v,'swapped channel'); comparisons+=1
    require(produced['threshold_dE4']['rank2_R_untouched_realizes_C'] is independent['dE4_rank2_R_untouched_realizes_C'],'rank2 threshold'); comparisons+=1
    number(produced['threshold_dE4']['rank3_construction_p_value'],independent['dE4_rank3_p_value'],'rank3 threshold')
    return comparisons

if __name__=='__main__':
    a,b,c=[json.loads(Path(x).read_bytes()) for x in sys.argv[1:4]]
    n=check(a,b,c)
    bad=copy.deepcopy(a); bad['Q1']['verdict']='FAIL'
    try:
        check(bad,b,c)
    except ValueError as exc:
        require(str(exc)=='value root.Q1.verdict','wrong control rejection')
        control={'status':'REJECTED','mutation':'corrupted-original-verdict','reason':str(exc)}
    else:
        raise ValueError('corrupted original verdict accepted')
    print(json.dumps({'status':'PASS','all_original_scientific_fields_equal':True,
        'metadata_excluded':['python','sympy','numpy','mpmath'],'haar_absolute_tolerance':1e-10,
        'independent_common_fields_checked':n,'control':control},indent=2,sort_keys=True))
