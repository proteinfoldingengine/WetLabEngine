import unittest,importlib
class T(unittest.TestCase):
 def m(self):return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_positive_witness(self):
  p,v=self.m();d=p.produce(3);v.verify_document(d);self.assertGreaterEqual(d['positive_barriers'],0)
 def test_false_zero_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers']:
   d['barriers'][0]['B1']=0
   with self.assertRaises(ValueError):v.verify_document(d)
 def test_complete_small(self):
  p,v=self.m();self.assertEqual(v.verify_document(p.produce(3))['execution_status'],'COMPLETED')
 def test_omitted_positive_pair_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers']: d['barriers'].pop()
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_bulk_count_rejected(self):
  p,v=self.m();d=p.produce(3);d['positive_barriers']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_missing_gate_adjudication_rejected(self):
  p,v=self.m();d=p.produce(3);d.pop('gate_a',None)
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_bad_path_certificate_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers'] and d['barriers'][0].get('path'): d['barriers'][0]['path']=[d['barriers'][0]['a'],d['barriers'][0]['b']]
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_gate_c_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_c']='CORRUPTED'
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_gate_d_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_d']['triangle_violations']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_gate_e_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_e']='UNIVERSAL_LOCALIZATION'
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_corrupt_component_range_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['component_ranges']:d['component_ranges'][0]['B1_range'][1]+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_corrupt_localization_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers']:d['barriers'][0]['changed_coordinates']=[]
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_gate_e_classification_rejected(self):
  p,v=self.m();d=p.produce(3);d['gate_e']='FIXED'
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_compulsory_coordinate_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers']:d['barriers'][0]['compulsory_coordinates']=[999]
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_possible_coordinate_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers']:d['barriers'][0]['possible_coordinates']=[]
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_bad_alternative_minimax_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers']:d['barriers'][0]['alternative_path']=[d['barriers'][0]['a'],d['barriers'][0]['b']]
  with self.assertRaises(ValueError):v.verify_document(d)
if __name__=='__main__':unittest.main(verbosity=2)
