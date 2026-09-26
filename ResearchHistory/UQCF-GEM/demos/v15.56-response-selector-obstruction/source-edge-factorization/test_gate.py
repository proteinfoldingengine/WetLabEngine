"""Fail-closed tests. Synthetic manifest tests check structure, not physics."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np
try:
    import gate as g
except ModuleNotFoundError as exc:
    if exc.name != 'gate':
        raise
    g = None

FIXTURES = [(0.1,0.08,0.04),(0.1,0.08,0.08),(0.1,0.08,0.12),
            (0.1,0.12,0.04),(0.1,0.12,0.08),(0.1,0.16,0.04),
            (0.15,0.12,0.04),(0.15,0.12,0.08),(0.15,0.16,0.04),
            (0.2,0.12,0.04),(0.2,0.16,0.04)]

class RankAndManifestTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(g, 'RED: source-edge gate implementation is absent')

    def manifest(self):
        return dict(schema=1,fixture_count=11,input_dimension=243,
                    fitted_parameters=0,controls_pass=True,provenance=g.provenance(),
                    rows=[dict(fixture=list(p),artifact=f'fixture_{i:02d}.npz',
                               sha256='0'*64,controls_pass=True)
                          for i,p in enumerate(FIXTURES)])

    def test_exact_frozen_fixture_order(self):
        self.assertEqual(list(g.FIXTURES), FIXTURES)

    def test_roundoff_residual_uses_parent_scale(self):
        noise=np.diag([1e-16,5e-17,2e-17])
        self.assertEqual(g.rank_info(noise,reference_scale=1.)['rank'],0)
        self.assertGreater(g.rank_info(noise)['rank'],0)

    def test_real_residual_is_not_erased(self):
        self.assertEqual(g.rank_info(np.diag([1e-6,1e-16,0]),reference_scale=1.)['rank'],1)

    def test_nonfinite_matrix_rejected(self):
        for x in (np.nan,np.inf,-np.inf):
            with self.assertRaises(ValueError):
                g.rank_info(np.array([[x]]))

    def test_invalid_parent_scale_rejected(self):
        for x in (-1.,np.nan,np.inf):
            with self.assertRaises(ValueError):
                g.rank_info(np.eye(3),reference_scale=x)

    def test_manifest_structure_accepts_complete_synthetic_record(self):
        self.assertEqual(g.validate_manifest(self.manifest()),[])

    def test_false_controls_rejected(self):
        r=self.manifest();r['controls_pass']=False
        self.assertTrue(g.validate_manifest(r))
        r=self.manifest();r['rows'][0]['controls_pass']=False
        self.assertTrue(g.validate_manifest(r))

    def test_invalid_verdict_rejected_even_with_true_flag(self):
        r=self.manifest();r['verdict']='INVALID'
        self.assertTrue(g.validate_manifest(r))

    def test_missing_fixture_rejected(self):
        r=self.manifest();r['rows'].pop()
        self.assertTrue(g.validate_manifest(r))

    def test_duplicate_fixture_rejected(self):
        r=self.manifest();r['rows'][1]['fixture']=r['rows'][0]['fixture']
        self.assertTrue(g.validate_manifest(r))

    def test_wrong_column_declaration_rejected(self):
        r=self.manifest();r['input_dimension']=242
        self.assertTrue(g.validate_manifest(r))

    def test_nonfinite_manifest_rejected(self):
        r=self.manifest();r['unexpected_diagnostic']=float('nan')
        self.assertTrue(g.validate_manifest(r))

    def test_provenance_change_rejected(self):
        r=self.manifest();r['provenance']['source_blobs']['response_quotient_rank.py']='0'*40
        self.assertTrue(g.validate_manifest(r))

    def test_cli_invalid_and_optimized_python_fail(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'report.json').write_text(json.dumps({'controls_pass':False}))
            for flags in ([],['-O']):
                p=subprocess.run([sys.executable,*flags,str(Path(g.__file__)),
                                  '--verify',td],capture_output=True,text=True)
                self.assertNotEqual(p.returncode,0,p.stdout+p.stderr)

    def test_cli_pipeline_does_not_hide_failure(self):
        import shlex
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'report.json').write_text('{}')
            cmd='set -o pipefail; '+ ' '.join(map(shlex.quote,[sys.executable,
                str(Path(g.__file__)),'--verify',td]))+' | cat'
            p=subprocess.run(['bash','-c',cmd],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)

class MeasuredFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arrays=None if g is None else g.measure_fixture(FIXTURES[0])

    def setUp(self):
        self.assertIsNotNone(g, 'RED: source-edge gate implementation is absent')

    def test_actual_fixture_factorization_and_fd_controls(self):
        metrics,errors=g.evaluate_arrays(self.arrays,FIXTURES[0])
        self.assertEqual(errors,[])
        self.assertEqual(self.arrays['E'].shape,(9,243))
        self.assertEqual(self.arrays['L'].shape,(3,9))
        self.assertEqual(self.arrays['K'].shape,(9,243))
        self.assertTrue(metrics['controls_pass'])

    def test_missing_raw_column_rejected(self):
        a=dict(self.arrays);a['E']=a['E'][:,:-1]
        self.assertTrue(g.evaluate_arrays(a,FIXTURES[0])[1])

    def test_nonfinite_raw_value_rejected(self):
        a=copy.deepcopy(self.arrays);a['K'][0,0]=np.nan
        self.assertTrue(g.evaluate_arrays(a,FIXTURES[0])[1])

    def test_modified_edge_map_rejected(self):
        a=copy.deepcopy(self.arrays);a['E'][0,0]+=.01
        self.assertTrue(g.evaluate_arrays(a,FIXTURES[0])[1])

    def test_export_reread_and_corruption(self):
        with tempfile.TemporaryDirectory() as td:
            row=g.save_fixture(Path(td),0,FIXTURES[0],self.arrays)
            arrays=g.load_fixture(Path(td),row)
            np.testing.assert_array_equal(arrays['E'],self.arrays['E'])
            p=Path(td)/row['artifact'];p.write_bytes(p.read_bytes()+b'corruption')
            with self.assertRaises(ValueError):
                g.load_fixture(Path(td),row)

if __name__=='__main__':
    unittest.main()
