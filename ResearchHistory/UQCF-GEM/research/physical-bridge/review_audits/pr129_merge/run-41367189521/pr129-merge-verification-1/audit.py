"""Exact-merge integration replay; no model request or scientific-source edits."""
from pathlib import Path
import hashlib, importlib.util, json, lzma, os, shutil, subprocess, sys, zipfile

SCIENCE = '084617b4c392b8955f0a19d2c2b2c02dfa8d9d91'
BASE = '1f1394d1a8708464bab064c787d396a28d0c5a86'
PR = '324183d11baec30926e8e995ce033d0c07ea06af'
root, out = map(lambda x: Path(x).resolve(), sys.argv[1:3])
first = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
out.mkdir(parents=True, exist_ok=True)
uq = root / 'ResearchHistory/UQCF-GEM'
stage = uq / 'research/physical-bridge/receiver_delivery_boundary'
fcv = uq / 'foundational-closure-verification'
commands, deterministic, sources = [], [], set()

def sha(raw): return hashlib.sha256(raw).hexdigest()
def write(name, obj):
    (out / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')
def git(*args): return subprocess.check_output(['git', *args], cwd=root)
def call(name, args, cwd=root):
    with (out / (name + '.log')).open('wb') as log:
        result = subprocess.run(args, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
    commands.append(dict(name=name, argv=args, cwd=str(cwd.relative_to(root)), exit_code=result.returncode))
    write('commands.json', commands)
    print(name, result.returncode, flush=True)
    if result.returncode: raise RuntimeError('Nonzero command: ' + name)
def capture(name, args, cwd=root):
    with (out / name).open('wb') as target, (out / (name + '.stderr.log')).open('wb') as err:
        result = subprocess.run(args, cwd=cwd, stdout=target, stderr=err)
    commands.append(dict(name=name, argv=args, cwd=str(cwd.relative_to(root)), exit_code=result.returncode))
    write('commands.json', commands)
    print(name, result.returncode, flush=True)
    if result.returncode: raise RuntimeError('Nonzero command: ' + name)
    deterministic.append(name)
def check_bytes(raw, record):
    assert len(raw) == record['bytes'] and sha(raw) == record['sha256'], 'Byte integrity mismatch'
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

try:
    assert git('rev-parse', 'HEAD').decode().strip() == SCIENCE
    assert git('show', '-s', '--format=%P', 'HEAD').decode().strip().split() == [BASE, PR]
    paths = git('diff', '--name-only', BASE, SCIENCE).decode().splitlines()
    assert len(paths) == 67
    merge_blobs = {}
    for path in paths:
        a = git('rev-parse', SCIENCE + ':' + path).decode().strip()
        b = git('rev-parse', PR + ':' + path).decode().strip()
        assert a == b, path
        merge_blobs[path] = a
    write('merge-blobs.json', merge_blobs)

    original = stage / 'evidence/actions-41313483346'
    successor = stage / 'successor_t241/evidence/actions-41335726832'
    legacy = module('legacy_review', root / '.github/scripts/uqcf_receiver_delivery_review.py')
    old_paths = dict(legacy.DOCS)
    old_paths.update({'EVIDENCE_' + n: original / 'evidence' / n for n in ('verification.json', 'controls.json', 'publication.json')})
    reviews = [original / 'review', stage / 'successor_t241/review/actions-41340518437', stage / 't249_review_evidence/review']
    doc_checks = {}
    for review in reviews:
        prompt = (review / 'prompt.txt').read_bytes()
        docs = json.loads((review / 'documents.json').read_text())
        rows = {}
        for label, record in docs.items():
            path = root / record['path'] if 'path' in record else old_paths[label]
            raw = path.read_bytes(); check_bytes(raw, record)
            assert raw in prompt, label
            sources.add(str(path.relative_to(root)))
            rows[label] = dict(record, resolved_path=str(path.relative_to(root)))
        manifest = json.loads((review / 'artifact_manifest.json').read_text())
        for name, record in manifest.items(): check_bytes((review / name).read_bytes(), record)
        doc_checks[str(review.relative_to(root))] = rows
    assert [len(v) for v in doc_checks.values()] == [22, 19, 20]
    write('review-document-readback.json', doc_checks)
    t249 = stage / 't249_review_evidence'
    pub = json.loads((t249 / 'PUBLICATION_AUDIT.json').read_text())
    for name, key, folder in [('review-run-41356747755.zip', 'review_zip_sha256', 'review'),
                              ('failure-run-41356533442.zip', 'prior_failure_zip_sha256', 'prior_failure')]:
        archive = t249 / name
        assert sha(archive.read_bytes()) == pub[key]
        with zipfile.ZipFile(archive) as z:
            files = [n for n in z.namelist() if not n.endswith('/')]
            assert set(files) == {p.name for p in (t249 / folder).iterdir() if p.is_file()}
            for n in files: assert z.read(n) == (t249 / folder / n).read_bytes()
    sys.path.insert(0, str(root / '.github/scripts'))
    from uqcf_preparability_review import parse_response, accepted
    answer, verdict, model = parse_response((reviews[-1] / 'response.json').read_bytes())
    assert answer == (reviews[-1] / 'review.txt').read_bytes()
    assert verdict == json.loads((reviews[-1] / 'verdict.json').read_text())
    accepted(verdict); assert verdict['native_bridge_status'] == 'NOT_DERIVED'
    write('review-gate.json', dict(verdict=verdict, model=model, review_run=41356747755,
                                  response_sha256=sha((reviews[-1] / 'response.json').read_bytes())))

    # Snapshot exact committed sources before producers write their output files.
    scope = ['.github/scripts', 'ResearchHistory/UQCF-GEM/AGENTS.md',
             str(fcv.relative_to(root)), str(stage.relative_to(root)),
             'ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction',
             'ResearchHistory/UQCF-GEM/demos/v16.15F-graded-obstruction-descent']
    with (out / 'scientific-source.zip').open('wb') as target:
        subprocess.run(['git', 'archive', '--format=zip', SCIENCE, *scope, *sorted(sources)], cwd=root, stdout=target, check=True)
    shutil.copyfile(__file__, out / 'audit.py')
    write('identity.json', dict(science_sha=SCIENCE, workflow_sha=os.environ.get('UQCF_WORKFLOW_SHA'),
                               run_id=os.environ.get('GITHUB_RUN_ID'), run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),
                               python=sys.version, script_sha256=sha(Path(__file__).read_bytes())))
    call('dependencies', [sys.executable, '-m', 'pip', 'freeze'])
    import sympy, mpmath
    assert sys.version_info[:2] == (3, 11) and sympy.__version__ == '1.13.3' and mpmath.__version__ == '1.3.0'
    call('fcv-publication-checksums', ['sha256sum', '-c', 'PUBLICATION_SHA256SUMS'], fcv)
    call('fcv-tests', [sys.executable, 'tests/test_fcv.py'], fcv)
    call('parent-tests', [sys.executable, '-m', 'unittest', '-v', 'test_pruning_consistency_audit'], uq / 'demos/v15.56-response-selector-obstruction')
    historical = uq / 'demos/v16.15F-graded-obstruction-descent'
    call('historical-tests', [sys.executable, '-m', 'unittest', '-v'], historical)
    call('historical-reproduction', [sys.executable, 'gate.py'], historical)
    shutil.copyfile(historical / 'result.json', fcv / 'evidence/REPRODUCED_1615F.json')
    call('fcv-producer', [sys.executable, 'produce_certificates.py'], fcv)
    call('fcv-independent-verifier', [sys.executable, 'verify_certificates.py'], fcv)
    for name in ('certificates.json.xz', 'PRODUCTION.json', 'VERIFICATION.json', 'REPRODUCED_1615F.json'):
        target = 'fcv-' + name; shutil.copyfile(fcv / 'evidence' / name, out / target); deterministic.append(target)
    assert sha(lzma.decompress((out / 'fcv-certificates.json.xz').read_bytes())) == '21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6'
    assert json.loads((out / 'fcv-VERIFICATION.json').read_text())['all_valid'] is True

    for tag, directory, suffix, evidence in [('original', stage, '', original / 'evidence'),
                                            ('successor', stage / 'successor_t241', '_s', successor)]:
        call(tag + '-publication-checksums', ['sha256sum', '-c', 'SHA256SUMS'], evidence)
        producer = directory / ('produce' + suffix + '.py')
        certificate = tag + '-certificate.json'
        capture(certificate, [sys.executable, '-B', str(producer)])
        capture(tag + '-verification.json', [sys.executable, '-B', str(directory / ('verify' + suffix + '.py')), str(out / certificate), str(producer)])
        capture(tag + '-controls.json', [sys.executable, '-B', 'test_controls' + suffix + '.py', str(out / certificate), producer.name], directory)
        for n in ('certificate.json', 'verification.json', 'controls.json'):
            assert (out / (tag + '-' + n)).read_bytes() == (evidence / n).read_bytes(), tag + n

    if first:
        prior_manifest = json.loads((first / 'artifact_manifest.json').read_text())
        for name, record in prior_manifest.items(): check_bytes((first / name).read_bytes(), record)
        for name in deterministic:
            assert (out / name).read_bytes() == (first / name).read_bytes(), 'Fresh replay: ' + name
    write('receipt.json', dict(status='PASS', science_sha=SCIENCE, workflow_sha=os.environ.get('UQCF_WORKFLOW_SHA'),
                              reviewed_PR_head=PR, merged_paths=len(paths), review_documents=61,
                              fresh_publication_replay=bool(first), deterministic_files=deterministic,
                              native_bridge_status='NOT_DERIVED', scientific_breakthrough=False))
except Exception as exc:
    write('failure.json', dict(status='FAIL', error_type=type(exc).__name__, detail=str(exc)))
    raise
finally:
    write('artifact_manifest.json', {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
                                     for p in sorted(out.iterdir()) if p.is_file() and p.name != 'artifact_manifest.json'})
