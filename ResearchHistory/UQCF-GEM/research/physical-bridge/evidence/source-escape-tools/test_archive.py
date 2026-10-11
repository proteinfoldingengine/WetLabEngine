import unittest,json,hashlib
from audit_helpers import check_review,check_tests,check_inputs,check_log,check_zip
from io import BytesIO
import zipfile
class ArchiveContracts(unittest.TestCase):
 def setUp(self):
  self.event='a'*40;self.raw=json.dumps({'verdict':'ACCEPTED','findings':[],'missing_assumptions':[],'counterexamples':[],'limitations':[]}).encode();self.m={'research_commit':self.event,'workflow_commit':self.event,'response_sha256':hashlib.sha256(self.raw).hexdigest(),'model':'gemini-3.1-pro-preview','attempts':[{'attempt':1,'status':'RESPONSE_RECEIVED'}]}
 def test_intact_review(self):check_review(self.raw,self.m,self.event)
 def test_wrong_commit(self):
  self.m['research_commit']='b'*40
  with self.assertRaises(ValueError):check_review(self.raw,self.m,self.event)
 def test_nonempty_adverse_array(self):
  raw=self.raw.replace(b'"counterexamples": []',b'"counterexamples": ["witness"]');self.m['response_sha256']=hashlib.sha256(raw).hexdigest()
  with self.assertRaises(ValueError):check_review(raw,self.m,self.event)
 def test_wrong_response_hash(self):
  self.m['response_sha256']='0'*64
  with self.assertRaises(ValueError):check_review(self.raw,self.m,self.event)
 def test_compensating_test_counts(self):
  good='test_a ... ok\ntest_b ... ok\nRan 2 tests in 0.1s\n\nOK\n';check_tests(good,2)
  with self.assertRaises(ValueError):check_tests(good,3)
 def test_failed_test(self):
  with self.assertRaises(ValueError):check_tests('test_a ... FAIL\nRan 1 tests in 0.1s\nFAILED (failures=1)\n',1)
 def test_missing_manifest_identity(self):
  actual={'one':b'a','two':b'b'};wanted={k:hashlib.sha256(v).hexdigest() for k,v in actual.items()};check_inputs(wanted,actual)
  del wanted['two']
  with self.assertRaises(ValueError):check_inputs(wanted,actual)
 def test_truncated_full_log(self):
  good='Current runner version '+self.event+' expected digest Cleaning up orphan processes';check_log(good,self.event,'expected digest')
  with self.assertRaises(ValueError):check_log(good.split(' Cleaning')[0],self.event,'expected digest')
 def test_omitted_archive_member(self):
  b=BytesIO()
  with zipfile.ZipFile(b,'w') as z:z.writestr('one.txt','data')
  raw=b.getvalue();check_zip(raw,{'one.txt'})
  with self.assertRaises(ValueError):check_zip(raw,{'one.txt','two.txt'})
if __name__=='__main__':unittest.main(verbosity=2)
