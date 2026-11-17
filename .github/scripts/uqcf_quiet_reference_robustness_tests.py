"""Review-plumbing controls only; no mathematical simulation or model call."""
import copy, hashlib, importlib, json, tempfile, unittest
from pathlib import Path

try:
    m = importlib.import_module('uqcf_quiet_reference_robustness_review')
except ModuleNotFoundError:
    m = None

ROOT=Path(__file__).resolve().parents[2]
PACKET=ROOT/'ResearchHistory/UQCF-GEM/research/physical-bridge/quiet_reference_robustness/review/SOURCE_PACKET.json'

class ReviewControls(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(m, 'Frozen-note review controller is not implemented')
        self.raw=PACKET.read_bytes(); self.digest=hashlib.sha256(self.raw).hexdigest()
        self.packet=json.loads(self.raw)
        self.identity={'run_id':'123','run_attempt':'1','checkout_sha':'a'*40,'workflow_sha':'a'*40}

    def test_rejects_changed_packet_before_source_use(self):
        with self.assertRaises(ValueError): m.load_packet(self.raw+b' ',self.digest)

    def test_rejects_missing_duplicate_and_changed_sources(self):
        for mutation in ('missing','duplicate','content'):
            p=copy.deepcopy(self.packet)
            if mutation=='missing': p['documents'].pop()
            elif mutation=='duplicate': p['documents'].append(copy.deepcopy(p['documents'][0]))
            else: p['documents'][0]['content']+='CHANGED'
            raw=json.dumps(p).encode()
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                m.load_packet(raw,hashlib.sha256(raw).hexdigest())

    def test_rejects_different_remote_source_bytes(self):
        with self.assertRaises(ValueError):
            m.load_packet(self.raw,self.digest,remote=lambda record:b'wrong remote bytes')

    def test_prompt_contains_each_exact_document_once(self):
        p=m.load_packet(self.raw,self.digest)
        prompt=m.prompt_for(p)
        for doc in p['documents']:
            self.assertIn(doc['content'].encode(),prompt)
            self.assertEqual(prompt.count(('EXACT DOCUMENT '+doc['id']+'\n').encode()),1)

    def test_generation_is_forbidden_on_retry(self):
        m.first_attempt('1')
        for attempt in ('2','0','',None):
            with self.subTest(attempt=attempt),self.assertRaises(ValueError):m.first_attempt(attempt)

    def make_bundle(self,path,verdict=None):
        v=verdict or {'verdict':'ACCEPTED','findings':[],'missing_assumptions':[],
             'counterexamples':[],'limitations':['SUPPLIED benchmark'],
             'native_bridge_status':'NOT_DERIVED'}
        answer=json.dumps(v,sort_keys=True)
        response={'modelVersion':'gemini-3.1-pro-preview','candidates':[{
          'finishReason':'STOP','content':{'role':'model','parts':[{'text':answer}]}}]}
        prompt=m.prompt_for(self.packet)
        request={'contents':[{'role':'user','parts':[{'text':prompt.decode()}]}],
                 'generationConfig':{'temperature':0,'maxOutputTokens':32768,'responseMimeType':'application/json'}}
        files={'response.json':response,'verdict.json':v,'request.json':request,
          'model_metadata.json':{'name':'models/gemini-3.1-pro-preview','supportedGenerationMethods':['generateContent']},
          'manifest.json':{**self.identity,'source_packet_sha256':self.digest,'model_requested':'gemini-3.1-pro-preview'}}
        for name,obj in files.items():(path/name).write_text(json.dumps(obj,sort_keys=True)+'\n')
        (path/'review.txt').write_text(answer)
        (path/'prompt.txt').write_bytes(prompt)

    def test_complete_raw_review_is_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); self.make_bundle(p)
            self.assertEqual(m.audit_review(p,self.packet,self.identity,self.digest)['verdict'],'ACCEPTED')

    def test_rejects_truncation_wrong_model_defects_and_native_promotion(self):
        for change in ('truncated','wrong_model','defect','native'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                p=Path(d);self.make_bundle(p)
                raw=json.loads((p/'response.json').read_text())
                if change=='truncated':raw['candidates'][0]['finishReason']='MAX_TOKENS'
                elif change=='wrong_model':raw['modelVersion']='different-model'
                else:
                    v=json.loads(raw['candidates'][0]['content']['parts'][0]['text'])
                    if change=='defect':v['findings']=['undischarged claim']
                    else:v['native_bridge_status']='DERIVED_FROM_SOURCES'
                    answer=json.dumps(v,sort_keys=True); raw['candidates'][0]['content']['parts'][0]['text']=answer
                    (p/'review.txt').write_text(answer);(p/'verdict.json').write_text(json.dumps(v)+'\n')
                (p/'response.json').write_text(json.dumps(raw)+'\n')
                with self.assertRaises(ValueError):m.audit_review(p,self.packet,self.identity,self.digest)

    def test_rejects_altered_prompt_verdict_and_run_identity(self):
        for change in ('prompt','verdict','identity'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                p=Path(d);self.make_bundle(p)
                if change=='prompt':(p/'prompt.txt').write_text('substituted prompt')
                elif change=='verdict':
                    v=json.loads((p/'verdict.json').read_text());v['limitations']=[]
                    (p/'verdict.json').write_text(json.dumps(v)+'\n')
                else:
                    v=json.loads((p/'manifest.json').read_text());v['checkout_sha']='b'*40
                    (p/'manifest.json').write_text(json.dumps(v)+'\n')
                with self.assertRaises(ValueError):m.audit_review(p,self.packet,self.identity,self.digest)


if __name__=='__main__':unittest.main(verbosity=2)
