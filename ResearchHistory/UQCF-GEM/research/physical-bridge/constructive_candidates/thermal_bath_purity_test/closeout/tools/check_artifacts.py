"""External ZIP/member/digest checks and full initial-to-publication evidence comparison."""
from pathlib import Path, PurePosixPath
import ast
import hashlib
import json
import re
import sys
import zipfile

ROOT=Path(__file__).resolve().parent
EV=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'evidence'
def digest(b): return hashlib.sha256(b).hexdigest()
def check(ok,label):
    if not ok: raise ValueError(label)
def read(p): return json.loads(p.read_bytes())

def unpack(meta):
    p=EV/(meta['name']+'.zip'); raw=p.read_bytes()
    check(digest(raw)==meta['digest'].removeprefix('sha256:'),'API ZIP digest '+meta['name'])
    dest=EV/meta['name']; dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        check(len(names)==len(set(names))==len({n.casefold() for n in names}),'ZIP duplicate')
        for n in names:
            q=PurePosixPath(n)
            check(not q.is_absolute() and '..' not in q.parts and '\\' not in n,'ZIP path')
        check(z.testzip() is None,'ZIP CRC')
        z.extractall(dest)
        files={n for n in names if not n.endswith('/')}
    manifest=read(dest/'artifact_manifest.json')
    check(set(manifest)=={n for n in files if PurePosixPath(n).name!='artifact_manifest.json'},'manifest universe '+meta['name'])
    for n,row in manifest.items():
        b=(dest/n).read_bytes()
        check(len(b)==row['bytes'] and digest(b)==row['sha256'],'member '+n)
    if (dest/'sources/FREEZE.json').exists():
        freeze=read(dest/'sources/FREEZE.json')
        for row in freeze['files']:
            b=(dest/'sources'/row['path']).read_bytes()
            blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            check(len(b)==row['bytes'] and digest(b)==row['sha256'] and blob==row['blob'],'source '+row['path'])
    return {'name':meta['name'],'id':meta['id'],'zip_bytes':len(raw),'zip_sha256':digest(raw),
            'member_count':len(files),'manifest_entries':len(manifest),'status':'PASS'}

def complete():
    ini=EV/'thermal-initial-1'; pub=EV/'thermal-publication-1'
    inherited=EV/'thermal-inherited-1'; inherited2=EV/'thermal-publication-inherited-1'
    rev=EV/'thermal-review-1'
    a=read(ini/'verification.json'); b=read(pub/'verification.json')
    check(a['status']==b['status']=='PASS' and b['fresh_byte_replay'] is True,'thermal passes')
    check(a['deterministic_outputs']==b['deterministic_outputs'],'deterministic hashes')
    for n,h in a['deterministic_outputs'].items():
        check((ini/n).read_bytes()==(pub/n).read_bytes() and digest((ini/n).read_bytes())==h,'fresh bytes '+n)
    for d in (inherited,inherited2):
        receipt=read(d/'receipt.json')
        check(receipt['status']=='PASS' and receipt['checkout_sha']==a['science_sha'],'inherited pass')
        check(read(d/'inherited/VERIFICATION.json')['all_valid'] is True,'FCV all valid')
    for n in ('certificate.json','verification.json','controls.json','inherited/certificates.json.xz',
              'inherited/PRODUCTION.json','inherited/VERIFICATION.json','inherited/REPRODUCED_1615F.json'):
        check((inherited/n).read_bytes()==(inherited2/n).read_bytes(),'fresh inherited bytes '+n)
    identity=read(rev/'review_identity.json'); response=read(rev/'response.json')
    check(identity['science_sha']==a['science_sha'] and identity['generation_requests']==1,'review identity')
    check(identity['response_sha256']==digest((rev/'response.json').read_bytes()),'response SHA')
    candidates=response['candidates']; check(len(candidates)==1 and candidates[0]['finishReason']=='STOP','complete review')
    answer='\n'.join(p['text'] for p in candidates[0]['content']['parts'] if not p.get('thought',False) and isinstance(p.get('text'),str)).strip()
    verdict=json.loads(answer)
    check(answer.encode()==(rev/'review.txt').read_bytes() and verdict==read(rev/'verdict.json'),'parsed response')
    check(response['modelVersion']==identity['model_returned'],'returned model')
    check(read(pub/'review_replay.json')['status']=='PASS' and read(pub/'review_replay.json')['new_model_calls']==0,'review replay')
    # Parse length-framed documents; compare each with the source or execution bytes.
    prompt=(rev/'prompt.txt').read_bytes(); check(digest(prompt)==identity['prompt_sha256'],'prompt SHA')
    controller=(ini/'sources/.github/scripts/uqcf_thermal_closeout.py').read_text()
    tree=ast.parse(controller)
    header=next(ast.literal_eval(n.value).encode() for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HEADER' for t in n.targets))
    check(prompt.startswith(header),'frozen prompt header'); rest=prompt[len(header):]
    documents=read(rev/'documents.json'); seen=set()
    while rest:
        m=re.match(rb'\nEXACT DOCUMENT ([^\n]+)\nUTF8-BYTES ([0-9]+)\n',rest); check(m is not None,'document framing')
        name=m[1].decode(); size=int(m[2]); start=m.end(); raw=rest[start:start+size]
        suffix=b'\nEND EXACT DOCUMENT\n'; check(rest[start+size:].startswith(suffix),'document terminator')
        rest=rest[start+size+len(suffix):]
        check(name not in seen and name in documents,'document identity'); seen.add(name)
        row=documents[name]; check(size==row['bytes'] and digest(raw)==row['sha256'],'document digest')
        if name.startswith('thermal_initial/'):
            expected=ini/name.removeprefix('thermal_initial/')
        elif name.startswith('inherited_initial/'):
            expected=inherited/name.removeprefix('inherited_initial/')
        elif name.endswith('/closeout/FREEZE.json'):
            expected=ini/'sources/FREEZE.json'
        else: expected=ini/'sources'/name
        check(raw==expected.read_bytes(),'independent document bytes '+name)
    check(seen==set(documents),'all review documents')
    request=read(rev/'request.json')
    check(request=={'contents':[{'role':'user','parts':[{'text':prompt.decode()}]}],
        'generationConfig':{'temperature':0,'maxOutputTokens':32768,'responseMimeType':'application/json'}},'request exact')
    return {'status':'PASS','science_sha':a['science_sha'],'deterministic_thermal_outputs':len(a['deterministic_outputs']),
            'deterministic_inherited_outputs':7,'review_documents_checked':len(seen),'verdict':verdict['verdict'],
            'response_sha256':identity['response_sha256'],'native_bridge':'NOT_DERIVED'}

if __name__=='__main__':
    metas=read(EV/'artifacts_api.json')['artifacts']
    reports=[unpack(m) for m in metas if (EV/(m['name']+'.zip')).exists()]
    result={'artifacts':reports}
    if len(reports)==5: result['cross_checks']=complete()
    (EV/'EXTERNAL_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
