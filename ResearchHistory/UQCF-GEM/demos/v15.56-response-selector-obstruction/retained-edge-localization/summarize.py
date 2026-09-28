"""Independent structural and arithmetic checks on the 16.05 publication ensemble."""
import argparse,ast,gzip,hashlib,json,pathlib,sys
from decimal import Decimal,localcontext
import sympy as sp
HEAD='24315bf18eed287f174f9b8e1e033fad55ea48f0'
CANDIDATES=[13,16,22,25,27,29,37,39,46,50,66,77]
METRICS=['coefficient_identity','state_reconstruction','transfer_identity','commutator','exact_direction','global_covariance','retained_covariance','response_covariance','precision','hidden_null','hidden_pair_equality','hessian_identity','parent_response','parent_complete_norm','identity_middle_null']
A=sp.Symbol('a',real=True)

def polynomial(text):
    def walk(node):
        if isinstance(node,ast.Constant) and type(node.value) is int:return sp.Integer(node.value)
        if isinstance(node,ast.Name) and node.id=='a':return A
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            x=walk(node.operand);return -x if isinstance(node.op,ast.USub) else x
        if isinstance(node,ast.BinOp):
            x,y=walk(node.left),walk(node.right)
            if isinstance(node.op,ast.Add):return x+y
            if isinstance(node.op,ast.Sub):return x-y
            if isinstance(node.op,ast.Mult):return x*y
            if isinstance(node.op,ast.Div) and y!=0:return x/y
            if isinstance(node.op,ast.Pow) and y.is_Integer and 0<=y<=256:return x**y
        raise ValueError('unsupported polynomial syntax')
    p=sp.Poly(walk(ast.parse(text,mode='eval').body),A,domain=sp.QQ)
    return p.as_expr()

def number(x):
    d=Decimal(str(x))
    if not d.is_finite():raise ValueError('nonfinite number')
    return d

def norm(matrix,cols=3):
    if len(matrix)!=3 or any(len(row)!=cols for row in matrix):raise ValueError('matrix shape')
    with localcontext() as ctx:
        ctx.prec=100
        return sum((number(x)**2 for row in matrix for x in row),Decimal(0)).sqrt()

def label(r,t):
    if r<=Decimal('1e-35'):
        if t<=Decimal('1e-35'):return 'RETAINED_EDGE_NULL'
        raise ValueError('retained-null/readout contradiction')
    if t>Decimal('1e-9'):return 'READOUT_RESPONSE'
    return 'READOUT_ANNIHILATION' if r>Decimal('1e-9') and t<=Decimal('1e-35') else 'UNRESOLVED'

