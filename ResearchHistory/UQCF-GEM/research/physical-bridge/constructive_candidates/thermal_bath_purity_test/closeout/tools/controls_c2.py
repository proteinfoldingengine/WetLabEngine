"""Seven frozen corruptions; preserve each input and independent checker rejection."""
import copy
import json
from pathlib import Path
import subprocess
import sys

original = json.loads(Path(sys.argv[1]).read_bytes())
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
checker = Path(__file__).with_name('verify_c2.py')
mutations = {}
c=copy.deepcopy(original); c['cases'].pop(); mutations['missing-case']=c
c=copy.deepcopy(original); c['cases'][1]=copy.deepcopy(c['cases'][0]); mutations['duplicate-case']=c
c=copy.deepcopy(original); c['cases'][1]['id']='substituted-channel'; mutations['substituted-case']=c
c=copy.deepcopy(original); c['choi_rank']=2; mutations['wrong-choi-rank']=c
c=copy.deepcopy(original); c['cases'][0]['realizable_R_untouched']=True; mutations['false-E2-sufficiency']=c
c=copy.deepcopy(original); p=c['cases'][1]['witness']['permutation']; p[6],p[4]=p[4],p[6]; p[6],p[5]=p[5],p[6]; mutations['wrong-slot-witness']=c
c=copy.deepcopy(original); c['provenance']['native_bridge']='DERIVED_FROM_SOURCES'; mutations['false-provenance']=c
reasons={'missing-case':'case count','duplicate-case':'case identity/order','substituted-case':'case identity/order',
         'wrong-choi-rank':'Choi rank','false-E2-sufficiency':'global realization claim',
         'wrong-slot-witness':'frozen witness slots','false-provenance':'provenance'}
results=[]
for name, c in mutations.items():
    path=out/(name+'.json'); path.write_text(json.dumps(c,indent=2,sort_keys=True)+'\n')
    p=subprocess.run([sys.executable,str(checker),str(path)],capture_output=True,text=True)
    (out/(name+'.stdout.txt')).write_text(p.stdout)
    (out/(name+'.stderr.txt')).write_text(p.stderr)
    assert p.returncode != 0 and ('ValueError: '+reasons[name]) in p.stderr, name
    results.append({'id':name,'exit_code':p.returncode,'reason':reasons[name],'status':'REJECTED'})
print(json.dumps({'status':'PASS','rejected':results},indent=2,sort_keys=True))
