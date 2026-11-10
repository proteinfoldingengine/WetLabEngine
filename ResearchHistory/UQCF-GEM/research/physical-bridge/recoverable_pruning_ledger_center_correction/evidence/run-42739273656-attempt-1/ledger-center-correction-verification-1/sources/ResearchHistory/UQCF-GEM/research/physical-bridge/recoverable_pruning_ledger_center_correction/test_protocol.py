import json,tempfile,unittest
from pathlib import Path
import uqcf_ledger_center_correction as p
class ProtocolTests(unittest.TestCase):
    def test_manifest_rejects_each_real_mutation(self):
        for change in ('modified','missing','added'):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as d:
                root=Path(d);(root/'x').write_text('frozen');p.manifest(root);p.valid_manifest(root)
                if change=='modified':(root/'x').write_text('altered')
                if change=='missing':(root/'x').unlink()
                if change=='added':(root/'y').write_text('extra')
                with self.assertRaises(AssertionError):p.valid_manifest(root)
    def test_contradictory_acceptance_rejected(self):
        with self.assertRaises(AssertionError):p.validate_verdict(dict(verdict='ACCEPTED',findings=['defect'],missing_assumptions=[],counterexamples=[],limitations=[],reconstruction=[],constructive_analysis=[],native_bridge_status='NOT_DERIVED',next_native_obligation='access'))
    def test_malformed_structure_rejected(self):
        with self.assertRaises(AssertionError):p.validate_verdict({'verdict':'ACCEPTED'})
    def test_adverse_verdict_is_preserved_not_blocked(self):
        p.validate_verdict(dict(verdict='REVISE',findings=['defect'],missing_assumptions=[],counterexamples=[],limitations=[],reconstruction=[],constructive_analysis=[],native_bridge_status='NOT_DERIVED',next_native_obligation='access'))
    def test_model_native_upgrade_is_not_silently_rewritten(self):
        v=dict(verdict='ACCEPTED',findings=[],missing_assumptions=[],counterexamples=[],limitations=[],reconstruction=[],constructive_analysis=[],native_bridge_status='DERIVED_FROM_SOURCES',next_native_obligation='none');p.validate_verdict(v);self.assertEqual(v['native_bridge_status'],'DERIVED_FROM_SOURCES')
if __name__=='__main__':unittest.main()
