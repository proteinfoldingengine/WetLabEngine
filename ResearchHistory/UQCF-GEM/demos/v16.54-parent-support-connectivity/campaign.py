"""GitHub-only complete protocol shards and independently checked evidence."""
from collections import Counter
import gzip
import hashlib
from itertools import zip_longest
import json
import os
from pathlib import Path
import re
import resource
import sqlite3
import subprocess
import sys
import tempfile
import traceback

HERE=Path(__file__).resolve().parent

def serial(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)
def dump(path,obj):Path(path).write_text(serial(obj)+'\n')

def verify_scientific_manifest(files,manifest):
    errors=[]
    if set(files)!=set(manifest):errors.append('scientific file membership mismatch')
    for name,data in files.items():
        if hashlib.sha256(data).hexdigest()!=manifest.get(name):errors.append('scientific digest mismatch: '+name)
    return errors

def validate_campaign_summary(s):
    errors=[]
    if s.get('status')!='PASS' or s.get('checked')!=s.get('expected') or not isinstance(s.get('expected'),int) or s['expected']<=0 or s.get('failures')!=0 or s.get('incomplete')!=0:errors.append('campaign unfinished or failed')
    for field in ('scientific_sha','workflow_sha'):
        if not isinstance(s.get(field),str) or not re.fullmatch('[0-9a-f]{40}',s[field]):errors.append('invalid immutable provenance: '+field)
    for field in ('identity_sha256','verified_identity_sha256'):
        if not isinstance(s.get(field),str) or not re.fullmatch('[0-9a-f]{64}',s[field]):errors.append('invalid identity digest')
    if s.get('identity_sha256')!=s.get('verified_identity_sha256'):errors.append('equal-count identity substitution')
    return errors

class JsonGzip:
    def __init__(self,path):
        self.raw=Path(path).open('wb');self.stream=gzip.GzipFile(filename='',fileobj=self.raw,mode='wb',mtime=0)
        self.digest=hashlib.sha256();self.count=0
    def write(self,obj):
        data=(serial(obj)+'\n').encode();self.stream.write(data);self.digest.update(data);self.count+=1
    def close(self):self.stream.close();self.raw.close()

def provenance(out,scope,shard):
    if os.environ.get('GITHUB_ACTIONS')!='true':raise RuntimeError('scientific execution is GitHub-only')
    resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if head!=os.environ['SCIENTIFIC_SHA']:raise ValueError('actual scientific checkout mismatch')
    prov={'scientific_sha':head,'workflow_sha':os.environ['GITHUB_SHA'],
          'run_id':os.environ['GITHUB_RUN_ID'],'attempt':os.environ['GITHUB_RUN_ATTEMPT'],
          'preregistration_sha':os.environ['PREREGISTRATION_SHA'],'scope':scope,'shard':shard}
    dump(out/'PROVENANCE.json',prov)
    source={}
    paths=list(HERE.glob('*.py'))+list((HERE/'tests').glob('*.py'))+[HERE/'protocol.json']+list(HERE.glob('*.md'))
    for path in sorted(paths):
        relative=path.relative_to(HERE);data=path.read_bytes();gitpath=str(path.relative_to(Path.cwd()))
        if subprocess.check_output(['git','show',head+':'+gitpath])!=data:raise ValueError('source checkout byte mismatch')
        source[str(relative)]=hashlib.sha256(data).hexdigest();dest=out/'source'/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    dump(out/'SOURCE_MANIFEST.json',source)
    return prov

