import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'.github/scripts/uqcf_apparatus_record_review.py'

class ReviewIntegrityTest(unittest.TestCase):
    def test_constructive_response_is_required_by_both_gates(self):
        for filename in ('uqcf_apparatus_record_review.py', 'uqcf_apparatus_record_publication.py'):
            with self.subTest(filename=filename):
                spec=importlib.util.spec_from_file_location('gate_under_test', SCRIPT.with_name(filename))
                mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
                valid={'constructive_analysis': [{'attempt': 'Source-to-state association examined'}],
                       'next_native_obligation': 'Establish the source-bound physical moment.'}
                mod.validate_constructive_response(valid)
                for changed in ({}, {'constructive_analysis': []}, {'constructive_analysis': [' ']},
                                {'constructive_analysis': [{}]}, {'constructive_analysis': [None]},
                                {'next_native_obligation': ''}, {'next_native_obligation': []}):
                    bad={} if changed=={} else dict(valid, **changed)
                    with self.assertRaises(ValueError): mod.validate_constructive_response(bad)

    def test_exact_inputs_and_rejecting_controls(self):
        self.assertTrue(SCRIPT.is_file(), 'adapted review integration is not present')
        spec=importlib.util.spec_from_file_location('review_under_test', SCRIPT)
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        base=ROOT/mod.BASE
        mod.BASE=base
        docs=mod.inputs()
        packet=json.loads(docs['SOURCE_PACKET.json'])
        for source in packet['sources']:
            raw=source['content'].encode('utf-8')
            mod.verify_source_excerpt(source, raw)
        source=packet['sources'][0]; raw=source['content'].encode('utf-8')
        with self.assertRaises(ValueError): mod.verify_source_excerpt(source, raw+b'changed')
        wrong=dict(source, byte_end=source['byte_end']+1)
        with self.assertRaises(ValueError): mod.verify_source_excerpt(wrong, raw)
        wrong=dict(source, content=source['content']+'changed')
        with self.assertRaises(ValueError): mod.verify_source_excerpt(wrong, raw)
        prompt=mod.prompt(docs)
        self.assertIn(b'constructive', prompt)
        for content in docs.values(): self.assertIn(content, prompt)
        target=base/'RESULT.md'; original=target.read_bytes()
        try:
            target.write_bytes(original+b'changed')
            with self.assertRaises(ValueError): mod.inputs()
        finally: target.write_bytes(original)

if __name__=='__main__': unittest.main()

