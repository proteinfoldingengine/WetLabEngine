"""Separate immutable readback and review-evidence audit; no science execution."""
import hashlib
import json
import os
from pathlib import Path
import urllib.request

SCIENCE='1bee2d318e2c5ff3d2146637af9236b6c805ba26'
PREFIX='ResearchHistory/UQCF-GEM/research/physical-bridge/source_enabled_record/'
OUT=Path('source_enabled_review')

def fetch(sha,path):
    with urllib.request.urlopen('https://raw.githubusercontent.com/proteinfoldingengine/WetLabEngine/'+sha+'/'+path,timeout=60) as r:
        return r.read()

def main():
    records={}
    for n,expected in json.loads((OUT/'artifact_manifest.json').read_bytes()).items():
        b=(OUT/n).read_bytes()
        if len(b)!=expected['bytes'] or hashlib.sha256(b).hexdigest()!=expected['sha256']:
            raise ValueError('Artifact mismatch')
    integrity=json.loads((OUT/'integrity.json').read_bytes())
    review=json.loads((OUT/'review_identity.json').read_bytes())
    if integrity['status']!='PASS' or integrity['scientific_execution'] is not False:
        raise ValueError('Invalid integrity evidence')
    for field in ['scientific_sha','checkout_sha','workflow_sha','run_id','run_attempt']:
        if integrity[field]!=review[field]: raise ValueError('Identity mismatch')
    if review['scientific_sha']!=SCIENCE or review['run_id']!=os.environ['GITHUB_RUN_ID']:
        raise ValueError('Wrong reviewed run')
    p=(OUT/'prompt.txt').read_bytes()
    if hashlib.sha256(p).hexdigest()!=review['prompt_sha256']: raise ValueError('Prompt mismatch')
    for name,h in integrity['documents'].items():
        raw=fetch(SCIENCE,PREFIX+name)
        if hashlib.sha256(raw).hexdigest()!=h: raise ValueError('Remote document mismatch')
        block=('\nEXACT DOCUMENT '+name+'\nUTF8-BYTES '+str(len(raw))+'\n').encode()+raw+b'\nEND EXACT DOCUMENT\n'
        if p.count(block)!=1: raise ValueError('Exact document absent or duplicated in prompt')
        records[name]=h
    packet=json.loads(fetch(SCIENCE,PREFIX+'SOURCE_PACKET.json'))
    for source,locked in zip(packet['sources'],integrity['sources'],strict=True):
        b=fetch(packet['source_commit'],source['path'])
        if b!=source['content'].encode() or hashlib.sha256(b).hexdigest()!=locked['sha256']:
            raise ValueError('Dependency mismatch')
    request=json.loads((OUT/'request.json').read_bytes())
    if request['contents'][0]['parts'][0]['text'].encode()!=p: raise ValueError('Model request mismatch')
    raw=(OUT/'response.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=review['response_sha256']: raise ValueError('Response mismatch')
    response=json.loads(raw)
    if response['modelVersion']!=review['model_returned']: raise ValueError('Model mismatch')
    candidates=response['candidates']
    if len(candidates)!=1 or candidates[0]['finishReason']!='STOP': raise ValueError('Incomplete review')
    answer='\n'.join(x['text'] for x in candidates[0]['content']['parts'] if not x.get('thought',False) and isinstance(x.get('text'),str)).strip().encode()
    if answer!=(OUT/'review.txt').read_bytes(): raise ValueError('Raw answer mismatch')
    v=json.loads(answer)
    if v!=json.loads((OUT/'verdict.json').read_bytes()): raise ValueError('Verdict mismatch')
    if v['verdict']!='ACCEPTED' or any(v[k] for k in ['findings','missing_assumptions','counterexamples']): raise ValueError('Unresolved findings')
    if v['native_bridge_status']!='NOT_DERIVED': raise ValueError('Scope mismatch')
    receipt={'status':'PASS','scientific_sha':SCIENCE,'run_id':os.environ['GITHUB_RUN_ID'],'documents':records,'source_count':len(packet['sources']),'model':review['model_returned'],'native_bridge':'NOT_DERIVED','scientific_execution':False}
    target=Path('source_enabled_publication');target.mkdir(exist_ok=True)
    (target/'publication.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('Independent exact remote-source and raw-review publication audit PASS.')

if __name__=='__main__': main()
