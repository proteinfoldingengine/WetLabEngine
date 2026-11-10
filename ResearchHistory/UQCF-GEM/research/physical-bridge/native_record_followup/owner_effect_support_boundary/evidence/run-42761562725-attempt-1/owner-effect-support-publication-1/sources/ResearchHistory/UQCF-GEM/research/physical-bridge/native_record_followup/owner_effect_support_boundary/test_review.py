"""Contract tests for the new review controller; no model calls."""
import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
MODULE=Path(__file__).parent/'review_controller.py'
if not MODULE.exists():
    MODULE=Path('.github/scripts/uqcf_owner_effect_support_review.py')
api=None
if MODULE.exists():
    spec=importlib.util.spec_from_file_location('controller',MODULE)
    api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)

class ReviewContracts(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(api,'review controller is not implemented')
    def verdict(self):
        return dict(verdict='ACCEPTED',findings=[],missing_assumptions=[],counterexamples=[],
                    limitations=[],reconstruction=['proof'],constructive_analysis=[],
                    native_bridge_status='NOT_DERIVED',next_native_obligation='access')
    def test_complete_and_adverse_verdicts(self):
        api.validate_verdict(self.verdict())
        v=self.verdict();v['verdict']='REVISE';v['findings']=['gap'];api.validate_verdict(v)
    def test_incomplete_or_contradictory_verdict_rejected(self):
        for field in ('reconstruction','next_native_obligation','native_bridge_status'):
            v=self.verdict();del v[field]
            with self.assertRaises((AssertionError,ValueError)):api.validate_verdict(v)
        v=self.verdict();v['findings']=['gap']
        with self.assertRaises((AssertionError,ValueError)):api.validate_verdict(v)
        v=self.verdict();v['verdict']='PASS'
        with self.assertRaises((AssertionError,ValueError)):api.validate_verdict(v)
    def test_manifest_exact_members_and_bytes(self):
        for mutation in ('delete','extra','change'):
            with tempfile.TemporaryDirectory() as d:
                p=Path(d);(p/'a').write_bytes(b'original')
                api.manifest(p);api.valid_manifest(p)
                if mutation=='delete':(p/'a').unlink()
                elif mutation=='extra':(p/'b').write_bytes(b'new')
                else:(p/'a').write_bytes(b'changed')
                with self.assertRaises((AssertionError,ValueError)):api.valid_manifest(p)
    def test_complete_stdout_comparison(self):
        expected='one\\ntwo\\n'
        api.compare_bytes(expected.encode(),expected.encode())
        for altered in ('one\\n','one\\ntwo\\ntwo\\n','one\\nthree\\n','one\\nTwo\\n'):
            with self.assertRaises((AssertionError,ValueError)):
                api.compare_bytes(altered.encode(),expected.encode())
    def test_manifest_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'artifact_manifest.json').write_text(json.dumps({'../outside':{}}))
            with self.assertRaises((AssertionError,ValueError)):api.valid_manifest(p)
class FailureAndRetryContracts(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(api)
    def test_duplicate_generation_guard(self):
        api.generation_guard('1','notehash',[])
        with self.assertRaises((AssertionError,ValueError)):api.generation_guard('2','notehash',[])
        with self.assertRaises((AssertionError,ValueError)):
            api.generation_guard('1','notehash',[dict(note_sha256='notehash',review_attempted=True)])
        api.generation_guard('1','notehash',[dict(note_sha256='notehash',review_attempted=False)])
        api.generation_guard('1','newnote',[dict(note_sha256='oldnote',review_attempted=True)])
    def test_remote_source_identity(self):
        raw=b'exact source'
        source=dict(content=raw.decode(),bytes=len(raw),sha256=api.sha(raw),blob=api.blob(raw))
        api.validate_remote_source(source,raw,api.blob(raw))
        with self.assertRaises((AssertionError,ValueError)):api.validate_remote_source(source,b'different',api.blob(b'different'))
        with self.assertRaises((AssertionError,ValueError)):api.validate_remote_source(source,raw,'wrongblob')
    def test_archive_includes_original_attempt_artifacts(self):
        try:
            from review_archive import select_artifacts
        except ModuleNotFoundError:
            from uqcf_owner_effect_support_archive import select_artifacts
        items=[dict(name='owner-effect-support-review-1',id=7),
               dict(name='owner-effect-support-verification-1',id=8),
               dict(name='owner-effect-support-publication-2',id=9),
               dict(name='unrelated',id=10)]
        self.assertEqual({a['id'] for a in select_artifacts(items)},{7,8,9})
    def test_failed_review_preserved_without_acceptance(self):
        try:
            from review_archive import disposition
        except ModuleNotFoundError:
            from uqcf_owner_effect_support_archive import disposition
        d=disposition({'verification':'success','review':'failure','publication':'skipped'},[],['publication'],None)
        self.assertFalse(d['scientific_pipeline_complete'])
        self.assertFalse(d['accepted'])
        self.assertEqual(d['preservation_status'],'PARTIAL')
        d=disposition({'verification':'success','review':'success','publication':'success'},[],[],{'verdict':'REVISE'})
        self.assertTrue(d['scientific_pipeline_complete'])
        self.assertFalse(d['accepted'])
if __name__=='__main__':unittest.main()
