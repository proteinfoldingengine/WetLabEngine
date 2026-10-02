import copy
import unittest
from test_bootstrap import fixture
import verifier as v

class VerifierGate(unittest.TestCase):
    def test_complete_control(self):
        self.assertEqual(v.verify(fixture())['status'],'VERIFIED')
    def test_omission_rejected(self):
        d=fixture();d['records']=[]
        with self.assertRaises(ValueError):v.verify(d)
    def test_duplicate_rejected(self):
        d=fixture();d['records']*=2
        with self.assertRaises(ValueError):v.verify(d)
    def test_substitution_rejected(self):
        d=fixture();d['records'][0]['identity']=['CONTROL','other']
        with self.assertRaises(ValueError):v.verify(d)
    def test_wrong_profile_rejected(self):
        d=fixture();d['records'][0]['q']=[2]
        with self.assertRaises(ValueError):v.verify(d)
    def test_wrong_start_rejected(self):
        d=fixture();d['records'][0]['start']=[9,7,17]
        with self.assertRaises(ValueError):v.verify(d)
    def test_stacked_defect_rejected(self):
        # Binary root and two binary children; simultaneous sibling defects.
        t=(((),()),((),()));raw=[127,1]
        self.assertEqual(v.profile_check(t,2,raw),[1,1,1])
        with self.assertRaisesRegex(v.InterfaceNotPreserved,'total excursion'):
            v.path_check(t,2,[1,2,2],[raw],raw,raw)

if __name__=='__main__':unittest.main(verbosity=2)
