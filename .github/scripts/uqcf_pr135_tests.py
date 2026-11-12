"""Rejecting controls for review plumbing, not historical scientific tests."""
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import base64

import uqcf_pr135_integrity as integrity
import uqcf_pr135_review as review
import uqcf_pr135_publication as publication

def encoded(obj):
    return (json.dumps(obj, sort_keys=True) + '\n').encode()

def verdict():
    return {'verdict': 'ACCEPTED', 'findings': [], 'missing_assumptions': [], 'counterexamples': [], 'limitations': ['source audit only'], 'constructive_analysis': [], 'native_bridge_status': 'NOT_DERIVED', 'next_native_obligation': 'Earn the receiver correspondence.'}

def response(v=None):
    return {'modelVersion': review.MODEL, 'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': json.dumps(v or verdict())}]}}]}

class PacketControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock, cls.raw = integrity.load_sources(integrity.ROOT)

    def test_complete_original_sources_and_all_members(self):
        self.assertEqual(len(self.raw), 115)
        self.assertEqual(sum(len(x['members']) for x in self.lock['archives']), 74)

    def reject_lock(self, edit):
        lock = copy.deepcopy(self.lock); edit(lock)
        with self.assertRaises((ValueError, KeyError)):
            integrity.validate_sources(integrity.ROOT, lock)

    def test_missing_source_rejected(self):
        self.reject_lock(lambda x: x['files'].pop())

    def test_duplicate_source_rejected(self):
        self.reject_lock(lambda x: x['files'].append(x['files'][0]))

    def test_substituted_source_rejected(self):
        self.reject_lock(lambda x: x['files'][0].update(path=integrity.BASE + '/nonexistent.md'))

    def test_wrong_digest_rejected(self):
        self.reject_lock(lambda x: x['files'][0].update(sha256='0' * 64))

    def test_wrong_byte_length_rejected(self):
        self.reject_lock(lambda x: x['files'][0].update(bytes=x['files'][0]['bytes'] + 1))

    def test_wrong_git_blob_rejected(self):
        self.reject_lock(lambda x: x['files'][0].update(git_blob='0' * 40))

    def test_wrong_provenance_rejected(self):
        self.reject_lock(lambda x: x.update(baseline='0' * 40))

    def test_missing_member_rejected(self):
        self.reject_lock(lambda x: x['archives'][0]['members'].pop())

    def test_duplicated_member_rejected(self):
        self.reject_lock(lambda x: x['archives'][0]['members'].append(x['archives'][0]['members'][0]))

    def test_substituted_extraction_rejected(self):
        self.reject_lock(lambda x: x['archives'][0]['members'][0].update(copy_path=x['files'][0]['path']))

    def test_additional_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); shutil.copytree(integrity.ROOT / integrity.BASE, root / integrity.BASE)
            (root / integrity.BASE / 'unexpected.txt').write_text('injected')
            with self.assertRaises(ValueError): integrity.validate_sources(root, self.lock)

    def test_changed_original_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); shutil.copytree(integrity.ROOT / integrity.BASE, root / integrity.BASE)
            p = root / self.lock['files'][0]['path']; p.write_bytes(p.read_bytes() + b'\n')
            with self.assertRaises(ValueError): integrity.validate_sources(root, self.lock)

    def test_prompt_full_exact_text_and_independent_reconstruction(self):
        data = {p: (integrity.ROOT / p).read_bytes() for p in integrity.document_paths(self.lock) + [integrity.REL + '/PROMPT.md']}
        prompt = integrity.build_prompt(integrity.ROOT, self.lock)
        self.assertEqual(prompt, publication.prompt_from(data, self.lock))
        self.assertEqual(len(integrity.document_paths(self.lock)), 106)
        for p in integrity.document_paths(self.lock):
            framed = ('\nEXACT DOCUMENT ' + p + '\nUTF8-BYTES ' + str(len(data[p])) + '\n').encode() + data[p] + b'\nEND EXACT DOCUMENT\n'
            self.assertIn(framed, prompt)

    def test_publication_rebuilds_complete_packet_and_rejects_wrong_tree(self):
        tree = {r['path']: {'path': r['path'], 'sha': r['git_blob']} for r in self.lock['files']}
        blobs = {integrity.identity(raw)['git_blob']: raw for raw in self.raw.values()}
        def api(path):
            sha = path.rsplit('/', 1)[1]
            return {'sha': sha, 'encoding': 'base64', 'content': base64.b64encode(blobs[sha]).decode()}
        self.assertEqual(publication.reconstruct_sources(self.lock, tree, tree, api), self.raw)
        bad = copy.deepcopy(tree); next(iter(bad.values()))['sha'] = '0' * 40
        with self.assertRaises(ValueError): publication.reconstruct_sources(self.lock, tree, bad, api)

