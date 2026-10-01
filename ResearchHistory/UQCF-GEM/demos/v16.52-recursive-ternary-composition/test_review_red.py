"""Real partial-transport loss and absent assertion binding, before review fixes."""
import copy, unittest, hashlib, ast
from unittest.mock import patch
import producer as p
import integrity as integrity

class ReviewControls(unittest.TestCase):
 def test_transport_partial_path_retained(self):
  t=p.TREES['G'];s=p.canonical(t,3,[2]*4);child=p.layout(t)[0][0]
  original=p.replace_role;emitted=[]
  def fail_after_real_moves(current,nodes,c,x,y,path):
   original(current,nodes,c,x,y,path);emitted[:]=copy.deepcopy(path)
   raise ValueError('INJECTED_AFTER_REAL_TRANSPORT')
  with patch.object(p,'replace_role',side_effect=fail_after_real_moves):
   try:p.transport_child(s,t,child,[0,1],[1,0],[0,1,2])
   except Exception as exc:retained=getattr(exc,'path',[])
   else:self.fail('injected failure escaped')
  self.assertGreater(len(emitted),1)
  self.assertEqual(retained,emitted,'PARTIAL_TRANSPORT_PATH_LOST')
 def test_assertion_manifest_rejects_hash_mutation(self):
  self.assertTrue(callable(getattr(integrity,'verify_test_manifest',None)),'MISSING_NEW_ASSERTION_BINDING')
  source='class Example:\n def test_value(self):\n  assert 1 == 1\n'
  node=ast.parse(source).body[0].body[0]
  manifest={'count':1,'tests':[{'identity':'example.Example.test_value','expected':'PASS','assertions_sha256':hashlib.sha256(ast.get_source_segment(source,node).encode()).hexdigest()}]}
  integrity.verify_test_manifest(manifest,{'example':source})
  bad=copy.deepcopy(manifest);bad['tests'][0]['assertions_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'assertion manifest'):integrity.verify_test_manifest(bad,{'example':source})
 def test_resource_failure_is_incomplete(self):
  import verifier as v
  import run_campaign
  with patch.object(p,'_normalize',side_effect=MemoryError('INJECTED_RESOURCE_EXHAUSTION')):doc=p.produce()
  self.assertEqual(len(doc['cases']),7236)
  try:v.verify(doc)
  except Exception as exc:outcome=run_campaign.failure_outcome(exc)
  else:self.fail('resource failure was accepted')
  self.assertEqual(outcome,'INCOMPLETE','RESOURCE_FAILURE_MISCLASSIFIED')

if __name__=='__main__':unittest.main(verbosity=2)
