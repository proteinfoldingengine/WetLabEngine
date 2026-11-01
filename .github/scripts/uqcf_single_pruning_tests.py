"""Evidence-plumbing controls only; no scientific code imports."""
import copy,gzip,hashlib,unittest
from uqcf_single_pruning_review import verify_source_excerpt
from uqcf_single_pruning_publication import audit_source_excerpt
from uqcf_preparability_review import accepted
class EvidenceControls(unittest.TestCase):
 def setUp(self):
  self.raw=gzip.compress(b'prefix target suffix',mtime=0)
  self.s=dict(commit='0'*40,path='x.gz',full_bytes=len(self.raw),full_sha256=hashlib.sha256(self.raw).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(self.raw)).encode()+b'\0'+self.raw).hexdigest(),compression='gzip',decoded_bytes=20,decoded_sha256=hashlib.sha256(b'prefix target suffix').hexdigest(),byte_start=7,byte_end=13,content='target')
 def both(self,s,raw):
  for fn in (verify_source_excerpt,audit_source_excerpt):
   with self.subTest(fn=fn.__name__):fn(s,raw)
 def reject_both(self,s,raw):
  for fn in (verify_source_excerpt,audit_source_excerpt):
   with self.subTest(fn=fn.__name__),self.assertRaises(ValueError):fn(s,raw)
 def test_valid(self):self.both(self.s,self.raw)
 def test_bad_compressed_bytes(self):self.reject_both(self.s,self.raw+b'x')
 def test_false_decoded_identity(self):
  s=copy.deepcopy(self.s);s['decoded_sha256']='0'*64;self.reject_both(s,self.raw)
 def test_wrong_excerpt(self):
  s=copy.deepcopy(self.s);s['content']='TARGET';self.reject_both(s,self.raw)
 def test_wrong_interval(self):
  s=copy.deepcopy(self.s);s['byte_start']=6;self.reject_both(s,self.raw)
 def test_bad_path(self):
  s=copy.deepcopy(self.s);s['path']='../x.gz';self.reject_both(s,self.raw)
 def test_nonclean_acceptance_rejected(self):
  with self.assertRaises((ValueError,AssertionError)):accepted(dict(verdict='ACCEPTED',findings=['unresolved error'],missing_assumptions=[],counterexamples=[]))
if __name__=='__main__':unittest.main()
