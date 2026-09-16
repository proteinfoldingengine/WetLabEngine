import importlib.util
from pathlib import Path
import tempfile
import unittest
import coherent_records as m
if importlib.util.find_spec('replay'):
    import replay as r
else:r=None

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'coherence replay not implemented')
    def test_all_schedules_and_stages(self):
        p=m.visual_payload()
        self.assertEqual(len(p['branches']),5)
        self.assertTrue(all(len(b['frames'])==5 for b in p['branches']))
    def test_all_record_probabilities_remain_normalized(self):
        for b in m.visual_payload()['branches']:
            for f in b['frames']:self.assertAlmostEqual(sum(f['record_probabilities']),1.,places=11)
    def test_offline_html_and_claims(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'demo.html';r.write_html(m.visual_payload(),path)
            txt=path.read_text()
            for s in ['Playback is not physical time','No actual record selected','joint state','declared pinching']:
                self.assertIn(s,txt)
            self.assertNotIn('<script src=',txt)
            self.assertNotIn('fetch(',txt)
    def test_no_offdiagonal_pinched_blocks(self):
        for b in m.visual_payload()['branches']:
            for f in b['frames']:
                for i in range(16):
                    for j in range(16):
                        if i!=j:self.assertEqual(f['pinched_blocks'][i][j],0.)
    def test_fps_guard(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_payload_does_not_add_actuality(self):
        self.assertIsNone(m.visual_payload()['audit']['actual_record_selected'])

if __name__=='__main__':unittest.main(verbosity=2)
