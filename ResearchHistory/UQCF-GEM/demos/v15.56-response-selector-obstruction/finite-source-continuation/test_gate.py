import importlib.util
import pathlib
import unittest
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=None
        if (HERE/'gate.py').exists():
            spec=importlib.util.spec_from_file_location('finite1603_test',HERE/'gate.py')
            cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)
    def need(self):
        self.assertIsNotNone(self.g,'v16.03 implementation absent: expected RED')
        return self.g
    def test_shared_edge_mixed_derivative(self):
        g=self.need()
        with mp.workdps(50):
            cs=[mp.eye(3) for _ in range(5)]; a=g.R.skew_basis()[0]
            v=[a]+[mp.zeros(3) for _ in range(4)]
            j,t,res=g.response(cs,cs,[v],'isotropic',v)
            self.assertLess(g.norm(t-mp.matrix([[-2],[-2],[-8]])),mp.mpf('1e-35'))
            self.assertLess(res,mp.mpf('1e-35'))
    def test_first_derivative_and_mixed_symmetry(self):
        g=self.need()
        with mp.workdps(50):
            for arm,c in [('isotropic',mp.diag([3,2,1])),('plane',mp.diag([3,2,0]))]:
                cs=[c.copy() for _ in range(5)];a=g.R.skew_basis()[2]
                b=[a*c]+[mp.zeros(3) for _ in range(4)];v=[c]+[mp.zeros(3) for _ in range(4)]
                j,t,res=g.response(cs,cs,[b],arm,v)
                _,_,old=g.E.readout({'cs':cs,'sc':cs,'ds':[b]},arm)
                self.assertLess(g.norm(j-old),mp.mpf('1e-35'))
                _,rev,_=g.response(cs,cs,[v],arm,b)
                self.assertLess(g.norm(t-rev),mp.mpf('1e-35'))
    def test_undefined_domains_rejected(self):
        g=self.need()
        with mp.workdps(50):
            for arm,c in [('plane',mp.diag([1,0,0])),('isotropic',mp.diag([3,2,-1]))]:
                with self.assertRaises(ValueError):g.response([c]*5,[c]*5,[[mp.zeros(3)]*5],arm)
    def test_scientific_no_and_invalid_override(self):
        g=self.need()
        self.assertEqual(g.adjudicate(False,['active'],True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,['null'],False),('DISJOINT_CUBIC_NUMERICAL_NULL','FINITE_GRID_OVERLAP_RESPONSE_NOT_CONFIRMED'))
        self.assertEqual(g.adjudicate(True,['unresolved'],True)[0],'DISJOINT_CUBIC_UNRESOLVED')
    def test_classification_agreement_and_domain_mismatch(self):
        g=self.need()
        with mp.workdps(50):
            zero=mp.zeros(3,1);near=mp.matrix([['2e-35'],[0],[0]])
            self.assertFalse(g.agreement([zero,zero],[near,near],classification=True)[0])
            self.assertFalse(g.agreement([zero,zero],[None,None])[0])
            self.assertFalse(g.agreement([None,zero],[None,None])[0])
    def test_nonfinite_is_not_a_domain_exit(self):
        g=self.need()
        with mp.workdps(50):
            cs=[mp.eye(3) for _ in range(5)];cs[0][0,0]=mp.nan
            try:g.response(cs,[mp.eye(3)]*5,[[mp.zeros(3)]*5],'isotropic')
            except g.DomainError:self.fail('nonfinite arithmetic was a domain exit')
            except ValueError:pass
            else:self.fail('nonfinite input was accepted')
    def test_fail_closed_classification(self):
        g=self.need()
        with mp.workdps(50):
            self.assertEqual(g.classify(mp.zeros(3,81)),'null')
            self.assertEqual(g.classify(mp.matrix([[1,0],[0,0],[0,0]])),'active')
            with self.assertRaises(ValueError):g.classify(mp.matrix([[mp.nan],[0],[0]]))

if __name__=='__main__':unittest.main()
