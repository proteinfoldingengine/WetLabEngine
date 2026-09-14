import json
from pathlib import Path
import tempfile
import unittest
import replay


class ReplayTests(unittest.TestCase):
    def test_payload_has_dimensions_not_gravity_scores(self):
        text = json.dumps(replay.payload()).lower()
        self.assertIn('candidates', text)
        self.assertNotIn('holonomy', text)
        self.assertNotIn('newton', text)
        self.assertNotIn('einstein', text)

    def test_html_is_offline_and_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'index.html'
            replay.write_html(replay.payload(), p)
            text = p.read_text()
            self.assertIn('No gravity observable was used to choose the coupling', text)
            self.assertIn('Scale unresolved', text)
            self.assertIn('Playback is not physical time', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_movie_fps_guard(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)

    def test_q_control_is_visibly_not_physical_candidate(self):
        p = replay.payload()
        self.assertEqual(p['audit']['q_control']['role'], 'BASELINE_CONTROL')
        self.assertEqual(p['audit']['q_control']['dimension'], 3)
        self.assertEqual(p['audit']['status'], 'PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK')


if __name__ == '__main__':
    unittest.main(verbosity=2)
