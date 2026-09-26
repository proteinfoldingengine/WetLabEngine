"""Behavioural tests for the matched-completion connection bridge."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import unittest
import numpy as np
import pruning_consistency_audit as q

AVAILABLE = importlib.util.find_spec('completion_connection_bridge') is not None
if AVAILABLE:
    import completion_connection_bridge as b

class Availability(unittest.TestCase):
    def test_checker_exists(self):
        self.assertTrue(AVAILABLE, 'Missing completion_connection_bridge implementation')

@unittest.skipUnless(AVAILABLE, 'Implementation not yet present')
class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.plus=b.state(F(1,20),F(1,100)); self.minus=b.state(F(1,20),F(-1,100))
        self.p=b.source()

    def test_pauli_product_phase(self):
        self.assertEqual(b.word_product('XII','YII'),(1,'ZII'))
        self.assertEqual(b.word_product('YII','XII'),(3,'ZII'))
        self.assertEqual(b.word_product('XYZ','XYZ'),(0,'III'))

    def test_state_trace_and_analytic_positivity(self):
        self.assertEqual(self.plus['III'],1)
        self.assertEqual(b.positivity_floor(self.plus),F(37,800))
        self.assertEqual(b.positivity_floor(self.minus),F(37,800))

    def test_all_initial_proper_marginals_match(self):
        for word in b.WORDS:
            if word.count('I'):
                self.assertEqual(b.expect(self.plus,word),b.expect(self.minus,word))
        self.assertNotEqual(self.plus,self.minus)

    def test_source_commutes_but_states_differ(self):
        self.assertEqual(b.commutator(self.plus,self.p),{})
        self.assertEqual(b.commutator(self.minus,self.p),{})
        self.assertGreater(sum(abs(x) for w,x in self.plus.items() if 'I' not in w),0)

    def test_noncommuting_source_rejected(self):
        with self.assertRaises(ValueError): b.tangent(self.plus,{'XII':F(1)})

    def test_pair_connected_data_full_rank_and_raw_polar(self):
        for edge in b.EDGES:
            C=b.connected(self.plus,*edge)
            self.assertEqual(C,q.scale(b.rotation(),F(1,20)))
            R,dR=b.polar_jet(C,q.zeros(3,3))
            self.assertEqual(R,b.rotation()); self.assertEqual(dR,q.zeros(3,3))
            self.assertEqual(b.det3(R),1)

    def test_tangent_includes_centering_and_is_trace_zero(self):
        t=b.tangent(self.plus,self.p)
        self.assertEqual(t['III'],0)
        shifted=b.tangent(self.plus,b.source(F(7,3),F(-2,3)))
        self.assertEqual(shifted,{w:F(7,3)*v for w,v in t.items()})
        biased={'III':F(1),'ZII':F(1,3)}
        self.assertEqual(b.tangent(biased,{'ZII':F(1)})['ZII'],F(8,9))

    def test_exact_connected_correlation_jet(self):
        t=b.tangent(self.plus,self.p)
        expected=[[F(0),F(1,100),F(0)],[-F(1,100),F(0),F(0)],[F(0)]*3]
        for edge in b.EDGES:
            self.assertEqual(b.connected_jet(self.plus,t,*edge),expected)
        self.assertEqual(t['ZII'],F(11,10))

    def test_exact_gauge_invariant_loop_response(self):
        a=b.analyze(self.plus,self.p); z=b.analyze(self.minus,self.p)
        self.assertEqual(a['trace'],F(-109,125));self.assertEqual(z['trace'],a['trace'])
        self.assertEqual(a['trace_jet'],F(-792,3125))
        self.assertEqual(z['trace_jet'],F(792,3125))
        self.assertEqual(a['reference_jet'],F(11,10))
        self.assertEqual(a['scale_free_ratio'],F(-1584,6875))
        self.assertEqual(z['scale_free_ratio'],F(1584,6875))

    def test_scale_identity_shift_and_null(self):
        ref=b.analyze(self.plus,self.p)
        for a in (F(1,5),F(1),F(7,3)):
            for shift in (F(-2,3),F(0),F(4)):
                r=b.analyze(self.plus,b.source(a,shift))
                self.assertEqual(r['scale_free_ratio'],ref['scale_free_ratio'])
                self.assertEqual(r['trace_jet'],a*ref['trace_jet'])
        r=b.analyze(self.plus,{'III':F(3)})
        self.assertEqual(r['trace_jet'],0);self.assertIsNone(r['scale_free_ratio'])

    def test_hidden_zero_and_flat_trace_blind_controls(self):
        r=b.analyze(b.state(F(1,20),F(0)),self.p)
        self.assertEqual(r['trace_jet'],0);self.assertEqual(q.maxabs(r['holonomy_jet']),0)
        r=b.analyze(b.state(F(1,20),F(1,100),F(1),F(0)),self.p)
        self.assertEqual(r['trace_jet'],0)
        self.assertGreater(q.maxabs(r['holonomy_jet']),0)

    def test_parity_fixture_not_a_unique_connection(self):
        rho={'III':F(1),'ZZZ':F(1,5)}
        for edge in b.EDGES:
            C=b.connected(rho,*edge);self.assertEqual(q.rank(C),0)
            with self.assertRaises(ValueError): b.polar_jet(C,q.zeros(3,3))
        rho=b.finite_tilt(rho,F(1,4),collective=False)
        self.assertEqual(q.rank(b.connected(rho,0,1)),1)

    def test_local_frame_covariance_exact(self):
        Rs=(b.rotation(),[[1,0,0],[0,F(3,5),F(4,5)],[0,F(-4,5),F(3,5)]],
            [[F(5,13),0,F(12,13)],[0,1,0],[F(-12,13),0,F(5,13)]])
        t=b.tangent(self.plus,self.p); os=[];ds=[]
        for i,j in b.EDGES:
            C=b.connected(self.plus,i,j); E=b.connected_jet(self.plus,t,i,j)
            O,D=b.polar_jet(C,E)
            Cg=q.mul(q.mul(Rs[i],C),b.transpose(Rs[j]))
            Eg=q.mul(q.mul(Rs[i],E),b.transpose(Rs[j]))
            Og,Dg=b.polar_jet(Cg,Eg)
            self.assertEqual(Og,q.mul(q.mul(Rs[i],O),b.transpose(Rs[j])))
            self.assertEqual(Dg,q.mul(q.mul(Rs[i],D),b.transpose(Rs[j])))
            os.append(Og);ds.append(Dg)
        H,dH=b.loop_jet(os,ds)
        r=b.analyze(self.plus,self.p)
        self.assertEqual(b.trace(H),r['trace']);self.assertEqual(b.trace(dH),r['trace_jet'])

    def test_parameter_family_not_hardcoded(self):
        for c in (F(1,40),F(1,30),F(1,20)):
            for h in (F(-1,100),F(0),F(1,100)):
                for x,y in ((F(3,5),F(4,5)),(F(5,13),F(12,13))):
                    r=b.analyze(b.state(c,h,x,y),self.p)
                    self.assertEqual(r['trace_jet'],-6*(3*y-4*y**3)*h*x/c)

    def test_dense_pauli_oracle_and_spectral_safety(self):
        rho=b.dense(self.plus);P=b.dense(self.p,normalized=False)
        self.assertLess(np.linalg.norm(rho@P-P@rho),1e-14)
        self.assertGreaterEqual(float(np.linalg.eigvalsh(rho).min()),float(F(37,800))-1e-14)
        self.assertAlmostEqual(np.trace(rho).real,1)
        tangent=rho@P-rho*np.trace(rho@P)
        for w in b.WORDS:
            expected=np.trace(tangent@b.dense_word(w)).real
            self.assertAlmostEqual(expected,float(b.tangent(self.plus,self.p)[w]),13)

    def test_independent_dense_exponential_svd_derivative(self):
        r=b.numeric_oracle(self.plus,self.p)
        self.assertLess(r['max_jet_error'],2e-7)
        self.assertGreater(r['min_edge_singular_value'],0.04)
        self.assertGreater(r['min_state_eigenvalue'],0.04)
        self.assertEqual(r['determinant_flip_count'],0)

    def test_exact_finite_source_changes_and_metric_matching(self):
        for t in (F(-1,10),F(0),F(1,10)):
            rp=b.finite_tilt(self.plus,t);rm=b.finite_tilt(self.minus,t)
            self.assertEqual(rp['III'],1);self.assertEqual(rm['III'],1)
            for site in range(3):
                for axis in 'XYZ':
                    w=b.word({site:axis})
                    self.assertEqual(rp[w],rm[w])
            if t:
                self.assertNotEqual(b.connected(rp,0,1),b.connected(rm,0,1))

    def test_invalid_parameters_and_polar_stratum_fail_closed(self):
        for args in ((F(0),F(1,100)),(F(1),F(1)),(F(1,20),F(1,100),F(1),F(1))):
            with self.assertRaises(ValueError):b.state(*args)
        with self.assertRaises(ValueError):b.polar_jet([[1,0,0],[0,2,0],[0,0,1]],q.eye(3))
        with self.assertRaises(ValueError):b.word_product('ABI','III')

    def test_saved_exact_results_are_recomputed(self):
        p=Path(__file__).with_name('COMPLETION_CONNECTION_RESULTS.json')
        self.assertTrue(p.exists())
        self.assertEqual(json.loads(p.read_text()),b.run())

if __name__=='__main__':unittest.main()