class ReviewControls(unittest.TestCase):
    def test_valid_raw_response(self):
        _, v, model = review.parse_response(encoded(response()))
        review.accepted(v); self.assertEqual(model, review.MODEL)

    def test_adverse_response_retained_and_rejected(self):
        for status in ('REVISE', 'FAIL'):
            v = verdict(); v['verdict'] = status; v['findings'] = ['substantive defect']
            _, parsed, _ = review.parse_response(encoded(response(v)))
            self.assertEqual(parsed['verdict'], status)
            with self.assertRaises(ValueError): review.accepted(parsed)

    def test_accepted_with_unresolved_findings_rejected(self):
        for key in ('findings', 'missing_assumptions', 'counterexamples'):
            v = verdict(); v[key] = ['unresolved']
            with self.assertRaises(ValueError): review.accepted(v)

    def test_wrong_or_missing_model_rejected(self):
        for model in (None, 'different-model'):
            r = response(); r['modelVersion'] = model
            with self.assertRaises(ValueError): review.parse_response(encoded(r))

    def test_truncated_and_ambiguous_replies_rejected(self):
        r = response(); r['candidates'][0]['finishReason'] = 'MAX_TOKENS'
        with self.assertRaises(ValueError): review.parse_response(encoded(r))
        r = response(); r['candidates'].append(r['candidates'][0])
        with self.assertRaises(ValueError): review.parse_response(encoded(r))

    def test_blocked_prompt_and_duplicate_json_rejected(self):
        r = response(); r['promptFeedback'] = {'blockReason': 'BLOCKED'}
        with self.assertRaises(ValueError): review.parse_response(encoded(r))
        with self.assertRaises(ValueError): review.parse_response(b'{"candidates":[],"candidates":[]}')

    def test_thought_only_text_rejected(self):
        r = response(); r['candidates'][0]['content']['parts'][0]['thought'] = True
        with self.assertRaises(ValueError): review.parse_response(encoded(r))

    def test_exact_model_transport_one_generation_and_no_key_in_saved_request(self):
        calls = []
        def opener(req, timeout):
            calls.append((req.method, req.full_url, req.data))
            return io.BytesIO(encoded({'name': 'models/' + review.MODEL, 'supportedGenerationMethods': ['generateContent']}) if req.method == 'GET' else encoded(response()))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); prompt = b'complete exact source input'
            review.call_model(out, 'test-key-never-persist', prompt, opener)
            self.assertEqual([c[0] for c in calls], ['GET', 'POST'])
            self.assertEqual(json.loads((out / 'request.json').read_bytes())['contents'][0]['parts'][0]['text'], prompt.decode())
            self.assertNotIn(b'test-key-never-persist', (out / 'request.json').read_bytes())

    def test_unavailable_requested_model_does_not_generate(self):
        calls = []
        def opener(req, timeout):
            calls.append(req.method)
            return io.BytesIO(encoded({'name': 'models/different', 'supportedGenerationMethods': ['generateContent']}))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): review.call_model(Path(tmp), 'fake', b'input', opener)
        self.assertEqual(calls, ['GET'])

class PublicationControls(unittest.TestCase):
    def setUp(self):
        self.context = {'source_sha': 'a' * 40, 'workflow_sha': 'a' * 40, 'run_id': '1', 'run_attempt': '1', 'repository': integrity.REPOSITORY}
        self.inputs = {}; self.lock = {}; self.prompt = b'exact prompt'
        self.upstream = {'input_manifest.json': encoded(self.inputs), 'source_manifest.json': encoded(self.lock)}
        self.upstream['integrity.json'] = encoded({'status': 'PASS', **self.context, 'scientific_execution': False, 'source_lock_sha256': publication.LOCK_HASH, 'prompt_sha256': publication.digest(self.prompt), **{k + '_sha256': publication.digest(v) for k, v in (('input_manifest', self.upstream['input_manifest.json']), ('source_manifest', self.upstream['source_manifest.json']))}})
        raw = encoded(response()); answer, v, model = review.parse_response(raw)
        self.art = {'input_manifest.json': encoded(self.inputs), 'prompt.txt': self.prompt, 'request.json': encoded({'contents': [{'role': 'user', 'parts': [{'text': self.prompt.decode()}]}], 'generationConfig': {'temperature': 0, 'maxOutputTokens': 32768, 'responseMimeType': 'application/json'}}), 'response.json': raw, 'review.txt': answer, 'verdict.json': encoded(v), 'model_metadata.json': encoded({'name': 'models/' + review.MODEL, 'supportedGenerationMethods': ['generateContent']})}
        self.manifest = {'status': 'ACCEPTED', **self.context, 'model_requested': review.MODEL, 'model_returned': model, 'generation_calls_maximum': 1, 'integrity_artifacts': {k: publication.digest(v) for k, v in self.upstream.items()}}
        self.seal()

    def seal(self):
        self.manifest['artifact_hashes'] = {k: publication.digest(v) for k, v in self.art.items() if k != 'manifest.json'}
        self.art['manifest.json'] = encoded(self.manifest)

    def verify(self):
        return publication.verify_review(self.art, self.upstream, self.context, self.inputs, self.lock, self.prompt)

    def test_independent_publication_acceptance(self):
        self.assertEqual(self.verify()[0]['verdict'], 'ACCEPTED')

    def test_tampered_prompt_even_with_new_artifact_hash_rejected(self):
        self.art['prompt.txt'] += b' favorable summary'; self.seal()
        with self.assertRaises(ValueError): self.verify()

    def test_spoofed_parsed_verdict_rejected(self):
        v = verdict(); v['verdict'] = 'REVISE'; self.art['response.json'] = encoded(response(v)); self.seal()
        with self.assertRaises(ValueError): self.verify()

    def test_stale_run_rejected(self):
        self.manifest['run_id'] = '2'; self.seal()
        with self.assertRaises(ValueError): self.verify()

    def test_replaced_generation_request_rejected(self):
        self.art['request.json'] = b'{}'; self.seal()
        with self.assertRaises(ValueError): self.verify()

    def test_corrupted_integrity_evidence_rejected(self):
        self.upstream['source_manifest.json'] = b'{"wrong":true}'
        with self.assertRaises(ValueError): self.verify()

    def test_wrong_returned_model_with_consistent_stored_manifest_rejected(self):
        r = response(); r['modelVersion'] = 'another-model'; self.art['response.json'] = encoded(r); self.manifest['model_returned'] = 'another-model'; self.seal()
        with self.assertRaises(ValueError): self.verify()

if __name__ == '__main__':
    unittest.main(verbosity=2)
