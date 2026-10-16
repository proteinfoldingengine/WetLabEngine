"""Closed-form production of the contract's finite exact regression examples."""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

SOURCE = '1ef7d25cedd5af6be6e72fea4e5963414a92cc0a'
CONTRACT = 'cbefdb85f21cd9606d1a9260d38176c2dc068b91'
CONTRACT_PATH = 'ResearchHistory/UQCF-GEM/research/physical-bridge/analytical_repair/CONTRACT.md'

def rational(x):
    x = F(x)
    return f'{x.numerator}/{x.denominator}'

def produce():
    records = []
    for D, dname in [(F(1,2),'1_2'), (F(1),'1')]:
        for r, rname in [(F(0),'0'),(F(1,2),'1_2'),(F(1),'1')]:
            records.append({'id':f'qubit_D{dname}_r{rname}','value':rational(r*D/2)})
    for n in range(2,9):
        records.append({'id':f'orthogonal_n{n}','value':rational(F(1,2))})
        records.append({'id':f'pure_mixed_n{n}','value':rational(F(n-1,n)**n)})
    controls = {
        'identical_centralizer':{'dim0':'2/1','dim1':'2/1','false_contrast':'0/1'},
        'reader_retention':{'coarse_before':'1/4','coarse_after':'1/4','fine_after':'1/1'},
        'block_product':'1/3', 'block_resolving':'1/2', 'so3_real':'0/1', 'so3_helicity':'3/4',
    }
    records.extend({'id':k,'value':v} for k,v in controls.items())
    return {'schema':'uqcf-analytical-repair-v1','source_parent':SOURCE,'contract_commit':CONTRACT,
        'contract_path':CONTRACT_PATH,
        'domain':{'qubit_D':['1/2','1/1'],'qubit_r':['0/1','1/2','1/1'],'n':list(range(2,9)),
                  'control_ids':list(controls)}, 'records':sorted(records,key=lambda x:x['id'])}

if __name__ == '__main__':
    Path(sys.argv[1]).write_text(json.dumps(produce(),sort_keys=True,indent=2)+'\n')
