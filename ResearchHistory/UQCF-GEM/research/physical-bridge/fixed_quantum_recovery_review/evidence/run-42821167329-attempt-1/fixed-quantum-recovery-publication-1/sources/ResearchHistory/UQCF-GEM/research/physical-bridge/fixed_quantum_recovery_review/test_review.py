import copy,json,tempfile,unittest,sys
from pathlib import Path
import uqcf_fixed_quantum_recovery_review as p
class ProtocolTests(unittest.TestCase):
 def valid(self,verdict='REVISE'):
  return dict(verdict=verdict,findings=['defect'] if verdict=='REVISE' else [],missing_assumptions=[],counterexamples=[],limitations=[],reconstruction=['exact reconstruction'],constructive_analysis=[],native_bridge_status='NOT_DERIVED',next_native_obligation='Earn availability')
 def test_real_manifest_mutations_rejected(self):
  for mutation in ('delete','add','change','wrong_length','wrong_hash','outside'):
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as d:
    r=Path(d);(r/'proof').write_bytes(b'proof');p.manifest(r);p.valid_manifest(r)
    if mutation=='delete':(r/'proof').unlink()
    if mutation=='add':(r/'extra').write_bytes(b'new')
    if mutation=='change':(r/'proof').write_bytes(b'wrong')
    if mutation in ('wrong_length','wrong_hash','outside'):
     m=json.loads((r/'artifact_manifest.json').read_text())
     if mutation=='wrong_length':m['proof']['bytes']+=1
     if mutation=='wrong_hash':m['proof']['sha256']='0'*64
     if mutation=='outside':m['../proof']=m.pop('proof')
     (r/'artifact_manifest.json').write_text(json.dumps(m))
    with self.assertRaises(AssertionError):p.valid_manifest(r)
 def test_reject_repeated_or_uncertain_generation(self):
  p.generation_guard('1','fixed',[])
  with self.assertRaises(AssertionError):p.generation_guard('2','fixed',[])
  with self.assertRaises(AssertionError):p.generation_guard('1','fixed',[dict(note_sha256='fixed',review_attempted=True)])
 def test_adverse_verdict_not_infrastructure_error(self):p.validate_verdict(self.valid())
 def test_false_acceptance_rejected(self):
  v=self.valid();v['verdict']='ACCEPTED'
  with self.assertRaises(AssertionError):p.validate_verdict(v)
 def test_empty_reconstruction_rejected(self):
  v=self.valid();v['reconstruction']=[]
  with self.assertRaises(AssertionError):p.validate_verdict(v)
 def test_raw_native_label_not_silently_rewritten(self):
  v=self.valid();v['native_bridge_status']='DERIVED_FROM_SOURCES';p.validate_verdict(v);self.assertEqual(v['native_bridge_status'],'DERIVED_FROM_SOURCES')
 def test_identity_mutations_rejected(self):
  ident=dict(scientific_sha='a',review_freeze_sha='b',checkout_sha='c',workflow_sha='c',run_id='1',run_attempt='1');p.validate_identity(ident,ident)
  for key in ident:
   changed=dict(ident);changed[key]='wrong'
   with self.assertRaises(AssertionError):p.validate_identity(changed,ident)
 def test_original_attempt_not_hidden_by_later_skipped_job(self):
  from unittest.mock import patch
  seen=[]
  def api(path):
   seen.append(path)
   if 'filter=all' in path:return {'jobs':[{'name':'review','status':'completed','conclusion':'success'},{'name':'review','status':'completed','conclusion':'skipped'}]}
   return {'jobs':[{'name':'review','status':'completed','conclusion':'skipped'}]}
  with patch.object(p,'api_json',api):self.assertTrue(p.prior_review_attempted('123'))
  self.assertIn('filter=all',seen[0])
 def test_request_config_and_model_metadata_mutations_rejected(self):
  prompt=b'fixed';v={'contents':[{'role':'user','parts':[{'text':'fixed'}]}],'generationConfig':{'temperature':0,'maxOutputTokens':32768,'responseMimeType':'application/json'}}
  raw=(json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n').encode();meta=json.dumps({'name':'models/gemini-3.1-pro-preview','supportedGenerationMethods':['generateContent']}).encode()
  p.validate_model_request(raw,meta,prompt)
  for key,value in [('temperature',1),('maxOutputTokens',2),('responseMimeType','text/plain')]:
   changed=copy.deepcopy(v);changed['generationConfig'][key]=value
   with self.assertRaises(AssertionError):p.validate_model_request((json.dumps(changed,ensure_ascii=False,sort_keys=True)+'\n').encode(),meta,prompt)
  for obj in [{'name':'models/wrong','supportedGenerationMethods':['generateContent']},{'name':'models/gemini-3.1-pro-preview','supportedGenerationMethods':[]}]:
   with self.assertRaises(AssertionError):p.validate_model_request(raw,json.dumps(obj).encode(),prompt)
 def test_source_packet_mutations_rejected(self):
  b=b'exact';s=dict(content='exact',bytes=len(b),sha256=p.sha(b),blob=p.blob(b));p.validate_remote_source(s,b,p.blob(b))
  for field,value in [('content','altered'),('bytes',6),('sha256','0'*64),('blob','0'*40)]:
   t=copy.deepcopy(s);t[field]=value
   with self.assertRaises(AssertionError):p.validate_remote_source(t,b,p.blob(b))
if __name__=='__main__':unittest.main()
