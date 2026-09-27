import importlib.util
import pathlib
import unittest
import numpy as np

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():raise AssertionError('v15.74 scientific implementation absent: expected RED')
        spec=importlib.util.spec_from_file_location('hamiltonian_gate',path)
        cls.g=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.g)

    def test_three_body_to_one_body_commutator(self):
        g=self.g;op=g.M.F.op
        np.testing.assert_allclose(g.V73.response(op(1,1,1),op(1,1,2)/np.sqrt(8)),op(0,0,3)/np.sqrt(8),atol=1e-15)

    def test_kernel_and_shared_rank_reference(self):
        g=self.g;a=np.diag([2.,1.,0.])
        np.testing.assert_allclose(g.kernel_projector(a,2.),np.diag([0.,0.,1.]),atol=1e-15)
        self.assertEqual(g.rank_sweep(np.eye(3)*1e-14,1.),[0,0,0])

    def test_verdict_preserves_negative_and_invalid(self):
        g=self.g
        self.assertEqual(g.adjudicate(True,True),'HAMILTONIAN_NULL_KERNEL_LOCAL_ONLY_CONFIRMED')
        self.assertEqual(g.adjudicate(True,False),'HAMILTONIAN_INTERACTION_NULL_NOT_EXCLUDED')
        self.assertEqual(g.adjudicate(False,True),'INVALID')

    def test_frozen_coverage_and_validity(self):
        r=self.g.run_measurement()
        self.assertEqual(r['candidate_indices'],[13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['states']),12)
        self.assertEqual(r['source_hidden_pairs'],1701)
        self.assertEqual(r['stack_shape'],[2916,63])
        self.assertTrue(r['all_valid'],r.get('controls'))
        self.assertIn(r['verdict'],['HAMILTONIAN_NULL_KERNEL_LOCAL_ONLY_CONFIRMED','HAMILTONIAN_INTERACTION_NULL_NOT_EXCLUDED'])

if __name__=='__main__':unittest.main()
