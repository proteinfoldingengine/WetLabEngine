import importlib,unittest
class Tests(unittest.TestCase):
 def m(self):return importlib.import_module('engine'),importlib.import_module('verify')
 def test_path_total(self):
  e,v=self.m();d=e.find_witness(4);self.assertIsNotNone(d);v.verify_witness(d);self.assertEqual(sum(x['delta_h'] for x in d['path_a']),sum(x['delta_h'] for x in d['path_b']))
 def test_same_event_changes(self):
  e,v=self.m();d=e.find_witness(4);v.verify_witness(d);self.assertTrue(d['changed_events'])
 def test_corrupt_delta_rejected(self):
  e,v=self.m();d=e.find_witness(4);d['path_a'][0]['delta_h']=9
  with self.assertRaises(ValueError):v.verify_witness(d)
 def test_endpoint_mismatch_rejected(self):
  e,v=self.m();d=e.find_witness(4);d['after'][0]=d['before'][0]
  with self.assertRaises(ValueError):v.verify_witness(d)
 def test_complete_bounded_search(self):
  e,v=self.m();doc=e.produce(4);r=v.verify_document(doc,4);self.assertGreater(r['endpoints'],0)
if __name__=='__main__':unittest.main(verbosity=2)
