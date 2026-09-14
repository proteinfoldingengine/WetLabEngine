import importlib.util
import tempfile
from pathlib import Path
import unittest
import linear_module as m
r=None
if importlib.util.find_spec('replay'):
    import replay as r

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'linear-module replay absent')
    def test_all_112_cases(self):
        data=r.payload();self.assertEqual(len(data['cases']),112)
        self.assertTrue(all(c['linear_dimension']<=c['algebra_dimension'] for c in data['cases']))
    def test_prediction_curves_are_computed(self):
        for c in r.payload()['cases']:
            self.assertEqual(len(c['trajectory']),13)
            for f in c['trajectory']:
                self.assertAlmostEqual(f['direct_probability'],f['linear_probability'],places=10)
                self.assertGreaterEqual(f['direct_probability'],-1e-11)
                self.assertLessEqual(f['direct_probability'],1+1e-11)
    def test_no_physical_time_or_collapse(self):
        p=r.payload();self.assertIsNone(p['audit']['actual_record_selected'])
        self.assertFalse(p['audit']['physical_pruning_law_derived'])
    def test_self_contained_html(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'demo.html';r.write_html(r.payload(),path);text=path.read_text()
            for phrase in ['Playback is not physical time','not a density matrix','No actual record selected','multiplication']:
                self.assertIn(phrase,text)
            self.assertNotIn('<script src=',text);self.assertNotIn('fetch(',text)
    def test_bad_fps(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_story_cases_exist(self):
        cases={(c['family'],c['mask']) for c in r.payload()['cases']}
        self.assertTrue(all(k in cases for k in r.STORY))

if __name__=='__main__':unittest.main(verbosity=2)
