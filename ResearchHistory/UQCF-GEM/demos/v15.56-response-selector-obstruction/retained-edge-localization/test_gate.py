import importlib.util,pathlib,unittest
import mpmath as mp
import sympy as sp
HERE=pathlib.Path(__file__).resolve().parent
class LocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=None
        if (HERE/'gate.py').exists():
            s=importlib.util.spec_from_file_location('localization1605',HERE/'gate.py');cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)
    def need(self):
        self.assertIsNotNone(self.g,'v16.05 implementation absent: expected RED');return self.g
    def test_excluded_sixth_edge_is_not_a_retained_direction(self):
        g=self.need();v=[mp.zeros(3) for _ in range(6)];v[5][0,0]=2
        self.assertEqual(g.edge_norms(v)['retained'],0)
        self.assertEqual(g.edge_norms(v)['omitted'],2)
        v[0][0,0]=3;self.assertEqual(g.edge_norms(v)['retained'],3)
    def test_exact_binary_coefficients_preserve_a_small_nonzero(self):
        g=self.need();q=sp.Rational(1,2**60);rho=sp.eye(16)/16
        rho+=q*sp.diag(*([1]*8+[-1]*8))
        self.assertEqual(g.exact_coefficients(rho)[(3,0,0,0)],4*q)
    def test_exact_commutator_sign_and_omitted_pair(self):
        g=self.need();a=sp.Symbol('a');d=g.exact_commutator({(0,0,3,0):sp.Integer(1)},'D',a)
        self.assertEqual(d,{(0,0,1,1):a-a**2})
        self.assertEqual(g.exact_commutator({(0,0,3,0):1},'D',sp.Integer(1)),{})
    def test_exact_connected_product_terms_survive(self):
        g=self.need();z={(1,0,0,0):sp.Rational(1,8),(0,1,0,0):sp.Rational(1,16)}
        x={(1,0,0,0):sp.Rational(1,4),(0,1,0,0):sp.Rational(1,2),(1,1,0,0):sp.Rational(3,4)}
        self.assertEqual(g.exact_connected(z,x)[0][0,0],sp.Rational(7,4))
    def test_localization_does_not_turn_unresolved_into_null(self):
        g=self.need()
        self.assertEqual(g.localize(mp.mpf(0),mp.mpf(0)),'RETAINED_EDGE_NULL')
        self.assertEqual(g.localize(mp.mpf('1e-5'),mp.mpf(0)),'READOUT_ANNIHILATION')
        self.assertEqual(g.localize(mp.mpf('1e-20'),mp.mpf(0)),'UNRESOLVED')
        self.assertEqual(g.localize(mp.mpf('1e-5'),mp.mpf('1e-5')),'READOUT_RESPONSE')
        with self.assertRaises(ValueError):g.localize(mp.nan,mp.mpf(0))
    def test_exact_nonzero_polynomial_is_not_a_numerical_null(self):
        g=self.need();a=sp.Symbol('a');v=[sp.zeros(3) for _ in range(6)]
        v[0][0,0]=a*(1-a)/2**80
        self.assertFalse(g.exact_localization(v)['retained_zero'])
        v[0][0,0]=0;v[5][0,0]=a*(1-a)
        self.assertTrue(g.exact_localization(v)['retained_zero'])
        self.assertFalse(g.exact_localization(v)['omitted_zero'])
if __name__=='__main__':unittest.main()
