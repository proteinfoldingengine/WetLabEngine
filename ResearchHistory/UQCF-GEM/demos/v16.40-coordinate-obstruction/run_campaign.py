"""Fresh parent canonical replay followed by the preregistered directed universe."""
from pathlib import Path
import sys,subprocess,json,gzip,time
from integrity import OLD,legacy,dump
import producer,verifier

def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(OLD/'run_campaign.py'),str(out/'parent39')],check=True)
    legacy.scientific_equal(out/'parent39',OLD/'evidence/science/scientific')
    tick=time.perf_counter();doc=producer.produce();print('production seconds',time.perf_counter()-tick,flush=True)
    tick=time.perf_counter();result=verifier.verify(doc);print('verification seconds',time.perf_counter()-tick,flush=True)
    (out/'CERTIFICATE.json.gz').write_bytes(gzip.compress((json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    dump(out/'VERIFY.json',result);dump(out/'SUMMARY.json',{'preregistered_outcome':result['outcome'],'finite_result':result,'general_claim':'See independently reviewed THEOREM.md; finite evidence does not prove the general family.','parent39_fresh_bytes_identical':True})
    print(json.dumps(result),flush=True)
if __name__=='__main__':run(sys.argv[1])
