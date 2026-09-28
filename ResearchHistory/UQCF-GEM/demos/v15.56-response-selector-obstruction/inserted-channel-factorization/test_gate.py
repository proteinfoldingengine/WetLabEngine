import hashlib
import importlib.util
import pathlib
import tempfile
import unittest
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent

class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=None
        if (HERE/'gate.py').exists():
            s=importlib.util.spec_from_file_location('factor1604_test',HERE/'gate.py')
            cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)
    def need(self):
        self.assertIsNotNone(self.g,'v16.04 implementation absent: expected RED')
        return self.g
    def test_commutator_sign_and_weight_preserving_null(self):
        g=self.need()
        with mp.workdps(50):
            entries=[(0,1,mp.mpf(3)),(1,0,mp.mpf(5)),(1,1,mp.mpf(7))]
            x=mp.matrix([2,4]);weights=[1,2]
            y,blocks=g.weight_action(entries,x,mp.mpf('0.5'),weights)
            self.assertEqual(list(y),[-3,mp.mpf('2.5')])
            self.assertEqual(g.weight_action(entries,x,mp.mpf(1),weights)[0],mp.zeros(2,1))
            self.assertEqual(g.weight_action([(1,1,mp.mpf(7))],x,mp.mpf('.5'),weights)[0],mp.zeros(2,1))
    def test_lift_respects_site_order_and_spectator(self):
        g=self.need();t=mp.zeros(16);t[4,1]=2
        entries=g.lift(t,(2,0))
        x=mp.zeros(256,1);x[g.G.INDEX[(1,2,0,3)]]=3
        expected=mp.zeros(256,1);expected[g.G.INDEX[(0,2,1,3)]]=6
        self.assertEqual(g.apply_entries(entries,x),expected)
    def test_connected_derivative_includes_both_products(self):
        g=self.need();z=mp.zeros(256,1);x=z.copy()
        z[g.G.INDEX[(1,0,0,0)]]=mp.mpf(1)/8
        z[g.G.INDEX[(0,1,0,0)]]=mp.mpf(1)/16
        x[g.G.INDEX[(1,0,0,0)]]=mp.mpf(1)/4
        x[g.G.INDEX[(0,1,0,0)]]=mp.mpf(1)/2
        x[g.G.INDEX[(1,1,0,0)]]=mp.mpf(3)/4
        edge=g.G.V96.EDGES.index((0,1))
        self.assertEqual(g.connected(z,x)[edge][0,0],mp.mpf(7)/4)
    def test_provenance_rejects_modified_and_missing_file(self):
        g=self.need()
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);(p/'a').write_bytes(b'original')
            m={'a':hashlib.sha256(b'original').hexdigest()}
            self.assertTrue(g.verify_files(p,m))
            (p/'a').write_bytes(b'changed');self.assertFalse(g.verify_files(p,m))
            (p/'a').unlink();self.assertFalse(g.verify_files(p,m))
    def test_domain_and_nonfinite_fail_closed(self):
        g=self.need()
        for c in [mp.diag([1,0,0]),mp.matrix([[mp.nan,0,0],[0,1,0],[0,0,1]])]:
            with self.assertRaises(ValueError):g.contract([c]*5,[c]*5,[[mp.eye(3)]*5],[mp.eye(3)]*5,'isotropic')
        self.assertEqual(g.verdict(False,True),'INVALID')
        self.assertEqual(g.verdict(True,False),'FACTORIZATION_NOT_CONFIRMED')
    def test_affine_readout_common_tangent_null(self):
        g=self.need()
        cs=[mp.eye(3)]*5;b=[[mp.eye(3)]*5]
        self.assertEqual(g.affine_contrast(cs,cs,b,b,'isotropic'),mp.zeros(3,1))
        skew=g.F.R.skew_basis()[0];cs=[mp.eye(3)+skew]+[mp.eye(3)]*4
        b=[[skew]+[mp.zeros(3)]*4]
        self.assertGreater(g.F.norm(g.affine_contrast(cs,cs,b,[[mp.zeros(3)]*5],'isotropic')),0)

if __name__=='__main__':unittest.main()
