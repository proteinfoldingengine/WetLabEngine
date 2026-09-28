"""Aggregate a complete v16.03 run without changing its frozen adjudication."""
import argparse
import gzip
import hashlib
import itertools
import json
import pathlib
from decimal import Decimal

CANDIDATES=[13,16,22,25,27,29,37,39,46,50,66,77]
AS=[1.,1/3,1/6]

def summarize(folder):
    folder=pathlib.Path(folder);shards=[];evidence=[];details=[];maxima={};domain_exits=[];classes=[];all_valid=True;continuation=True
    for candidate in CANDIDATES:
        path=folder/f'result-{candidate}.json.gz';packed=path.read_bytes();raw=gzip.decompress(packed);r=json.loads(raw)
        assert r['version']=='16.03' and r['candidate_index']==candidate
        expected=set(itertools.product(AS,['overlap','disjoint'],['plane','isotropic'],[50,80]))
        got={(x['a'],x['pair'],x['arm'],x['precision']) for x in r['rows']}
        assert got==expected and len(r['rows'])==24
        assert len(r['controls']['precisions'])==2
        all_valid=all_valid and r['all_valid'];continuation=continuation and r['finite_overlap_confirmed'];classes.extend(r['cubic_classes'])
        evidence.append({'candidate':candidate,'execution_head':r['execution_head'],'file':path.name,'packed_sha256':hashlib.sha256(packed).hexdigest(),'raw_sha256':hashlib.sha256(raw).hexdigest()})
        shards.append({k:r[k] for k in ['candidate_index','all_valid','verdict','continuation_verdict']})
        for ctrl in r['controls']['precisions']:
            for k,v in ctrl['metrics'].items():
                key=str(ctrl['precision'])+':'+k;maxima[key]=str(max(Decimal(v),Decimal(maxima.get(key,'0'))))
        for row in r['rows']:
            assert [x['lambda_exponent'] for x in row['finite']]==[4,5,6,7,8]
            for step in row['finite']:
                for order,frames in step['orders'].items():
                    assert len(frames)==2
                    for frame,v in enumerate(frames):
                        if 'domain_error' in v:domain_exits.append({'candidate':candidate,'a':row['a'],'pair':row['pair'],'arm':row['arm'],'precision':row['precision'],'exponent':step['lambda_exponent'],'order':order,'frame':frame,'error':v['domain_error']})
            if row['precision']!=80:continue
            d={k:row[k] for k in ['candidate_index','a','pair','arm']}
            if row['pair']=='disjoint':
                d['cubic_classification']=row['classification'];d['cubic_norms']=[x['norm'] for x in row['cubic']];d['cubic_ranks']=[x['ranks'] for x in row['cubic']]
            d['finite']=[{'exponent':x['lambda_exponent'],'all_domains':all('domain_error' not in v for vv in x['orders'].values() for v in vv),'remainder_norms':x.get('remainder_norms'),'contrast_ranks':[v['ranks'] for v in x.get('normalized_contrast',[])],'contrast_norms':[v['norm'] for v in x.get('normalized_contrast',[])]} for x in row['finite']]
            details.append(d)
    assert len(classes)==48
    heads={x['execution_head'] for x in evidence};assert len(heads)==1
    primary='DISJOINT_CUBIC_RESPONSE_DETECTED' if 'active' in classes else 'DISJOINT_CUBIC_NUMERICAL_NULL' if all(x=='null' for x in classes) else 'DISJOINT_CUBIC_UNRESOLVED'
    secondary='FINITE_GRID_OVERLAP_RESPONSE_CONFIRMED' if continuation else 'FINITE_GRID_OVERLAP_RESPONSE_NOT_CONFIRMED'
    if not all_valid:primary=secondary='INVALID'
    return {'version':'16.03','all_valid':all_valid,'verdict':primary,'continuation_verdict':secondary,'execution_head':next(iter(heads)),'candidate_count':12,'origin_rows_per_precision':144,'finite_rows_per_precision':720,'eb_cubic_class_counts':{k:classes.count(k) for k in ['active','null','unresolved']},'domain_exit_count':len(domain_exits),'domain_exits':domain_exits,'maximum_metrics_by_precision':maxima,'shards':shards,'evidence':evidence,'rows_80_digits':details}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',nargs='?',default=str(pathlib.Path(__file__).parent));p.add_argument('--output',default='SUMMARY.json');a=p.parse_args()
    r=summarize(a.folder);pathlib.Path(a.output).write_text(json.dumps(r,indent=2,allow_nan=False)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['evidence','rows_80_digits','domain_exits','shards']},indent=2))
