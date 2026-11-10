import http.client,io,json,tempfile,unittest,urllib.error,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'.github/scripts'))
if not (Path.cwd()/'.github/scripts/uqcf_preparability_review.py').exists():sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'templates'))
from uqcf_preparability_review import parse_response
from review_transport import call_model
class TransportTests(unittest.TestCase):
 def test_http_failure_body_durable_without_retry(self):
  count=[]
  def opener(req,timeout):
   count.append(req.get_method())
   if req.get_method()=='GET':return io.BytesIO(json.dumps(dict(name='models/gemini-3.1-pro-preview',supportedGenerationMethods=['generateContent'])).encode())
   raise urllib.error.HTTPError(req.full_url,503,'unavailable',{},io.BytesIO(b'{"error":"test failure"}'))
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   with self.assertRaises(urllib.error.HTTPError):call_model(p,'FAKE_TEST_KEY',b'example',opener=opener)
   self.assertEqual(count,['GET','POST'])
   self.assertTrue((p/'response.json').exists(),'Raw failed response was not preserved')
   self.assertEqual((p/'response.json').read_bytes(),b'{"error":"test failure"}')
 def test_partial_response_read_failure_preserved(self):
  class Partial(io.BytesIO):
   def read(self,*a):raise http.client.IncompleteRead(b'partial response',100)
  calls=[]
  def opener(req,timeout):
   calls.append(req.get_method())
   if req.get_method()=='GET':return io.BytesIO(json.dumps(dict(name='models/gemini-3.1-pro-preview',supportedGenerationMethods=['generateContent'])).encode())
   return Partial()
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   with self.assertRaises(http.client.IncompleteRead):call_model(p,'FAKE_TEST_KEY',b'fixed',opener=opener)
   self.assertTrue((p/'response.partial').exists(),'Partial response bytes lost')
   self.assertEqual((p/'response.partial').read_bytes(),b'partial response')
   self.assertEqual(json.loads((p/'transport_failure.json').read_bytes())['outcome'],'UNCERTAIN')
   self.assertEqual(calls,['GET','POST'])
 def test_thought_excluded_opaque_bytes_unchanged(self):
  raw=json.dumps({'modelVersion':'gemini-3.1-pro-preview','candidates':[{'finishReason':'STOP','content':{'parts':[{'thought':True,'text':'not ordinary answer','thoughtSignature':'opaque/+=='},{'text':json.dumps(dict(verdict='REVISE',findings=['x'],missing_assumptions=[],counterexamples=[],limitations=[]))}]}}]}).encode()
  before=raw[:];answer,v,m=parse_response(raw)
  self.assertEqual(raw,before);self.assertNotIn(b'not ordinary',answer);self.assertEqual(v['verdict'],'REVISE')
if __name__=='__main__':unittest.main()
