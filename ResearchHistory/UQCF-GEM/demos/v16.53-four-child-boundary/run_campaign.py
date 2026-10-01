"""Fresh parent52 science plus the frozen four-child boundary corpus."""
from pathlib import Path
import sys,subprocess,json,gzip
from integrity import OLD,parent_equal,dump
import producer,verifier
def failure_outcome(exc):return 'INTERFACE_NOT_PRESERVED' if isinstance(exc,verifier.InterfaceNotPreserved) else 'INCOMPLETE'
def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(OLD/'run_campaign.py'),str(out/'parent52')],check=True)
    parent_equal(out/'parent52',OLD/'evidence/science/scientific')
    try:doc=producer.produce()
    except Exception as exc:
        dump(out/'FAILURE.json',{'status':'INCOMPLETE','phase':'enumeration','exception_type':type(exc).__name__,'message':str(exc),'nonunit_witness':'NOT_CLAIMED'});raise
    (out/'CERTIFICATE.json.gz').write_bytes(gzip.compress((json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    try:result=verifier.verify(doc)
    except Exception as exc:
        dump(out/'FAILURE.json',{'status':failure_outcome(exc),'exception_type':type(exc).__name__,'message':str(exc),'raw_attempts':'CERTIFICATE.json.gz','nonunit_witness':'NOT_CLAIMED'});raise
    dump(out/'VERIFY.json',result)
    dump(out/'SUMMARY.json',{'preregistered_outcome':result['outcome'],'finite_result':result,'general_claim':'See independently reviewed FOUR_CHILD_INTERFACE.md for finite ordered arity2/3/4 trees; finite cases validate implementation and do not replace the proof.','parent52_fresh_bytes_identical':True})
    print(json.dumps({k:v for k,v in result.items() if k!='results'}),flush=True)
if __name__=='__main__':run(sys.argv[1])
