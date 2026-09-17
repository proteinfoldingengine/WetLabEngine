import json
import tempfile
import unittest
from pathlib import Path
import replay


class ReplayTests(unittest.TestCase):
    def test_payload_has_candidates_graph_fiber_and_audit(self):
        data = replay.payload()
        self.assertEqual(data['version'], 'v15.30')
        self.assertEqual(len(data['candidates']), 4)
        self.assertIn('typed_graph', data)
        self.assertIn('fibers', data)
        self.assertIn('audit', data)

    def test_payload_contains_no_gravity_or_coupling_scores(self):
        text = json.dumps(replay.payload()).lower()
        for forbidden in ('holonomy_score', 'newton_score', 'einstein_score',
                          'inverse_square_score', 'preferred_coupling'):
            self.assertNotIn(forbidden, text)

    def test_html_is_self_contained_and_declares_nonphysical_playback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'index.html'
            replay.write_html(replay.payload(), path)
            text = path.read_text()
            self.assertIn('Playback is not physical time', text)
            self.assertIn('No coupling member or gravity observable is evaluated', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_movie_guard_rejects_nonpositive_fps(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)


if __name__ == '__main__':
    unittest.main()
