"""Completion acceptance tests; frozen before the new producer and verifier."""
import ast
import copy
import importlib
import json
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
REJECTIONS=[]

class Complete(unittest.TestCase):
    def modules(self):
        self.assertTrue((HERE/'producer.py').is_file(),'completion producer absent')
        self.assertTrue((HERE/'verifier.py').is_file(),'independent verifier absent')
        return importlib.import_module('producer'),importlib.import_module('verifier')
    def case(self):
        p,v=self.modules();return p.certify([-1,0,0],[[0,1],[0,2],[0,1,2]],[[0,1],[0,2],[0]])
    def reject(self,name,change):
        d=self.case();change(d);_,v=self.modules()
        with self.assertRaises(ValueError) as cm:v.verify_case(d)
        REJECTIONS.append({'defect':name,'reason':str(cm.exception)})
    def test_valid_dependent_case(self):
        _,v=self.modules();r=v.verify_case(self.case());self.assertEqual(r['path_count'],2);self.assertTrue(r['dependent'])
    def test_identity_and_unique_path_controls(self):
        p,v=self.modules()
        for a,b in [([[0]],[[0]]),([[0,1],[0,1]],[[0],[0,1]])]:
            raw=[-1] if len(a[0])==1 else [-1,0]
            r=v.verify_case(p.certify(raw,a,b));self.assertFalse(r['dependent']);self.assertEqual(r['path_count'],1)
    def test_reordered_path_records_accepted(self):
        _,v=self.modules();d=self.case();d['paths'].reverse();v.verify_case(d)
    def test_missing_path(self):self.reject('missing-path',lambda d:d['paths'].pop())
    def test_duplicate_path(self):self.reject('duplicate-path',lambda d:d['paths'].append(copy.deepcopy(d['paths'][0])))
    def test_false_delta(self):self.reject('false-path-delta',lambda d:d['paths'][0]['deltas'].__setitem__(0,9))
    def test_boolean_delta(self):self.reject('boolean-path-delta',lambda d:d['paths'][0]['deltas'].__setitem__(0,True))
    def test_false_profile(self):self.reject('false-profile',lambda d:d['paths'][0]['profiles'][0].__setitem__(0,9))
    def test_false_trigger(self):self.reject('false-trigger',lambda d:d['paths'][0]['triggers'].__setitem__(0,False))
    def test_missing_event(self):self.reject('missing-event',lambda d:d['paths'][0]['events'].pop())
    def test_false_verdict(self):self.reject('false-attribution',lambda d:d.__setitem__('dependent',False))
    def test_foreign_origin(self):self.reject('foreign-origin',lambda d:d.__setitem__('genesis','foreign'))
    def test_nonprefix_endpoint(self):
        p,v=self.modules()
        with self.assertRaises(ValueError):p.certify([-1,0,1],[[0,1,2],[0,1,2]],[[0,2],[0,1,2]])
    def test_changed_union(self):
        p,v=self.modules()
        with self.assertRaises(ValueError):p.certify([-1,0,0],[[0,1,2]],[[0,1]])
    def test_invalid_parents(self):
        p,v=self.modules()
        for raw in [[],[-1,True],[-1,0.0],[-1,2,1],[-1,2,99],[-1,-1]]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):p.certify(raw,[[0]],[[0]])
                with self.assertRaises(ValueError):v.validate(raw,[[0]],[[0]])
    def test_ancestor_cannot_precede_descendant(self):
        p,v=self.modules();d=p.certify([-1,0,1],[[0,1,2],[0,1,2]],[[0],[0,1,2]])
        d['paths'][0]['events'].reverse()
        with self.assertRaises(ValueError):v.verify_case(d)
    def test_nonpermutation_event_identity(self):self.reject('wrong-view-identity',lambda d:d['paths'][0]['events'][0].__setitem__(0,0))
    def test_small_complete_universe(self):
        p,v=self.modules();d=p.produce(3);r=v.verify_document(d,3);self.assertGreater(r['original']['endpoints'],0)
    def test_missing_endpoint(self):
        p,v=self.modules();d=p.produce(3);next(x for x in d['instances'] if x['cases'])['cases'].pop()
        with self.assertRaises(ValueError):v.verify_document(d,3)
    def test_missing_shape(self):
        p,v=self.modules();d=p.produce(3);d['instances']=d['instances'][2:]
        with self.assertRaises(ValueError):v.verify_document(d,3)
    def test_false_metamorphic_copy(self):
        p,v=self.modules();d=p.produce(3);a=next(x for x in d['instances'] if x['variant']=='original' and x['parents']==[-1,0,1]);b=next(x for x in d['instances'] if x['variant']=='relabeled' and x['code']==a['code']);b['parents']=a['parents'][:]
        with self.assertRaises(ValueError):v.verify_document(d,3)
    def test_relabeling_and_storage(self):
        p,v=self.modules();d=p.produce(3);v.verify_document(d,3)
    def test_independent_module_has_no_producer_import(self):
        _,v=self.modules();text=(HERE/'verifier.py').read_text();nodes=ast.walk(ast.parse(text))
        for node in nodes:
            if isinstance(node,ast.Import):self.assertTrue(all(x.name not in ('producer','engine','importlib') for x in node.names))
            if isinstance(node,ast.ImportFrom):self.assertNotIn(node.module,('producer','engine','importlib'))
        self.assertNotIn('prod.produce',text)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Complete))
    out=HERE/'evidence';out.mkdir(exist_ok=True)
    (out/'COMPLETE_TESTS.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'rejections':REJECTIONS},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
