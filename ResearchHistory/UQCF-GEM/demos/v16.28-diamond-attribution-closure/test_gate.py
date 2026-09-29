"""Preregistered v16.28 constructive, destructive and metamorphic controls."""
import ast
import copy
import importlib
import json
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
REJECTIONS=[]
class Tests(unittest.TestCase):
 def modules(self):
  for name in ('producer','verifier'):
   self.assertTrue((HERE/(name+'.py')).is_file(),'wiring RED: missing '+name)
  return importlib.import_module('producer'),importlib.import_module('verifier')
 def negative(self):
  p,_=self.modules();return p.certify((-1,0,0),[(0,1),(0,2),(0,1,2)],[(0,1),(0,2),(0,)])
 def reject(self,label,mutator):
  _,v=self.modules();c=self.negative();mutator(c)
  with self.assertRaises(ValueError) as cm:v.verify_case(c)
  REJECTIONS.append({'defect':label,'reason':str(cm.exception)})
 def test_parent_counterexample(self):
  _,v=self.modules();c=self.negative();r=v.verify_case(c)
  self.assertFalse(c['independent']);self.assertEqual([x[3] for x in c['diamonds']],[-1]);self.assertIsNone(c['weights']);self.assertEqual(r['paths'],2)
 def test_positive_mixed_difference_control(self):
  p,v=self.modules();c=p.certify((-1,0,0),[(0,1,2),(0,1,2)],[(0,2),(0,1)])
  self.assertEqual([x[3] for x in c['diamonds']],[1]);self.assertFalse(c['independent']);v.verify_case(c)
 def test_identity_control(self):
  p,v=self.modules();c=p.certify((-1,),[(0,)],[(0,)])
  self.assertTrue(c['independent']);self.assertEqual(c['weights'],[]);self.assertEqual(c['diamonds'],[]);v.verify_case(c)
 def test_one_event_positive_weight(self):
  p,v=self.modules();c=p.certify((-1,0,0),[(0,1,2),(0,1)],[(0,2),(0,1)])
  self.assertEqual(c['weights'],[1]);v.verify_case(c)
 def test_chain_interval_is_not_a_no_go(self):
  p,v=self.modules();c=p.certify((-1,0,0,1),[(0,1,2,3),(0,1,3)],[(0,2),(0,1,3)])
  self.assertTrue(c['independent']);self.assertEqual(c['diamonds'],[]);self.assertEqual(c['weights'],[1,0]);v.verify_case(c)
 def test_same_total_wrong_coefficients_rejected(self):
  p,v=self.modules();c=p.certify((-1,0,0,1),[(0,1,2,3),(0,1,3)],[(0,2),(0,1,3)])
  c['weights']=[0,1]
  with self.assertRaises(ValueError):v.verify_case(c)
 def test_reordered_records_valid(self):
  _,v=self.modules();c=self.negative();c['states'].reverse();c['diamonds'].reverse();v.verify_case(c)
 def test_actual_lineage_and_storage_relabeling(self):
  p,v=self.modules();c=p.certify((-1,2,0),[(1,2,0),(2,0)],[(2,0),(2,0)])
  self.assertTrue(c['independent']);v.verify_case(c)
 def test_illegal_inputs_rejected(self):
  p,v=self.modules()
  for par,a,b in [((-1,2,1),[(0,1,2)],[(0,1,2)]),((-1,True),[(0,1)],[(0,1)]),((-1,0,1),[(0,2)],[(0,)]),((-1,0),[(0,1)],[(0,)])]:
   with self.subTest(par=par):
    with self.assertRaises(ValueError):p.certify(par,a,b)
 def test_changed_union_rejected_by_verifier(self):
  self.reject('changed-union',lambda c:c.__setitem__('after',[[0],[0],[0]]))
 def test_false_h(self):self.reject('false-state-value',lambda c:c['states'][0].__setitem__(1,99))
 def test_boolean_h(self):self.reject('boolean-state-value',lambda c:c['states'][0].__setitem__(1,True))
 def test_false_mixed_difference(self):self.reject('false-mixed-difference',lambda c:c['diamonds'][0].__setitem__(3,0))
 def test_missing_diamond(self):self.reject('missing-diamond',lambda c:c['diamonds'].pop())
 def test_missing_state(self):self.reject('missing-state',lambda c:c['states'].pop())
 def test_false_independence(self):self.reject('false-independence',lambda c:c.__setitem__('independent',True))
 def test_fitted_weights_not_accepted(self):self.reject('fitted-weights',lambda c:c.__setitem__('weights',[1,0]))
 def test_missing_predecessor_field(self):self.reject('missing-predecessors',lambda c:c.pop('predecessors'))
 def test_wrong_event_identity(self):self.reject('wrong-event',lambda c:c['events'][0].__setitem__(1,99))
 def test_wrong_witness_path(self):self.reject('wrong-witness-path',lambda c:c['witness']['path_a'].__setitem__(0,c['witness']['path_a'][1]))
 def test_false_witness_heights(self):self.reject('wrong-witness-height',lambda c:c['witness']['heights_a'].__setitem__(0,99))
 def test_missing_witness(self):self.reject('missing-witness',lambda c:c.__setitem__('witness',None))
 def test_foreign_origin(self):self.reject('foreign-origin',lambda c:c.__setitem__('genesis','other'))
 def test_missing_endpoint(self):
  p,v=self.modules();d=p.produce(3);x=next(x for x in d['instances'] if x['cases']);x['cases'].pop()
  with self.assertRaises(ValueError):v.verify_document(d,3)
 def test_missing_shape(self):
  p,v=self.modules();d=p.produce(3);d['instances'].pop()
  with self.assertRaises(ValueError):v.verify_document(d,3)
 def test_false_metamorphic_copy(self):
  p,v=self.modules();d=p.produce(3);old=next(x for x in d['instances'] if x['variant']=='original' and x['parents']==[-1,0,1]);new=next(x for x in d['instances'] if x['code']==old['code'] and x['variant']=='relabeled');new['parents']=old['parents'][:]
  with self.assertRaises(ValueError):v.verify_document(d,3)
 def test_complete_small_universe(self):
  p,v=self.modules();r=v.verify_document(p.produce(3),3)
  self.assertEqual(r['execution_status'],'COMPLETED');self.assertGreater(r['original']['endpoints'],0)
 def test_verifier_does_not_import_producer(self):
  self.modules();tree=ast.parse((HERE/'verifier.py').read_text());names=[]
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):names.extend(a.name for a in node.names)
   if isinstance(node,ast.ImportFrom):names.append(node.module or '')
  self.assertFalse(any('producer' in n or 'engine' in n or 'importlib' in n for n in names))
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
 e=HERE/'evidence';e.mkdir(exist_ok=True)
 (e/'TESTS.json').write_text(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'rejections':REJECTIONS},indent=2)+'\n')
 raise SystemExit(0 if result.wasSuccessful() else 1)
