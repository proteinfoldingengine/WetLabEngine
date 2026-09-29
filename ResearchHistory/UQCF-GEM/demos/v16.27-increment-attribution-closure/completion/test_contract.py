"""One strict witness contract, run first against historical verify, then the replacement."""
import copy
import importlib
import json
import os
from pathlib import Path
import sys
import unittest
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE))
REJECTIONS=[]

def witness():
    start=[[0,1],[0,2],[0,1,2]]
    final=[[0,1],[0,2],[0]]
    def path(first,second):
        mid=[[0,1],[0,2],[0,second]]
        rows=[]
        for before,after,leaf,h0,h1,trig in [(start,mid,first,1,2,True),(mid,final,second,2,2,False)]:
            rows.append({'version':'16.26','genesis':'v16.26-common-genesis','parents':[-1,0,0],
                         'before':copy.deepcopy(before),'after':copy.deepcopy(after),'index':2,'leaf':leaf,
                         'parent':0,'tau_before':h0,'tau_after':h1,'h_before':h0,'h_after':h1,
                         'delta_h':h1-h0,'trigger':trig})
        return rows
    return {'version':'16.27','parents':[-1,0,0],'before':start,'after':final,
            'path_a':path(1,2),'path_b':path(2,1),'changed_events':[[2,1],[2,2]]}

class Contract(unittest.TestCase):
    def module(self):
        return importlib.import_module(os.environ.get('V27_VERIFIER','verifier'))
    def reject(self,name,mutate):
        data=witness();mutate(data)
        with self.assertRaises(ValueError) as cm:self.module().verify_witness(data)
        REJECTIONS.append({'defect':name,'reason':str(cm.exception)})
    def test_valid_admissible_witness(self):self.module().verify_witness(witness())
    def test_false_stored_after(self):self.reject('false-after',lambda d:d['path_a'][0].__setitem__('after',[[0]]))
    def test_missing_stored_after(self):self.reject('missing-after',lambda d:d['path_a'][0].pop('after'))
    def test_foreign_step_carrier(self):self.reject('foreign-step-carrier',lambda d:d['path_a'][0].__setitem__('parents',[-1,0,1]))
    def test_foreign_step_origin(self):self.reject('foreign-step-origin',lambda d:d['path_a'][0].__setitem__('genesis','foreign'))
    def test_false_h_before(self):self.reject('false-h-before',lambda d:d['path_a'][0].__setitem__('h_before',9))
    def test_false_local_trigger(self):self.reject('false-local-trigger',lambda d:d['path_a'][0].__setitem__('trigger',False))
    def test_boolean_delta_is_not_integer(self):self.reject('boolean-delta',lambda d:d['path_a'][0].__setitem__('delta_h',True))
    def test_actual_endpoint_mismatch(self):self.reject('endpoint-mismatch',lambda d:d['after'].__setitem__(1,[0]))
    def test_false_delta(self):self.reject('false-delta',lambda d:d['path_a'][0].__setitem__('delta_h',9))
    def test_reordered_valid_witness(self):
        d=witness();d['path_a'],d['path_b']=d['path_b'],d['path_a'];self.module().verify_witness(d)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contract))
    out=Path(os.environ.get('V27_EVIDENCE',str(HERE/'evidence')));out.mkdir(parents=True,exist_ok=True)
    (out/'CONTRACT_TESTS.json').write_text(json.dumps({'target':os.environ.get('V27_VERIFIER','verifier'),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'rejections':REJECTIONS},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
