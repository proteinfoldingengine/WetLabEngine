import importlib.util
import pathlib
import unittest

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).with_name('gate.py')
        assert p.exists(), 'v16.02 implementation absent: expected RED'
        s=importlib.util.spec_from_file_location('v1602_test',p)
        cls.g=importlib.util.module_from_spec(s);s.loader.exec_module(cls.g)

    def test_full_rank_solver_and_improper_rejection(self):
        g=self.g
        with g.mp.workdps(50):
            c=g.mp.diag([3,2,1]);r,p,lin,_,_=g.edge(c,c,'isotropic')
            b=g.mp.matrix([[0,-1,0],[1,0,0],[0,0,0]])
            w,err=g.R.solve_skew(r,p,lin,b*c)
            self.assertLess(g.norm(w-b),g.mp.mpf('1e-35'))
            self.assertLess(err,g.mp.mpf('1e-35'))
            with self.assertRaises(ValueError):g.edge(g.mp.diag([3,2,-1]),c,'isotropic')
            with self.assertRaises(ValueError):g.edge(g.mp.diag([3,0,0]),c,'plane')

    def test_readout_and_finite_tensor_layout(self):
        g=self.g
        with g.mp.workdps(50):
            c=g.mp.diag([3,2,1]);zero=g.mp.zeros(3)
            inp={'cs':[c]*6,'sc':[c]*6,'ds':[[zero]*6]}
            rr,k,j=g.readout(inp,'isotropic')
            self.assertEqual(rr['K_ranks'],[0,0,0])
            self.assertEqual(rr['J_ranks'],[0,0,0])
            probe={'dc':g.np.zeros((1,6,3,3)),'dh':None,'J':None,'domain':False}
            self.assertEqual(g.finite_errors(probe,inp,None)['finite_channel_error'],0.)

    def test_isotropic_channel(self):
        g=self.g
        with g.mp.workdps(50):
            law=g.laws(50)
            self.assertTrue(law['isotropic_controls']['valid'])
            want=g.mp.diag([1,g.mp.mpf(1)/3,g.mp.mpf(1)/3,g.mp.mpf(1)/3])
            for frame in [0,1]:
                for t in law['preparation']['isotropic'][frame]:
                    self.assertLess(g.norm(t-want),g.mp.mpf('1e-35'))

    def test_verdict_override_and_scientific_no(self):
        g=self.g
        self.assertEqual(g.adjudicate(False,True,True),('INVALID','INVALID'))
        self.assertEqual(g.adjudicate(True,False,False),('FULL_ENSEMBLE_EB_RESPONSE_SCALING_NOT_CONFIRMED','FULL_ENSEMBLE_ERASURE_NOT_CONFIRMED'))

    def test_complete_measurement(self):
        g=self.g;r=g.run_measurement()
        self.assertTrue(r['all_valid'],r['controls'])
        self.assertEqual(len(r['rows']),192)
        self.assertEqual(sum(x['a']>0 for x in r['rows']),144)
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        for row in r['rows']:
            self.assertEqual(set(row['precision_results']),{'50','80'})
            if row['a']==0:
                for pr in row['precision_results'].values():
                    self.assertIsNone(pr['responses'])
                    self.assertEqual(pr['polar_readout'],'undefined')
        self.assertEqual(r['precision_digits'],[50,80])
        # Tests accept both valid scientific outcomes; validity is mandatory.
        self.assertIn(r['verdict'],['FULL_ENSEMBLE_EB_RESPONSE_SCALING_CONFIRMED','FULL_ENSEMBLE_EB_RESPONSE_SCALING_NOT_CONFIRMED'])

if __name__=='__main__':unittest.main()
