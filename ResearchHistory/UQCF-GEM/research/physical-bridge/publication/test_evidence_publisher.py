"""Publication safety contracts. These are not mathematical-review tests."""
import base64
import hashlib
import importlib.util
import io
from pathlib import Path
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
MODULE = HERE / 'evidence_publisher.py'


class PublicationContracts(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.is_file(), 'Evidence publisher not implemented (expected RED)')
        spec = importlib.util.spec_from_file_location('publisher_under_test', MODULE)
        self.p = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.p)

    def archive(self, names):
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w') as z:
            for name, content in names:
                z.writestr(name, content)
        return out.getvalue()

    def test_exact_archive_keeps_empty_members(self):
        blob = self.archive([('first.txt', b'exact\n'), ('empty.log', b'')])
        files = self.p.unpack(blob, hashlib.sha256(blob).hexdigest(), {'first.txt', 'empty.log'})
        self.assertEqual(files, {'first.txt': b'exact\n', 'empty.log': b''})

    def test_wrong_digest_missing_duplicate_and_unsafe_members_rejected(self):
        cases = [[('../outside', b'a')], [('x', b'a'), ('x', b'b')], [('y', b'a')]]
        for names in cases:
            with self.subTest(names=names):
                blob = self.archive(names)
                with self.assertRaises(self.p.PublicationError):
                    self.p.unpack(blob, hashlib.sha256(blob).hexdigest(), {'x'})
        blob = self.archive([('x', b'a')])
        with self.assertRaises(self.p.PublicationError):
            self.p.unpack(blob, '0' * 64, {'x'})

    def test_evidence_only_path_and_budget_guard(self):
        for name in ('.github/workflows/x.yml', self.p.PREFIX + '../x', '/tmp/x'):
            with self.assertRaises(self.p.PublicationError):
                self.p.validate({name: b'x'})
        with self.assertRaises(self.p.PublicationError):
            self.p.validate({self.p.PREFIX + 'x': b'x' * (self.p.LIMIT + 1)})

    def test_manifest_hashes_exact_bytes(self):
        files = {self.p.PREFIX + 'test/x': b'x\n'}
        row = self.p.file_manifest(files)[self.p.PREFIX + 'test/x']
        self.assertEqual(row['size'], 2)
        self.assertEqual(row['sha256'], hashlib.sha256(b'x\n').hexdigest())
        self.assertEqual(row['git_blob'], hashlib.sha1(b'blob 2\0x\n').hexdigest())

    def fake(self, corrupt=False, collision=False, denied=False):
        p = self.p
        class API:
            def __init__(self):
                self.calls, self.blobs, self.rows = [], {}, []
                self.ref = 'd' * 40 if collision else None
            def json(self, method, path, data=None):
                self.calls.append((method, path, data))
                if denied:
                    raise p.APIError(403, 'Denied')
                if path.startswith('git/ref/'):
                    if self.ref is None:
                        raise p.APIError(404, 'Absent')
                    return {'object': {'sha': self.ref}}
                if path == 'git/refs':
                    self.ref = data['sha']
                    return {'object': {'sha': self.ref}}
                if path == 'git/commits/' + 'a' * 40:
                    return {'tree': {'sha': '1' * 40}}
                if path == 'git/blobs' and method == 'POST':
                    body = base64.b64decode(data['content'])
                    sha = p.git_blob(body); self.blobs[sha] = body
                    return {'sha': sha}
                if path == 'git/trees':
                    for row in data['tree']:
                        if 'content' in row:
                            body = row['content'].encode()
                            sha = p.git_blob(body); self.blobs[sha] = body
                        else:
                            sha = row['sha']
                        self.rows.append({'filename': row['path'], 'status': 'added', 'sha': sha})
                    return {'sha': '2' * 40}
                if path == 'git/commits':
                    return {'sha': 'b' * 40, 'parents': [{'sha': data['parents'][0]}],
                            'tree': {'sha': data['tree']}}
                if path.startswith('compare/'):
                    return {'files': self.rows, 'total_commits': 1}
                if path.startswith('git/blobs/'):
                    body = b'corrupt' if corrupt else self.blobs[path.rsplit('/', 1)[1]]
                    return {'encoding': 'base64', 'content': base64.b64encode(body).decode()}
                if path.startswith('git/refs/') and method == 'PATCH':
                    self.ref = data['sha']; return {'object': {'sha': self.ref}}
                raise AssertionError((method, path, data))
        return API()

    def test_seed_then_evidence_only_nonforce_update(self):
        api = self.fake()
        files = {self.p.PREFIX + 'test/x.txt': b'payload\n',
                 self.p.PREFIX + 'test/archive.zip': b'\xff\x00'}
        sha = self.p.publish(api, 'a' * 40, 'research/test-evidence', files)
        self.assertEqual(sha, 'b' * 40)
        creates = [d for m, u, d in api.calls if u == 'git/refs']
        self.assertEqual(creates[0]['sha'], 'a' * 40)
        updates = [d for m, u, d in api.calls if m == 'PATCH']
        self.assertEqual(updates, [{'sha': 'b' * 40, 'force': False}])
        self.assertTrue(all(r['filename'].startswith(self.p.PREFIX) for r in api.rows))

    def test_readback_corruption_prevents_reference_update(self):
        api = self.fake(corrupt=True)
        with self.assertRaises(self.p.PublicationError):
            self.p.publish(api, 'a' * 40, 'research/test-evidence', {self.p.PREFIX + 'x': b'x'})
        self.assertFalse(any(m == 'PATCH' for m, _, _ in api.calls))

    def test_reference_collision_fails_closed(self):
        api = self.fake(collision=True)
        with self.assertRaises(self.p.PublicationError):
            self.p.publish(api, 'a' * 40, 'research/test-evidence', {self.p.PREFIX + 'x': b'x'})
        self.assertFalse(any(m in ('POST', 'PATCH') for m, _, _ in api.calls))

    def test_denied_access_is_not_retried_with_other_credentials(self):
        api = self.fake(denied=True)
        with self.assertRaises(self.p.APIError):
            self.p.publish(api, 'a' * 40, 'research/test-evidence', {self.p.PREFIX + 'x': b'x'})
        self.assertEqual(len(api.calls), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