def run_shard(scope,shard,out):
    from universe import generate_cases
    from verifier import reconstruct_cases,verify_protocol,verify_record
    from mechanisms import produce
    out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True);science=out/'scientific';science.mkdir(exist_ok=True)
    prov=provenance(out,scope,shard);summary={'status':'INCOMPLETE','expected':0,'checked':0,'failures':0,'incomplete':1,'scope':scope,'shard':shard,'shards':8}
    dump(out/'STATUS.json',{**summary,**prov});current=None;record=None;cases=None;records=None
    try:
        protocol=json.loads((HERE/'protocol.json').read_text());errors=verify_protocol(protocol,HERE)
        if errors:raise ValueError(errors)
        families={'local':['M'+str(i) for i in range(1,7)],'extension':['M7','M8','M9'],'all':protocol['families']}[scope]
        # Selection is a prospectively authorized stage, never an outcome filter.
        domain=dict(protocol,families=families)
        with tempfile.TemporaryDirectory(prefix='v1654-shard-') as temp:
            db=sqlite3.connect(temp+'/checked.sqlite');db.execute('CREATE TABLE universe(n INTEGER PRIMARY KEY,identity TEXT UNIQUE,payload TEXT)')
            whole=hashlib.sha256();previous=None;total=0
            for left,right in zip_longest(reconstruct_cases(domain),generate_cases(domain)):
                if left is None or right is None or serial(left)!=serial(right):raise ValueError('complete independent universe mismatch')
                identity=serial(left['identity'])
                if previous is not None and identity<=previous:raise ValueError('universe duplicate/order violation')
                previous=identity;data=serial(left);whole.update((data+'\n').encode());db.execute('INSERT INTO universe VALUES (?,?,?)',(total,identity,data));total+=1
            db.commit();start=total*shard//8;stop=total*(shard+1)//8;summary['expected']=stop-start
            # Freeze complete membership and this contiguous interval BEFORE paths.
            expected_hash=hashlib.sha256();first=None;last=None
            cases=JsonGzip(science/'CASES.jsonl.gz')
            for payload, in db.execute('SELECT payload FROM universe WHERE n>=? AND n<? ORDER BY n',(start,stop)):
                obj=json.loads(payload);cases.write(obj);identity=serial(obj['identity']);expected_hash.update((identity+'\n').encode());first=first or obj['identity'];last=obj['identity']
            cases.close();cases=None
            freeze={'scope':scope,'families':families,'shard':shard,'shards':8,'total':total,'start':start,'stop':stop,'first':first,'last':last,'whole_universe_sha256':whole.hexdigest(),'identity_sha256':expected_hash.hexdigest()}
            dump(science/'DOMAIN_FREEZE.json',freeze)
            actual_hash=hashlib.sha256();counts=Counter();diagnostics=Counter();records=JsonGzip(science/'RECORDS.jsonl.gz')
            for payload, in db.execute('SELECT payload FROM universe WHERE n>=? AND n<? ORDER BY n',(start,stop)):
                current=json.loads(payload);record=produce(current);errors=verify_record(current,record)
                if errors:
                    summary['failures']+=1;dump(out/'FIRST_FAILURE.json',{'case':current,'record':record,'errors':errors});raise ValueError('independent path rejection: '+str(errors))
                records.write(record);actual_hash.update((serial(record['identity'])+'\n').encode());summary['checked']+=1;counts[current['identity'][0]+':'+record['status']]+=1
                for ev in record.get('events',[]):
                    diagnostics[ev['kind']]+=1
                    if ev['kind']=='buffered_cycle' and len({e[2] for e in ev['edges']})<len(ev['edges']):diagnostics['repeated_row_colors']+=1
                    if ev['kind']=='element_buffer' and ev['target']==ev['old_owner']:diagnostics['element_spare_is_old_owner']+=1
                for move in record.get('facts',{}).get('balancing',[]):
                    diagnostics['exceptional_cyclic_balancing' if move['before'][0]==move['after'][0] else 'ordinary_balancing']+=1
                if summary['checked']%10000==0:print(serial({'shard':shard,'checked':summary['checked'],'expected':summary['expected']}),flush=True)
            record_digest=records.digest.hexdigest();records.close();records=None;db.close()
        summary.update(status='PASS',incomplete=0,identity_sha256=expected_hash.hexdigest(),verified_identity_sha256=actual_hash.hexdigest(),record_sha256=record_digest,counts=dict(counts),diagnostics=dict(diagnostics))
        errors=validate_campaign_summary({**summary,**prov})
        if errors:raise ValueError(errors)
        dump(science/'SUMMARY.json',summary)
        manifest={path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(science.iterdir()) if path.is_file()}
        dump(science/'MANIFEST.json',manifest)
        dump(out/'STATUS.json',{**summary,**prov})
    except BaseException as exc:
        if cases is not None:cases.close()
        if records is not None:records.close()
        summary.update(status='FAIL' if summary['failures'] else 'INCOMPLETE',incomplete=0 if summary['failures'] else 1)
        dump(out/'STATUS.json',{**summary,**prov,'exception_type':type(exc).__name__,'message':str(exc)})
        if current is not None and not (out/'FIRST_FAILURE.json').exists():dump(out/'FIRST_FAILURE.json',{'case':current,'record':record,'exception':str(exc)})
        raise

if __name__=='__main__':run_shard(sys.argv[1],int(sys.argv[2]),sys.argv[3])
