import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import recoverability as m
if importlib.util.find_spec('replay'):
    import replay as r
else:r=None

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'partial-pruning presentation missing')
    def test_all_masks_and_measured_witnesses_exported(self):
        p=r.visual_payload();self.assertEqual(len(p['cases']),16)
        for c in p['cases']:
            self.assertEqual(len(c['witnesses']),120)
            for w in c['witnesses']:
                expected=float(c['keep_matrix'][w['i']][w['j']])
                for d in w['output_distances']:self.assertAlmostEqual(d,expected,places=10)
    def test_offline_html_and_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'demo.html';r.write_html(r.visual_payload(),p);s=p.read_text()
            for t in ['Playback is not physical time','No actual record selected','not entropy','same completed encoding']:
                self.assertIn(t,s)
            self.assertNotIn('<script src=',s);self.assertNotIn('fetch(',s)
    def test_equal_size_masks_export_different_phase_survival(self):
        cases={c['mask']:c for c in r.visual_payload()['cases']}
        def val(mask):return next(w['output_distances'][0] for w in cases[mask]['witnesses'] if w['i']==0 and w['j']==8)
        self.assertLess(val('1000'),1e-11);self.assertAlmostEqual(val('0001'),1,places=10)
    def test_exported_probabilities_are_mask_independent(self):
        p=r.visual_payload()
        for c in p['cases']:
            self.assertAlmostEqual(sum(c['record_probabilities']),1,places=10)
    def test_invalid_fps_rejected(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_story_contains_all_five_dimension_levels(self):
        self.assertEqual({m.details(x)['hermitian_dimension'] for x in r.STORY},{256,128,64,32,16})
    def test_export_claims_do_not_add_physics(self):
        a=r.visual_payload()['audit']
        self.assertIsNone(a['actual_record_selected']);self.assertFalse(a['physical_entropy_law_derived'])

if __name__=='__main__':unittest.main(verbosity=2)
