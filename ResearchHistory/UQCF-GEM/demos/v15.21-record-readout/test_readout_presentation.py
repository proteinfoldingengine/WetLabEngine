import importlib.util
import tempfile
import unittest
from pathlib import Path
import record_readout as m
r=None
target=Path(__file__).with_name('replay.py')
if target.exists():
    spec=importlib.util.spec_from_file_location('v1521_replay',target)
    r=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'record-readout presentation missing')
    def test_all_inputs_schedules_exported(self):
        p=m.payload();self.assertEqual(len(p['cases']),90)
        self.assertEqual(len({(c['input'],c['schedule_index']) for c in p['cases']}),90)
    def test_self_contained_html(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'replay.html';r.write_html(m.payload(),path);text=path.read_text()
            for phrase in ['Playback is not physical time','signed','No actual record selected','single-copy']:
                self.assertIn(phrase,text)
            self.assertNotIn('<script src=',text);self.assertNotIn('fetch(',text)
    def test_plot_data_not_substituted(self):
        p=m.payload()
        for c in p['cases']:
            self.assertEqual(len(c['ideal']),16);self.assertEqual(len(c['raw']),16)
            for a,b in zip(c['ideal'],c['decoded']):self.assertAlmostEqual(a,b,places=10)
    def test_all_movie_cases_exist(self):
        cases={(c['input'],c['schedule_index']) for c in m.payload()['cases']}
        self.assertTrue(all(c in cases for c in r.STORY))
    def test_invalid_fps(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_no_actuality_from_rendering(self):
        self.assertIsNone(m.payload()['audit']['actual_record_selected'])

if __name__=='__main__':unittest.main(verbosity=2)
