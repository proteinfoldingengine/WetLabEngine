import importlib.util
from pathlib import Path
import tempfile
import unittest
import retention_family as m
p=Path(__file__).with_name('replay.py');r=None
if p.exists():
    spec=importlib.util.spec_from_file_location('family_replay',p);r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class ViewTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'family presentation absent')
    def test_all_grid_points_are_computed(self):
        data=r.payload();self.assertEqual(len(data['points']),81)
        for point in data['points']:self.assertAlmostEqual(point['distance'],point['radius'],places=10)
    def test_phase_changes_state_not_modulus(self):
        data=r.payload()
        self.assertGreater(max(p['reference_distance'] for p in data['points'] if p['radius']==1),.99)
    def test_all_15_partitions_exported(self):
        data=r.payload();self.assertEqual(len(data['partitions']),15)
        for c in data['partitions']:self.assertEqual(len(c['matrix']),4)
    def test_self_contained_and_no_time_claim(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'demo.html';r.write_html(r.payload(),p);s=p.read_text()
            for text in ['No actual outcome selected','not physical time','idempotent','same supplied event']:
                self.assertIn(text,s)
            self.assertNotIn('<script src=',s);self.assertNotIn('fetch(',s)
    def test_video_guard(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),0)
    def test_view_does_not_select_a_law(self):
        self.assertFalse(r.payload()['audit']['physical_pruning_law_derived'])
        self.assertIsNone(r.payload()['audit']['actual_record_selected'])
if __name__=='__main__':unittest.main(verbosity=2)
