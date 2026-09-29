"""v16.29 preregistered actual-retained controls and rejecting certificates."""
import ast,copy,importlib,json
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
REJECTIONS=[]
NEG=((-1,0,0,1,1),[(0,1,2),(0,1,3,4),(0,2),(0,1,4)],[(0,2),(1,4)])
POS=((-1,0,0,1,1,1),[(0,1,3,4,5),(0,1,3),(0,1,4),(0,2)],[(0,3),(0,4)])
MASK=((-1,0,0,1,1),[(0,1,3,4),(0,1,3),(0,1,4),(0,2)],[(0,3),(0,4)])
class Tests(unittest.TestCase):
 def modules(self):
  for name in ('producer','verifier'):self.assertTrue((HERE/(name+'.py')).exists(),'wiring RED: missing '+name)
  return importlib.import_module('producer'),importlib.import_module('verifier')
 def case(self,spec=NEG):
  p,_=self.modules();return p.certify(*spec)
 def reject(self,name,change):
  _,v=self.modules();c=self.case();change(c)
  with self.assertRaises(ValueError) as cm:v.verify_case(c)
  REJECTIONS.append({'defect':name,'reason':str(cm.exception)})
 def test_negative_max_only(self):
  _,v=self.modules();c=self.case();v.verify_case(c);self.assertEqual(c['heights'],[1,2,2,2]);self.assertEqual(c['local_mixed'],[0]*5);self.assertEqual(c['mechanism'],'MAX_ONLY')
 def test_positive_max_only(self):
  _,v=self.modules();c=self.case(POS);v.verify_case(c);self.assertEqual(c['heights'],[2,2,2,3]);self.assertEqual(c['local_mixed'],[0]*6);self.assertEqual(c['global_mixed'],1);self.assertEqual(c['mechanism'],'MAX_ONLY')
 def test_local_masked(self):
  _,v=self.modules();c=self.case(MASK);v.verify_case(c);self.assertEqual(c['global_mixed'],0);self.assertEqual(c['local_mixed'],[0,-1,0,0,0]);self.assertEqual(c['mechanism'],'LOCAL_MASKED')
 def test_transmitted_negative(self):
  p,v=self.modules();c=p.certify((-1,0,0),[(0,1),(0,2),(0,1,2)],[(2,1),(2,2)]);v.verify_case(c);self.assertEqual(c['local_mixed'][0],-1);self.assertEqual(c['mechanism'],'LOCAL_TRANSMITTED')
 def test_transmitted_positive(self):
  p,v=self.modules();c=p.certify((-1,0,0),[(0,1,2),(0,1,2)],[(0,1),(1,2)]);v.verify_case(c);self.assertEqual(c['global_mixed'],1);self.assertEqual(c['mechanism'],'LOCAL_TRANSMITTED')
 def test_zero_control(self):
  p,v=self.modules();c=p.certify((-1,0),[(0,1)]*3,[(0,1),(1,1)]);v.verify_case(c);self.assertEqual(c['mechanism'],'ZERO')
 def test_reversed_events(self):
  p,v=self.modules();c=p.certify(NEG[0],NEG[1],list(reversed(NEG[2])));v.verify_case(c);self.assertEqual(c['global_mixed'],-1)
 def test_reversed_storage(self):
  p,v=self.modules();c=p.certify(NEG[0],[tuple(reversed(y)) for y in NEG[1]],NEG[2]);v.verify_case(c);self.assertEqual(c['global_mixed'],-1)
 def test_actual_relabeling(self):
  p,v=self.modules();par,a,events=NEG;pi=[0,4,3,2,1];q=[-1]*5
  for x in range(1,5):q[pi[x]]=pi[par[x]]
  c=p.certify(q,[[pi[x] for x in reversed(y)] for y in reversed(a)],[[len(a)-1-i,pi[x]] for i,x in events]);v.verify_case(c);self.assertEqual(c['mechanism'],'MAX_ONLY')
 def test_wrong_local_interaction(self):self.reject('invented-local',lambda c:c['local_mixed'].__setitem__(0,-1))
 def test_wrong_scalar_sign(self):self.reject('wrong-scalar',lambda c:c.__setitem__('global_mixed',1))
 def test_wrong_profile(self):self.reject('wrong-profile',lambda c:c['profiles'][0].__setitem__(0,9))
 def test_wrong_height(self):self.reject('wrong-height',lambda c:c['heights'].__setitem__(0,9))
 def test_wrong_class(self):self.reject('wrong-class',lambda c:c.__setitem__('mechanism','LOCAL_TRANSMITTED'))
 def test_wrong_prediction(self):self.reject('wrong-prediction',lambda c:c.__setitem__('prediction',0))
 def test_wrong_background(self):self.reject('wrong-background',lambda c:c.__setitem__('background',99))
 def test_wrong_state(self):self.reject('wrong-state',lambda c:c['states'].__setitem__(1,[[0]]))
 def test_missing_profile(self):self.reject('missing-profile',lambda c:c.pop('profiles'))
 def test_missing_state(self):self.reject('missing-state',lambda c:c['states'].pop())
 def test_boolean_height(self):self.reject('boolean-height',lambda c:c['heights'].__setitem__(0,True))
 def test_boolean_event(self):self.reject('boolean-event',lambda c:c['events'][0].__setitem__(0,False))
 def test_foreign_origin(self):self.reject('foreign-origin',lambda c:c.__setitem__('genesis','other'))
 def test_wrong_parent_pair(self):self.reject('wrong-parent',lambda c:c.__setitem__('parent_pair',[0,0]))
 def test_invalid_inputs(self):
  p,_=self.modules()
  bad=[((-1,2,1),[(0,1,2)]*3,[(0,1),(1,2)]),((-1,0,1),[(0,1,2)]*3,[(0,1),(1,2)]),((-1,0,0),[(0,1),(0,2)],[(0,1),(1,2)]),((-1,0,0),[(0,1,2)]*2,[(0,1),(0,1)]),((-1,True),[(0,1)]*3,[(0,1),(1,1)])]
  for spec in bad:
   with self.subTest(spec=spec):
    with self.assertRaises(ValueError):p.certify(*spec)
 def test_complete_small_universe(self):
  p,v=self.modules();r=v.verify_document(p.produce(3,False),3,False);self.assertEqual(r['execution_status'],'COMPLETED');self.assertGreater(r['extension']['original']['diamonds'],0)
 def test_missing_case(self):
  p,v=self.modules();d=p.produce(3,False);next(x for x in d['extension'] if x['cases'])['cases'].pop()
  with self.assertRaises(ValueError):v.verify_document(d,3,False)
 def test_missing_shape(self):
  p,v=self.modules();d=p.produce(3,False);d['extension'].pop()
  with self.assertRaises(ValueError):v.verify_document(d,3,False)
 def test_false_relabeling(self):
  p,v=self.modules();d=p.produce(3,False);x=next(x for x in d['extension'] if x['parents']==[-1,2,0]);x['parents']=[-1,0,1]
  with self.assertRaises(ValueError):v.verify_document(d,3,False)
 def test_extra_duplicate_case(self):
  p,v=self.modules();d=p.produce(3,False);x=next(x for x in d['extension'] if x['cases']);x['cases'].append(copy.deepcopy(x['cases'][0]))
  with self.assertRaises(ValueError):v.verify_document(d,3,False)
 def test_verifier_no_producer_import(self):
  self.modules();t=ast.parse((HERE/'verifier.py').read_text());names=[]
  for n in ast.walk(t):
   if isinstance(n,ast.Import):names.extend(a.name for a in n.names)
   if isinstance(n,ast.ImportFrom):names.append(n.module or '')
  self.assertFalse(any('producer' in n or 'engine' in n or 'importlib' in n for n in names))
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests));e=HERE/'evidence';e.mkdir(exist_ok=True)
 (e/'TESTS.json').write_text(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'rejections':REJECTIONS},indent=2,sort_keys=True)+'\n')
 raise SystemExit(0 if r.wasSuccessful() else 1)
