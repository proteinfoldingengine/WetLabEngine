import unittest,importlib
class T(unittest.TestCase):
 def m(self):return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_missing_gate_rejected(self):
  p,v=self.m();d=p.produce(3);d.pop('gate_c')
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_barrier_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['pairs']:d['pairs'][0]['B1']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_signature_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['pairs']:d['pairs'][0]['candidate_signature']['q']=[]
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_complete_small(self):
  p,v=self.m();self.assertEqual(v.verify_document(p.produce(3))['execution_status'],'COMPLETED')
 def test_false_group_count_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_c']['groups']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_gate_d_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_d']='FIBER_CONTEXT' if d['gate_d']!='FIBER_CONTEXT' else 'UNRESOLVED'
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_extension_count_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_e']['tested_cases']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_ultrametric_count_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_e']['ultrametric_violations']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_hidden_exclusion_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_e']['excluded'].append({'parents':[-1],'view_count':1,'states':9999,'reason':'EXCLUDED_RESOURCE'})
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_omitted_valid_pair_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['pairs']:d['pairs'].pop()
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_extra_duplicate_pair_rejected(self):
  import copy
  p,v=self.m();d=p.produce(3)
  if d['pairs']:d['pairs'].append(copy.deepcopy(d['pairs'][0]))
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_substituted_pair_rejected(self):
  import copy
  p,v=self.m();d=p.produce(3)
  if len(d['pairs'])>1:
   import json
   def k(r):return (tuple(r['parents']),r['view_count'],tuple(r['q']))
   j=next((j for j in range(1,len(d['pairs'])) if k(d['pairs'][j])!=k(d['pairs'][0])),None)
   if j is not None:d['pairs'][0]=copy.deepcopy(d['pairs'][j])
  with self.assertRaises(ValueError):v.verify_document(d)
if __name__=='__main__':unittest.main(verbosity=2)
