"""Preserve genuine rejected certificates and independent-verifier exits."""
import copy, json, pathlib, subprocess, sys
out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
certificate=json.load(open(sys.argv[1])); checker=pathlib.Path(__file__).with_name('verify.py')
rows=[]
def run(name,c):
    path=out/(name+'.json'); path.write_text(json.dumps(c,sort_keys=True)+'\n')
    p=subprocess.run([sys.executable,str(checker),str(path)],capture_output=True,text=True)
    (out/(name+'.stdout')).write_text(p.stdout); (out/(name+'.stderr')).write_text(p.stderr)
    assert p.returncode==1 and json.loads(p.stdout)['status']=='REJECTED',name
    rows.append({'name':name,'exit_code':p.returncode,'verifier':json.loads(p.stdout)})
for name in ['empty','missing','duplicate','substituted','invalid_carrier','wrong_P','wrong_S','false_source','false_witness']:
    c=copy.deepcopy(certificate)
    if name=='empty': c['records']=[]
    elif name=='missing': c['records'].pop()
    elif name=='duplicate': c['records'].append(copy.deepcopy(c['records'][0]))
    elif name=='substituted': c['records'][-1]=copy.deepcopy(c['records'][0])
    elif name=='invalid_carrier': c['records'][0]['Y']=[[9]]
    elif name=='wrong_P': c['records'][0]['P'][0][0]+=1
    elif name=='wrong_S': c['records'][0]['S'][0][0]+=1
    elif name=='false_source': c['source_sha']='0'*40
    elif name=='false_witness': c['witness']['blind_R']=[0,1]
    run(name,c)
print(json.dumps({'status':'PASS','rejected':rows},sort_keys=True))
