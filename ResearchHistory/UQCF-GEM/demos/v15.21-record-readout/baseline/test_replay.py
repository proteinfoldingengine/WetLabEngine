import importlib.util
from pathlib import Path
import tempfile
import unittest
import physical_predictor as m
r=None
if importlib.util.find_spec('replay'):
    import replay as r

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'channel/readout replay implementation missing')
    def test_all_grid_points_include_validity(self):
        p=r.payload();self.assertEqual(len(p['grid']),441)
        for row in p['grid']:
            self.assertEqual(row['cptp'],row['lambda']<=(1+row['t'])/2+1e-12)
    def test_raw_projection_is_not_shown_as_a_channel(self):
        row=r.point(1,0)
        self.assertFalse(row['cptp']);self.assertIsNone(row['decoded_expectation'])
        self.assertLess(row['min_pure_witness_eigenvalue'],0)
    def test_boundary_readout_keeps_cost_visible(self):
        row=r.point(.5,0)
        self.assertTrue(row['cptp']);self.assertEqual(row['readout_gain'],2)
        self.assertAlmostEqual(row['decoded_expectation'],1)
        self.assertAlmostEqual(row['decoded_zero_signal_variance'],4)
    def test_offline_page_contains_claim_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'demo.html';r.write_html(r.payload(),path);s=path.read_text()
            for x in ('Playback is not physical time','No actual record selected','sampling variance','not quantum-state recovery'):
                self.assertIn(x,s)
            self.assertNotIn('<script src=',s);self.assertNotIn('fetch(',s)
    def test_story_cases_exist_in_grid(self):
        known={(row['lambda'],row['t']) for row in r.payload()['grid']}
        self.assertTrue(all((lam,t) in known for lam,t in r.STORY))
    def test_invalid_fps_is_rejected(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)

if __name__=='__main__':unittest.main(verbosity=2)
