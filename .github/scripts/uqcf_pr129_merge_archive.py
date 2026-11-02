"""Archive the completed merge-audit run, verifying original ZIPs and all members."""
from pathlib import Path
import hashlib, io, json, os, subprocess, urllib.error, urllib.request, zipfile

RUN = 41367189521
SCIENCE = '084617b4c392b8955f0a19d2c2b2c02dfa8d9d91'
CONTROLLER = '899793e16f360435af6cf86d1451cc9b81d57ce3'
repo = os.environ['GITHUB_REPOSITORY']
base = 'https://api.github.com/repos/' + repo
headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
out = Path('ResearchHistory/UQCF-GEM/research/physical-bridge/review_audits/pr129_merge') / ('run-' + str(RUN))
out.mkdir(parents=True, exist_ok=True)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs): return None
opener = urllib.request.build_opener(NoRedirect)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def api(path):
    with urllib.request.urlopen(urllib.request.Request(base + path, headers=headers), timeout=60) as r:
        return json.load(r)
def download(path):
    try:
        with opener.open(urllib.request.Request(base + path, headers=headers), timeout=60) as r: return r.read()
    except urllib.error.HTTPError as exc:
        if exc.code not in (301, 302, 303, 307, 308): raise
        target = exc.headers['Location']; assert target.startswith('https://')
        with urllib.request.urlopen(target, timeout=180) as r: return r.read()
def write(path, obj): path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')

try:
    run = api('/actions/runs/' + str(RUN))
    assert run['status'] == 'completed' and run['conclusion'] == 'success'
    assert run['head_sha'] == CONTROLLER and run['run_attempt'] == 1
    write(out / 'run.json', run)
    listing = api('/actions/runs/' + str(RUN) + '/artifacts?per_page=100')
    expected = {f'pr129-merge-{job}{kind}-1' for job in ('verification', 'publication') for kind in ('', '-controller')}
    artifacts = listing['artifacts']; assert {a['name'] for a in artifacts} == expected and len(artifacts) == 4
    receipts = []
    for item in artifacts:
        assert item['expired'] is False
        raw = download('/actions/artifacts/' + str(item['id']) + '/zip')
        assert item['digest'] == 'sha256:' + sha(raw), item['name']
        # Preserve original ZIP bytes in bounded Git blobs; concatenation recovers
        # the API-digested archive exactly, without recompression or repackaging.
        part_size = 32 * 1024 * 1024
        parts = []
        for offset in range(0, len(raw), part_size):
            part_name = item['name'] + '.zip.part-' + str(offset // part_size).zfill(3)
            data = raw[offset:offset + part_size]
            (out / part_name).write_bytes(data)
            parts.append(dict(path=part_name, bytes=len(data), sha256=sha(data)))
        assert sha(b''.join((out / p['path']).read_bytes() for p in parts)) == sha(raw)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            files = {n: z.read(n) for n in z.namelist() if not n.endswith('/')}
            assert all(Path(n).name == n for n in files), 'Unexpected nested ZIP path'
        if '-controller-' in item['name']:
            assert set(files) == {'PLAN.md', 'uqcf_pr129_merge_audit.py', 'uqcf-pr129-merge-audit.yml'}
            controller_paths = {'PLAN.md': out.parent / 'PLAN.md',
                                'uqcf_pr129_merge_audit.py': Path('.github/scripts/uqcf_pr129_merge_audit.py'),
                                'uqcf-pr129-merge-audit.yml': Path('.github/workflows/uqcf-pr129-merge-audit.yml')}
            for n, path in controller_paths.items(): assert files[n] == path.read_bytes()
        else:
            manifest = json.loads(files['artifact_manifest.json'])
            assert set(files) == set(manifest) | {'artifact_manifest.json'}
            for n, record in manifest.items():
                assert len(files[n]) == record['bytes'] and sha(files[n]) == record['sha256'], n
            receipt = json.loads(files['receipt.json'])
            assert receipt['status'] == 'PASS' and receipt['science_sha'] == SCIENCE
            assert receipt['workflow_sha'] == CONTROLLER and receipt['review_documents'] == 61
            assert receipt['native_bridge_status'] == 'NOT_DERIVED'
            assert receipt['fresh_publication_replay'] == ('publication' in item['name'])
            dest = out / item['name']; dest.mkdir(exist_ok=True)
            # The complete source ZIP is already retained inside the exact raw
            # archive parts; do not duplicate its large nested historical bundles.
            for n, raw_member in files.items():
                if n != 'scientific-source.zip': (dest / n).write_bytes(raw_member)
        receipts.append(dict(id=item['id'], name=item['name'], api_digest=item['digest'],
                             download_sha256=sha(raw), bytes=len(raw), members=len(files), raw_archive_parts=parts))
    jobs = api('/actions/runs/' + str(RUN) + '/jobs?per_page=100')['jobs']
    assert {j['name'] for j in jobs} == {'verification', 'publication'} and len(jobs) == 2
    for job in jobs:
        assert job['status'] == 'completed' and job['conclusion'] == 'success'
        (out / ('job-' + str(job['id']) + '.log')).write_bytes(download('/actions/jobs/' + str(job['id']) + '/logs'))
    write(out / 'jobs.json', jobs)
    write(out / 'EXTRACTION_POLICY.json', dict(raw_archives='Concatenate each DOWNLOAD_AUDIT.json raw_archive_parts list in order to reconstruct the original API-digested ZIP.',
                                              extracted='All evidence members except scientific-source.zip are duplicated as browsable files. That complete source snapshot remains inside each original ZIP. Controller ZIPs are retained as original parts.'))
    write(out / 'DOWNLOAD_AUDIT.json', dict(status='PASS', run_id=RUN, workflow_sha=CONTROLLER, science_sha=SCIENCE,
                                          artifacts=receipts, native_bridge_status='NOT_DERIVED'))
    write(out / 'ARCHIVE_MANIFEST.json', {str(p.relative_to(out)): dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()))
                                         for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'ARCHIVE_MANIFEST.json'})
    print('Both original artifact ZIPs, both controllers, all member manifests and completed job logs verified.')
    print(out)
except Exception as exc:
    write(out / 'archive-failure.json', dict(error_type=type(exc).__name__, detail=str(exc)[:500]))
    raise
