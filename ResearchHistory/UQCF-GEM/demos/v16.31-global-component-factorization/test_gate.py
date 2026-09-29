"""Pre-implementation rejecting checks. Synthetic controls are not retained results."""
import ast
import copy
import importlib
import json
from pathlib import Path
import unittest
P=Path(__file__).resolve().parent
CHAIN=((-1,0,0,1),[(0,1,2,3),(0,1,3)],[(0,2),(0,1,3)])
THREE=((-1,0,0,0),[(0,1,2,3),(0,1),(0,2),(0,3)],[(0,),(0,1),(0,2),(0,3)])
REJECTIONS=[]
class Tests(unittest.TestCase):
 def modules(self):
  for n in ('producer','verifier'):self.assertTrue((P/(n+'.py')).is_file(),'wiring RED: missing '+n)
  return importlib.import_module('producer'),importlib.import_module('verifier')
 def case(self,fixture=CHAIN):
  p,_=self.modules();return p.certify(*fixture)
 def reject(self,label,change):
  _,v=self.modules();c=self.case();change(c)
  with self.assertRaises(ValueError) as cm:v.verify_case(c)
  REJECTIONS.append({'defect':label,'reason':str(cm.exception)})
 def test_noncartesian_nonconstant_chain(self):
  _,v=self.modules();c=self.case();r=v.verify_case(c)
  self.assertEqual(len(c['states']),3);self.assertEqual(c['product_states'],4)
  self.assertEqual(c['edges'],[]);self.assertNotEqual(c['states'][0][1],c['states'][-1][1]);self.assertEqual(r['cases'],1)
 def test_identity(self):
  p,v=self.modules();c=p.certify((-1,),[(0,)],[(0,)])
  self.assertEqual(c['events'],[]);self.assertEqual(c['states'],[[0,[0]]]);v.verify_case(c)
 def test_retained_third_order(self):
  _,v=self.modules();c=self.case(THREE);v.verify_case(c)
  t=next(t for t in c['local'] if t['vertex']==0);self.assertEqual(t['mobius'][-1],-1);self.assertEqual(len(t['components']),1)
 def test_synthetic_cubic_all_background_not_baseline(self):
  _,v=self.modules();r=v.boolean_audit([0,0,0,0,0,0,0,1])
  self.assertEqual(r['mobius'][-1],1);self.assertEqual(r['edges'],[[0,1],[0,2],[1,2]])
 def test_synthetic_separate_components(self):
  _,v=self.modules();vals=[1+int(bool(s&1))+int(bool(s&2) and bool(s&4)) for s in range(8)]
  r=v.boolean_audit(vals);self.assertEqual(r['components'],[[0],[1,2]])
 def test_wrong_cube_shape(self):
  _,v=self.modules()
  for x in ([0,1,2],[0,True],[0,1.0]):
   with self.assertRaises(ValueError):v.boolean_audit(x)
 def test_valid_reversed_records(self):
  _,v=self.modules();c=self.case(THREE);c['states'].reverse();c['local'].reverse();v.verify_case(c)
 def test_actual_relabeling_and_view_storage(self):
  p,v=self.modules();par,a,b=CHAIN;pi=[0,3,2,1];q=[-1]*4
  for n in range(1,4):q[pi[n]]=pi[par[n]]
  tr=lambda y:[tuple(pi[n] for n in reversed(z)) for z in reversed(y)]
  c=p.certify(q,tr(a),tr(b));v.verify_case(c);self.assertEqual(len(c['states']),3)
 def test_invalid_endpoint_inputs(self):
  p,_=self.modules()
  examples=[((-1,2,1),[(0,1,2)],[(0,1,2)]),((-1,True),[(0,1)],[(0,1)]),((-1,0,1),[(0,2)],[(0,)]),((-1,0),[(0,1)],[(0,)]),((-1,0),[(0,1)],[(0,1),(0,1)])]
  for z in examples:
   with self.subTest(z=z):
    with self.assertRaises(ValueError):p.certify(*z)
 def test_missing_state(self):self.reject('missing-state',lambda c:c['states'].pop())
 def test_false_profile(self):self.reject('false-profile',lambda c:c['states'][0][1].__setitem__(0,99))
 def test_boolean_profile(self):self.reject('boolean-profile',lambda c:c['states'][0][1].__setitem__(0,True))
 def test_wrong_predecessor(self):self.reject('wrong-predecessor',lambda c:c['predecessors'].__setitem__(0,0))
 def test_wrong_parent_prelude(self):self.reject('wrong-prelude',lambda c:c['local'][0].__setitem__('prelude',0))
 def test_wrong_component_values(self):self.reject('wrong-component',lambda c:c['local'][0]['components'][0]['values'].__setitem__(1,99))
 def test_wrong_mobius(self):self.reject('wrong-mobius',lambda c:c['local'][0]['mobius'].__setitem__(1,99))
 def test_missing_local_table(self):self.reject('missing-local',lambda c:c['local'].pop())
 def test_cross_parent_edge(self):self.reject('cross-parent-edge',lambda c:c['edges'].append([0,1]))
 def test_missing_actual_edge(self):
  _,v=self.modules();c=self.case(THREE);c['edges'].pop()
  with self.assertRaises(ValueError):v.verify_case(c)
 def test_fabricated_cartesian_count(self):self.reject('cartesian-confusion',lambda c:c.__setitem__('product_states',3))
 def test_foreign_origin(self):self.reject('foreign-origin',lambda c:c.__setitem__('genesis','foreign'))
 def test_missing_document_sections(self):
  _,v=self.modules()
  with self.assertRaises(ValueError):v.verify_document({'version':'16.31'})
 def test_complete_small_universe(self):
  p,v=self.modules();r=v.verify_document(p.produce(3),3);self.assertEqual(r['execution_status'],'COMPLETED');self.assertGreater(r['original']['cases'],0)
 def test_missing_shape(self):
  p,v=self.modules();d=p.produce(3);d['instances'].pop()
  with self.assertRaises(ValueError):v.verify_document(d,3)
 def test_missing_endpoint(self):
  p,v=self.modules();d=p.produce(3);next(i for i in d['instances'] if i['cases'])['cases'].pop()
  with self.assertRaises(ValueError):v.verify_document(d,3)
 def test_duplicate_endpoint(self):
  p,v=self.modules();d=p.produce(3);i=next(i for i in d['instances'] if i['cases']);i['cases'].append(copy.deepcopy(i['cases'][0]))
  with self.assertRaises(ValueError):v.verify_document(d,3)
 def test_false_relabeling(self):
  p,v=self.modules();d=p.produce(3);i=next(i for i in d['instances'] if i['variant']=='relabeled' and i['parents']==[-1,2,0]);i['parents']=[-1,0,1]
  with self.assertRaises(ValueError):v.verify_document(d,3)
 def test_verifier_no_producer_import(self):
  self.modules();tree=ast.parse((P/'verifier.py').read_text());names=[]
  for n in ast.walk(tree):
   if isinstance(n,ast.Import):names.extend(a.name for a in n.names)
   if isinstance(n,ast.ImportFrom):names.append(n.module or '')
  self.assertFalse(any('producer' in n or 'engine' in n or 'importlib' in n for n in names))
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
 e=P/'evidence';e.mkdir(exist_ok=True);(e/'TESTS.json').write_text(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'rejections':REJECTIONS},indent=2)+'\n')
 raise SystemExit(0 if r.wasSuccessful() else 1)
