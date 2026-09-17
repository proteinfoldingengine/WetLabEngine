import json
import tempfile
import unittest
from pathlib import Path

import replay


class ReplayTests(unittest.TestCase):
    def test_payload_has_fibers_and_provenance_not_gravity_scores(self):
        p = replay.payload()
        self.assertIn('fibers', p)
        self.assertIn('audit', p)
        text = json.dumps(p).lower()
        for forbidden in ('holonomy_score','newton_score','einstein_score','inverse_square_score'):
            self.assertNotIn(forbidden, text)

    def test_html_is_offline_and_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'index.html'
            replay.write_html(replay.payload(), path)
            text = path.read_text()
            self.assertIn('Microscopic difference is not automatically physical source difference', text)
            self.assertIn('Playback is not physical time', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_movie_guard(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)


if __name__ == '__main__':
    unittest.main()