def summarize(shards):
    ids=[s['candidate_index'] for s in shards]
    if len(ids)!=12 or set(ids)!=set(CANDIDATES):raise ValueError('missing/duplicate candidate')
    expected={(a,arm,d) for a in [1.,1/3,1/6] for arm in ['plane','isotropic'] for d in [50,80]}
    valid=True;metrics={};counts={};metadata={};exact_rows=[];rows=[];support=[];omitted=[];retained=[]
    for s in sorted(shards,key=lambda s:s['candidate_index']):
        if s['version']!='16.05' or s['execution_head']!=HEAD:raise ValueError('wrong version/head')
        keys=[(r['a'],r['arm'],r['precision']) for r in s['rows']]
        if len(keys)!=12 or set(keys)!=expected:raise ValueError('missing/duplicate configuration')
        valid=valid and s['all_valid'] is True and s['verdict']!='INVALID'
        if sorted(c['precision'] for c in s['controls'])!=[50,80]:raise ValueError('precision control missing')
        for c in s['controls']:
            valid=valid and c['all_valid'] is True and c['ranks_and_localizations_agree'] is True and c['laws']['valid'] is True and c['isotropic_laws']['valid'] is True
            if set(c['metrics'])!=set(METRICS) or set(c['limits'])!=set(METRICS):raise ValueError('missing metric')
            for k,v in c['metrics'].items():
                limit=Decimal('1e-30' if k=='precision' else '1e-35');value=number(v)
                if number(c['limits'][k])!=limit:raise ValueError('changed tolerance')
                valid=valid and 0<=value<=limit
                key=f"{c['precision']}:{k}";metrics[key]=max(metrics.get(key,Decimal(0)),value)
        if set(s['exact'])!={'plane','isotropic'}:raise ValueError('exact arm missing')
        for arm,rec in s['exact'].items():
            mats=rec['direction_polynomials']
            if len(mats)!=6 or any(len(m)!=3 or any(len(row)!=3 for row in m) for m in mats):raise ValueError('exact matrix shape')
            pp=[[[polynomial(x) for x in row] for row in m] for m in mats]
            zeros=[all(x==0 for row in m for x in row) for m in pp]
            middle=all(x.subs(A,1)==0 for m in pp for row in m for x in row)
            if zeros!=rec['edge_zero'] or all(zeros[:5])!=rec['retained_zero'] or zeros[5]!=rec['omitted_zero'] or middle!=rec['identity_middle_zero']:raise ValueError('incorrect exact zero metadata')
            valid=valid and middle
            exact_rows.append({'candidate_index':s['candidate_index'],'arm':arm,'retained_zero':all(zeros[:5]),'omitted_zero':zeros[5]})
        cert=s['support_certificate']
        if cert['confirmed'] != (len(cert['failures'])==0):raise ValueError('incorrect support certificate metadata')
        valid=valid and cert['basis_word_count']==112 and cert['exact_transfer_reconstruction'] is True
        extra_zero=all(polynomial(c)==0 for w,c in s['excluded_sector_commutator'])
        if extra_zero!=s['excluded_sector_commutator_zero']:raise ValueError('incorrect excluded-sector zero metadata')
        support.append({'candidate_index':s['candidate_index'],'basis_certificate':s['support_certificate'],'excluded_nonzero_word_count':len(s['excluded_state_coefficients']),'excluded_sector_commutator_zero':s['excluded_sector_commutator_zero']})
        for r in s['rows']:
            if r['candidate_index']!=s['candidate_index'] or [f['frame'] for f in r['frames']]!=[0,1]:raise ValueError('row/frame identity')
            for f in r['frames']:
                if len(f['directions'])!=6:raise ValueError('six directions required')
                en=[norm(m) for m in f['directions']]
                with localcontext() as ctx:
                    ctx.prec=100
                    nn={'retained':sum((x*x for x in en[:5]),Decimal(0)).sqrt(),'omitted':en[5],'complete':sum((x*x for x in en),Decimal(0)).sqrt()}
                if len(f['norms']['edges'])!=6:raise ValueError('six norms required')
                if any(abs(x-number(y))>Decimal('1e-35') for x,y in zip(en,f['norms']['edges'])) or any(abs(v-number(f['norms'][k]))>Decimal('1e-35') for k,v in nn.items()):raise ValueError('incorrect direction norm')
                td=f['T_D'];tn=norm(td['matrix'],81)
                if abs(tn-number(td['norm']))>Decimal('1e-35'):raise ValueError('incorrect response norm')
                sv=[number(x) for x in td['singular_values']]
                if len(sv)!=3 or sv!=sorted(sv,reverse=True) or min(sv)<0:raise ValueError('invalid spectrum')
                ranks=[sum(v>Decimal(t) for v in sv) for t in ['1e-9','1e-10','1e-11']]
                cls='null' if number(td['norm'])<=Decimal('1e-35') else ('active' if sv[0]>Decimal('1e-9') else 'unresolved')
                loc=label(number(f['norms']['retained']),number(td['norm']))
                if td['ranks']!=ranks or f['classification']!=cls or f['localization']!=loc:raise ValueError('incorrect rank/classification/localization')
                key=(s['candidate_index'],r['a'],r['arm']);current=(ranks,cls,loc)
                if key in metadata and metadata[key]!=current:raise ValueError('frame/precision disagreement')
                metadata[key]=current
            if r['precision']==80:
                f=r['frames'][0];group='identity' if r['a']==1. else 'EB';key=group+':'+f['localization'];counts[key]=counts.get(key,0)+1
                rows.append({k:r[k] for k in ['candidate_index','a','arm']}|{'norms':f['norms'],'localization':f['localization'],'T_D_norm':f['T_D']['norm'],'T_D_ranks':f['T_D']['ranks']})
                if group=='EB':omitted.append(number(f['norms']['omitted']));retained.append(number(f['norms']['retained']))
    confirmed=all(r['retained_zero'] for r in exact_rows) and counts.get('EB:RETAINED_EDGE_NULL',0)==48
    return {'version':'16.05','execution_head':HEAD,'all_valid':bool(valid),'verdict':'INVALID' if not valid else ('EXACT_RETAINED_EDGE_LOCALIZATION_CONFIRMED' if confirmed else 'LOCALIZATION_MIXED_OR_NOT_CONFIRMED'),'candidate_count':12,'configurations_per_precision':72,'frame_count':2,'maximum_metrics':{k:str(v) for k,v in metrics.items()},'localization_counts_80_native':counts,'exact_symbolic_cases':exact_rows,'support_cases':support,'EB_retained_norm_range':[str(min(retained)),str(max(retained))],'EB_omitted_norm_range':[str(min(omitted)),str(max(omitted))],'rows_80_native':rows}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=pathlib.Path);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args()
    files=[a.directory/f'result-{n}.json.gz' for n in CANDIDATES]
    result=summarize([json.loads(gzip.decompress(f.read_bytes())) for f in files]);result['raw_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({k:result[k] for k in ['all_valid','verdict','candidate_count']}));sys.exit(0 if result['all_valid'] else 2)
