import importlib.util
from pathlib import Path
import tempfile
import unittest
import retained_motion as m
r=None
if importlib.util.find_spec('replay'):
    import replay as r

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'retained-motion presentation missing')
    def test_computed_frames_distinguish_pruned_and_unpruned_routes(self):
        data=r.payload()
        self.assertEqual(len(data['frames']),65)
        mid=data['frames'][32]
        self.assertAlmostEqual(mid['unpruned_retained_distance'],1,places=10)
        self.assertLess(mid['actually_pruned_distance'],1e-11)
        self.assertLess(mid['transported_distance'],1e-11)
    def test_finite_swap_not_continuous_closure(self):
        data=r.payload()
        self.assertEqual(data['frames'][0]['status'],'CLOSED_FIXED_RECORDS')
        self.assertEqual(data['frames'][-1]['status'],'CLOSED_RECORD_PERMUTATION')
        self.assertEqual(data['frames'][32]['status'],'NOT_CLOSED_ON_FIXED_ALGEBRA')
    def test_offline_explicit_template(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'demo.html';r.write_html(r.payload(),p);text=p.read_text()
            for s in ['Playback is not physical time','actually pruned','transported algebra','No actual record selected']:
                self.assertIn(s,text)
            self.assertNotIn('<script src=',text);self.assertNotIn('fetch(',text)
    def test_all_panel_cases_exported(self):
        data=r.payload()
        self.assertEqual(len(data['audit']['cases']),96)
        self.assertEqual(len({(c['motion'],c['mask']) for c in data['audit']['cases']}),96)
    def test_fps_guard(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_no_dynamic_or_clock_replacement(self):
        data=r.payload()
        self.assertIsNone(data['audit']['physical_duration'])
        self.assertFalse(data['audit']['new_physical_motion_law_derived'])
        self.assertIn('counterfactual',data['notice'])

if __name__=='__main__':unittest.main(verbosity=2)
