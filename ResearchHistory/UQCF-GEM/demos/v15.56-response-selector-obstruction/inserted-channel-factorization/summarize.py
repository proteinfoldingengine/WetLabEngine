"""Fail-closed aggregation of the frozen v16.04 ensemble."""
import argparse,collections,gzip,hashlib,json,pathlib,sys
from decimal import Decimal
HEAD='1b14035ab727b1f07a40c01498f91ad7fd0f3aac'
CANDIDATES=[13,16,22,25,27,29,37,39,46,50,66,77]
METRICS=['lift','commutator','connected','global_covariance','response_covariance','precision','hidden_null','hidden_pair_equality','affine_null','identity_middle_null','weight_preserving_null','hessian_identity','parent_coefficient','direct_coefficient','sum_coefficient','retained_covariance']

def number(x):
    d=Decimal(str(x))
    if not d.is_finite():raise ValueError('nonfinite reported number')
    return d

def summarize(shards):
    ids=[s['candidate_index'] for s in shards]
    if len(ids)!=12 or set(ids)!=set(CANDIDATES):raise ValueError('incomplete or duplicate candidate ensemble')
    expected={(a,arm,d) for a in [1.,1/3,1/6] for arm in ['plane','isotropic'] for d in [50,80]}
    valid=True;confirmed=True;metrics={};counts={};ranks={};ratios=[];rows=[];metadata={}
    for s in sorted(shards,key=lambda x:x['candidate_index']):
        if s['version']!='16.04' or s['execution_head']!=HEAD:raise ValueError('wrong version or execution head')
        keys=[(r['a'],r['arm'],r['precision']) for r in s['rows']]
        if len(keys)!=12 or set(keys)!=expected:raise ValueError('incomplete or duplicate configurations')
        valid=valid and s['all_valid'] is True and s['verdict']!='INVALID'
        confirmed=confirmed and s['factorization_confirmed'] is True and s['verdict']=='FACTORIZATION_CONFIRMED'
        if sorted(c['precision'] for c in s['controls'])!=[50,80]:raise ValueError('missing precision controls')
        for c in s['controls']:
            valid=valid and c['all_valid'] is True and c['ranks_and_classes_agree'] is True and c['laws']['valid'] is True and c['isotropic_laws']['valid'] is True
            if set(c['metrics'])!=set(METRICS) or set(c['limits'])!=set(METRICS):raise ValueError('missing metric')
            for k,v in c['metrics'].items():
                limit=Decimal('1e-30' if k=='precision' else '1e-35')
                if number(c['limits'][k])!=limit:raise ValueError('changed frozen tolerance')
                value=number(v);valid=valid and 0<=value<=limit
                key=f"{c['precision']}:{k}";metrics[key]=max(metrics.get(key,Decimal(0)),value)
        for r in s['rows']:
            if r['candidate_index']!=s['candidate_index'] or [f['frame'] for f in r['frames']]!=[0,1]:raise ValueError('wrong row or frame identity')
            for frame in r['frames']:
                for key in ['T_D','T_A','T']:
                    rec=frame[key]
                    if len(rec['matrix'])!=3 or any(len(row)!=81 for row in rec['matrix']):raise ValueError('wrong cubic matrix shape')
                    for row in rec['matrix']:
                        for v in row:number(v)
                    norm=number(rec['norm']);sv=[number(v) for v in rec['singular_values']]
                    if norm<0 or len(sv)!=3 or any(v<0 for v in sv) or sv!=sorted(sv,reverse=True):raise ValueError('invalid spectrum or norm')
                    computed_ranks=[sum(v>Decimal(t) for v in sv) for t in ['1e-9','1e-10','1e-11']]
                    classification='null' if norm<=Decimal('1e-35') else ('active' if sv[0]>Decimal('1e-9') else 'unresolved')
                    if rec['ranks']!=computed_ranks or frame['classifications'][key]!=classification:raise ValueError('inconsistent rank or classification')
                    mkey=(s['candidate_index'],r['a'],r['arm'],key)
                    current=(computed_ranks,classification)
                    if mkey in metadata and metadata[mkey]!=current:raise ValueError('frame or precision metadata disagreement')
                    metadata[mkey]=current
                if frame['cancellation_ratio'] is not None:number(frame['cancellation_ratio'])
            if r['precision']==80:
                f=r['frames'][0];group='identity' if r['a']==1. else 'EB'
                for k in ['T_D','T_A','T']:
                    label=f"{group}:{k}:{f['classifications'][k]}";counts[label]=counts.get(label,0)+1
                    label=f"{group}:{r['arm']}:{k}:{f[k]['ranks']}";ranks[label]=ranks.get(label,0)+1
                if group=='EB' and f['cancellation_ratio'] is not None:ratios.append(number(f['cancellation_ratio']))
                rows.append({k:r[k] for k in ['candidate_index','a','arm']}|{'classifications':f['classifications'],'ranks':{k:f[k]['ranks'] for k in ['T_D','T_A','T']},'norms':{k:f[k]['norm'] for k in ['T_D','T_A','T']},'direction_norms':f['direction_norms'],'cancellation_ratio':f['cancellation_ratio']})
    return {'version':'16.04','execution_head':HEAD,'all_valid':bool(valid),'verdict':'INVALID' if not valid else ('FACTORIZATION_CONFIRMED' if confirmed else 'FACTORIZATION_NOT_CONFIRMED'),'candidate_count':12,'configurations_per_precision':72,'frame_count':2,'maximum_metrics':{k:str(v) for k,v in metrics.items()},'classification_counts_80_native':counts,'rank_counts_80_native':ranks,'EB_cancellation_ratio_range':None if not ratios else [str(min(ratios)),str(max(ratios))],'rows_80_native':rows}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=pathlib.Path);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args()
    files=[a.directory/f'result-{n}.json.gz' for n in CANDIDATES]
    result=summarize([json.loads(gzip.decompress(f.read_bytes())) for f in files]);result['raw_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({k:result[k] for k in ['all_valid','verdict','candidate_count']}))

    sys.exit(0 if result['all_valid'] else 2)
