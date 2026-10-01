"""Fresh parent replay and complete prospectively registered core campaign."""
from pathlib import Path
import sys,subprocess,json,gzip,time
from integrity import OLD,parent_equal,dump
import producer,verifier

def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(OLD/'run_campaign.py'),str(out/'parent46')],check=True)
    parent_equal(out/'parent46',OLD/'evidence/science/scientific')
    tick=time.perf_counter();doc=producer.produce();print('production seconds',time.perf_counter()-tick,flush=True)
    # Preserve the produced certificate even if independent verification fails.
    (out/'CERTIFICATE.json.gz').write_bytes(gzip.compress((json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    tick=time.perf_counter()
    try:
        result=verifier.verify(doc)
        parent=json.loads(gzip.decompress((out/'parent46/CERTIFICATE.json.gz').read_bytes()))
        verifier.parent_graph_equal(doc,parent)
    except Exception as exc:
        dump(out/'FAILURE.json',{'status':'INCOMPLETE','exception':str(exc)});raise
    print('verification seconds',time.perf_counter()-tick,flush=True)
    dump(out/'VERIFY.json',result);dump(out/'SUMMARY.json',{'preregistered_outcome':result['outcome'],'finite_result':result,'general_claim':'See independently reviewed THEOREM.md; finite results do not establish the universal unit-barrier claim.','parent46_fresh_bytes_identical':True,'parent_graph_records_identical':True})
    print(json.dumps(result),flush=True)
if __name__=='__main__':run(sys.argv[1])
