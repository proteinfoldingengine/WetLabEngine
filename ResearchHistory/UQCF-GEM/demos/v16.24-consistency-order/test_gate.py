"""v16.24 tests frozen before implementation. Checker controls are not physical results."""
import copy
import importlib
import json
from fractions import Fraction as F
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
REJECTIONS=[]
class Tests(unittest.TestCase):
 def modules(self):
  for name in ('engine','verify'):
   self.assertTrue((HERE/(name+'.py')).is_file(),'expected wiring RED: missing '+name)
  return importlib.import_module('engine'),importlib.import_module('verify')
 def fixture(self):
  e,_=self.modules();return e.certify((-1,0,0,0),[(0,1),(0,2),(0,3)])
 def reject(self,name,mutate):
  _,v=self.modules();d=self.fixture();mutate(d)
  with self.assertRaises(ValueError) as cm:v.verify_case(d)
  REJECTIONS.append({'defect':name,'reason':str(cm.exception)})
 def test_root_and_path(self):
  e,v=self.modules()
  for p,views in [((-1,),[(0,)]),((-1,0,1),[(0,),(0,1),(0,1,2)])]:
   d=e.certify(p,views);self.assertEqual(d['h'],1);v.verify_case(d)
 def test_two_and_three_view_parent_witnesses(self):
  e,v=self.modules()
  for leaves in (2,3):
   p=(-1,)+(0,)*leaves;ys=[(0,i) for i in range(1,leaves+1)]
   d=e.certify(p,ys);self.assertEqual(d['h'],leaves)
   self.assertEqual(d['witness']['global'],[-1]+[1]*leaves);v.verify_case(d)
 def test_four_way_sharpness(self):
  e,v=self.modules();d=e.certify((-1,0,0,0,0),[(0,1),(0,2),(0,3),(0,4)])
  self.assertEqual(d['h'],4);v.verify_case(d)
 def test_branch_count_not_exact_cover_number(self):
  e,v=self.modules();d=e.certify((-1,0,0,0,0),[(0,1,2),(0,3,4)])
  self.assertEqual(d['h'],2);v.verify_case(d)
 def test_full_view_and_redundancy(self):
  e,v=self.modules();p=(-1,0,0);ys=[(0,1),(0,2),(0,1,2)]
  self.assertEqual(e.threshold(p,ys),1)
  self.assertEqual(e.threshold(p,ys+[(0,1)]),1)
  v.verify_case(e.certify(p,ys+[(0,1)]))
 def test_binary_views_sufficiency(self):
  e,v=self.modules();d=e.certify((-1,0,0,1,1),[(0,1,3),(0,1,4),(0,2)])
  self.assertEqual(d['h'],2);v.verify_case(d)
 def test_order_is_worst_case_not_every_input(self):
  e,_=self.modules();d=self.fixture()
  self.assertIn(0,[r[1] for r in d['samples']]);self.assertGreater(d['h'],1)
 def test_exact_rational_pushforward(self):
  e,_=self.modules();self.assertEqual(e.push((-1,0,0),(0,1),(F(1,3),F(1,2),F(1,6))),(F(1,2),F(1,2)))
 def test_invalid_parent_types_cycles(self):
  e,v=self.modules()
  for p in [(),(-1,True),(-1,0.0),(-1,2,1),(-1,4),(-1,-1)]:
   with self.subTest(p=p):
    with self.assertRaises(ValueError):e.threshold(p,[(0,)])
 def test_invalid_view_and_union(self):
  e,_=self.modules()
  for ys in [[],[(1,)],[(0,2)],[(0,0,1)],[(0,True)],[(0,1)]]:
   with self.subTest(views=ys):
    with self.assertRaises(ValueError):e.threshold((-1,0,1),ys)
 def test_inexact_scalar_rejected(self):
  e,_=self.modules()
  for x in [(0.0,1,0),(False,1,0),('NaN',1,0),(1,2)]:
   with self.assertRaises(ValueError):e.push((-1,0,0),(0,1),x)
 def test_changed_lineage_and_storage(self):
  e,v=self.modules();a=e.certify((-1,0,0,1,1),[(0,1,3),(0,1,4),(0,2)])
  b=e.certify((-1,4,4,0,0),[(3,0),(1,4,0),(2,4,0)])
  self.assertEqual(v.verify_case(a)['h'],v.verify_case(b)['h'])
 def test_valid_dual_and_rescaling(self):
  _,v=self.modules();d=self.fixture();w=d['witness']
  v.check_dual(d['parents'],d['views'],w['local'],w['dual'],w['vertex'])
  v.check_dual(d['parents'],d['views'],w['local'],[2*x for x in w['dual']],w['vertex'])
 def test_false_low_threshold(self):self.reject('false-low-threshold',lambda d:d.__setitem__('h',1))
 def test_false_high_threshold(self):self.reject('false-high-threshold',lambda d:d.__setitem__('h',4))
 def test_false_child_cover(self):self.reject('false-child-cover',lambda d:d['child_covers'][0].__setitem__('support',[0]))
 def test_corrupt_global_witness(self):self.reject('corrupt-global-witness',lambda d:d['witness']['global'].__setitem__(0,0))
 def test_corrupt_local_marginal(self):self.reject('corrupt-local-marginal',lambda d:d['witness']['local'][0].__setitem__(0,99))
 def test_corrupt_dual(self):self.reject('corrupt-dual',lambda d:d['witness']['dual'].__setitem__(0,99))
 def test_missing_sample(self):self.reject('missing-sample',lambda d:d['samples'].pop())
 def test_false_sample_verdict(self):
  def change(d):
   row=next(r for r in d['samples'] if r[1]);row[1]=0
  self.reject('false-sample-feasibility',change)
 def test_foreign_origin(self):self.reject('foreign-origin',lambda d:d.__setitem__('genesis','another-origin'))
 def test_missing_required_field(self):self.reject('missing-child-ledger',lambda d:d.pop('child_covers'))
 def test_metadata_boolean_not_integer(self):self.reject('boolean-threshold',lambda d:d.__setitem__('h',True))
 def test_linear_but_nonnatural_control(self):
  _,v=self.modules();s=v.sp;P=s.Matrix([[1,1,1]]);I=s.Matrix([0,1,0]);A=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
  self.assertEqual(P*I,s.eye(1))
  with self.assertRaises(ValueError):v.check_section(P,I,A,s.eye(1))
  v.check_section(P,s.Matrix([1,0,0]),A,s.eye(1))
 def test_missing_cover_rejected(self):
  e,v=self.modules();doc=e.produce(3);doc['instances'][0]['cases'].pop()
  with self.assertRaises(ValueError):v.verify_document(doc,3)
 def test_false_metamorphic_claim(self):
  e,v=self.modules();doc=e.produce(3)
  pair=next((doc['instances'][i:i+2] for i in range(0,len(doc['instances']),2) if len(doc['instances'][i]['parents'])==3 and doc['instances'][i]['parents']==[-1,0,1]),None)
  self.assertIsNotNone(pair);pair[1]['parents']=list(pair[0]['parents'])
  with self.assertRaises(ValueError):v.verify_document(doc,3)
 def test_complete_small_universe(self):
  e,v=self.modules();r=v.verify_document(e.produce(3),3);self.assertGreater(r['covers'],0)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
 out=HERE/'evidence';out.mkdir(exist_ok=True)
 (out/'TEST_RECEIPT.json').write_text(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'rejections':REJECTIONS},indent=2)+'\n')
 raise SystemExit(0 if result.wasSuccessful() else 1)
