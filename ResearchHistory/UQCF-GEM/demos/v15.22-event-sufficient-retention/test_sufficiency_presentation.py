import importlib.util
from pathlib import Path
import tempfile
import unittest
import numpy as np
import event_sufficiency as m
r=None
path=Path(__file__).with_name('replay.py')
if path.exists():
    spec=importlib.util.spec_from_file_location('v1522_replay',path)
    r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class PresentationTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'event-sufficiency replay absent')
    def test_contexts_match_computation(self):
        p=r.payload();self.assertEqual(len(p['cases']),29)
        self.assertEqual(p['cases'],m.audit()['cases'])
    def test_all_convex_comparison_points_valid(self):
        p=r.payload();self.assertEqual(len(p['comparison']),41)
        for f in p['comparison']:
            self.assertLess(f['matching_event_error'],1e-10)
            self.assertLess(f['other_event_probability_error'],1e-10)
            self.assertAlmostEqual(f['other_event_state_distance'],f['mixture_weight']/2,places=10)
            self.assertAlmostEqual(f['pair_distance'],1-f['mixture_weight'],places=10)
    def test_two_event_batch_matches_at_each_point(self):
        for f in r.payload()['comparison']:self.assertLess(f['two_event_batch_error'],1e-10)
    def test_offline_html_explicit_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'demo.html';r.write_html(r.payload(),p);txt=p.read_text()
            for word in ['Playback is not physical time','No actual record selected','post-event state','supplied next event']:
                self.assertIn(word,txt)
            self.assertNotIn('<script src=',txt);self.assertNotIn('fetch(',txt)
    def test_cptp_formula_matches_mixture_kraus(self):
        f=m.prior.start();ps=m.effects(f,'A1');rho=m.prior.start().rho
        for a in (0,.2,.5,1):
            ks=[np.sqrt(1-a)*np.eye(16),*(np.sqrt(a)*p for p in ps)]
            out=sum(k@rho@k.conj().T for k in ks)
            np.testing.assert_allclose(out,(1-a)*rho+a*m.retain(rho,ps),atol=1e-10)
    def test_video_rate_guard(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)

if __name__=='__main__':unittest.main(verbosity=2)
