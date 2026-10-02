import unittest
import copy
import os,json,gzip
from pathlib import Path
from unittest.mock import patch
import producer as p
import verifier as v

class Campaign(unittest.TestCase):
    document=None
    def retain(self,name,doc):
        folder=Path(os.environ.get('V1653_TEST_OUTPUT','out/v1653-test-attempts'));folder.mkdir(parents=True,exist_ok=True)
        (folder/(name+'.json.gz')).write_bytes(gzip.compress((json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    def campaign(self):
        self.assertTrue(callable(getattr(p,'produce',None)),'CAMPAIGN_IMPLEMENTATION_MISSING')
        if type(self).document is None:
            type(self).document=p.produce();self.retain('campaign',type(self).document)
        return copy.deepcopy(type(self).document)
    def test_complete_frozen_campaign(self):
        d=self.campaign();result=v.verify(d)
        self.assertEqual(result['status'],'VERIFIED')
        self.assertEqual([r['identity'] for r in d['records']],v.expected_specs())
        self.assertEqual(len(d['records']),len(v.expected_specs()))
    def test_campaign_omission_rejected(self):
        d=self.campaign();d['records'].pop()
        with self.assertRaisesRegex(ValueError,'coverage'):v.verify(d)
    def test_infeasible_not_construction_failure(self):
        d=self.campaign();result=v.verify(d)
        r=next(r for r in d['records'] if r['identity']==['F',[1,1,1,1],4,1])
        self.assertEqual(r,{'identity':['F',[1,1,1,1],4,1],'status':'ok','feasible':False})
        self.assertEqual(result['status'],'VERIFIED')
    def unsafe(self,name):
        d=self.campaign();result=v.verify(d)
        row=next(r for r in d['records'] if r['identity']==['M',name])
        self.assertEqual(next(r for r in result['results'] if r['identity']==['M',name])['outcome'],'native_but_not_unit')
        for state in row['path']:self.assertTrue(v.profile_check(row['tree'],row['k'],state))
        with self.assertRaisesRegex(v.InterfaceNotPreserved,'total excursion exceeds one'):
            v.path_check(row['tree'],row['k'],row['q'],row['path'],row['start'],row['end'])
        row['expected_outcome']='unit_path'
        with self.assertRaises(ValueError):v.verify(d)
    def test_native_unsafe_q2_rejected_as_unit(self):self.unsafe('unsafe_q2')
    def test_native_unsafe_q3_rejected_as_unit(self):self.unsafe('unsafe_q3')
    def test_resource_failure_incomplete(self):
        self.campaign()
        with patch.object(p,'normalize',side_effect=MemoryError('INJECTED_RESOURCE_EXHAUSTION')):d=p.produce()
        self.retain('resource_failure',d)
        self.assertEqual([r['identity'] for r in d['records']],v.expected_specs())
        failures=[r for r in d['records'] if r['status']!='ok']
        self.assertTrue(failures)
        self.assertTrue(all(r['category']=='incomplete' and r['exception_type']=='MemoryError' for r in failures))
        with self.assertRaises(ValueError) as caught:v.verify(d)
        self.assertNotIsInstance(caught.exception,v.InterfaceNotPreserved)
    def test_construction_failure_scoped(self):
        self.campaign()
        with patch.object(p,'normalize',side_effect=ValueError('INJECTED_CONSTRUCTION_FAILURE')):d=p.produce()
        self.retain('construction_failure',d)
        self.assertEqual([r['identity'] for r in d['records']],v.expected_specs())
        with self.assertRaises(v.InterfaceNotPreserved):v.verify(d)

if __name__=='__main__':unittest.main(verbosity=2)
