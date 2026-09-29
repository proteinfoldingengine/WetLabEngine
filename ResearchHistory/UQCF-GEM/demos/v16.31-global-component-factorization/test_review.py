"""Self-review boundary regressions; written before correcting the storage bug."""
import json
from pathlib import Path
import unittest
import producer
import verifier
P=Path(__file__).resolve().parent
class Review(unittest.TestCase):
 def test_independently_reordered_final_storage(self):
  p=(-1,0,0,1);a=[(0,1,2,3),(0,1,3)];b=[(2,0),(3,1,0)]
  c=producer.certify(p,a,b);r=verifier.verify_case(c);self.assertEqual(r['states'],3)
 def test_two_nonzero_same_parent_components(self):
  p=(-1,0,0,0,0)
  a=[(0,1,2),(0,1),(0,2),(0,3,4),(0,3),(0,4)]
  b=[(0,),(0,1),(0,2),(0,),(0,3),(0,4)]
  c=producer.certify(p,a,b);verifier.verify_case(c);t=c['local'][0]
  self.assertEqual(len(t['components']),2)
  self.assertEqual([g['values'] for g in t['components']],[[0,1,1,1],[0,1,1,1]])
 def test_missing_witness_is_not_verified(self):
  c=producer.examples()['third_order'];c['edge_witnesses'].pop()
  with self.assertRaises(ValueError):verifier.verify_case(c)
 def test_empty_background_graph_misses_actual_third_order(self):
  c=producer.examples()['third_order'];t=c['local'][0];f=t['values']
  self.assertEqual(f[3]-f[1]-f[2]+f[0],0)
  self.assertEqual(f[7]-f[5]-f[6]+f[4],-1)
  c['edges']=[]
  with self.assertRaises(ValueError):verifier.verify_case(c)
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Review))
 e=P/'evidence';e.mkdir(exist_ok=True);(e/'REVIEW_TESTS.json').write_text(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)},indent=2)+'\n')
 raise SystemExit(0 if r.wasSuccessful() else 1)
