"""GitHub-only development runner; preserves exact outcomes, logs and source."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent


def main():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise SystemExit('scientific execution is GitHub-only')
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    phase, output = sys.argv[1:3]
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    os.environ['V1654_DEV_OUTPUT'] = str(out.resolve())
    scientific = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if scientific != os.environ['SCIENTIFIC_SHA']:
        raise ValueError('checked-out scientific SHA mismatch')
    provenance = {'workflow_sha': os.environ['GITHUB_SHA'], 'scientific_sha': scientific,
                  'run_id': os.environ['GITHUB_RUN_ID'], 'attempt': os.environ['GITHUB_RUN_ATTEMPT'],
                  'phase': phase, 'preregistration': os.environ['PREREGISTRATION_SHA']}
    (out / 'PROVENANCE.json').write_text(json.dumps(provenance, indent=2, sort_keys=True)+'\n')
    sources = {}
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path.suffix in {'.py', '.json', '.md'} and '__pycache__' not in path.parts:
            rel = path.relative_to(HERE)
            data = path.read_bytes()
            dest = out / 'source' / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            sources[str(rel)] = hashlib.sha256(data).hexdigest()
    (out / 'SOURCE_MANIFEST.json').write_text(json.dumps(sources, indent=2, sort_keys=True)+'\n')
    suite = unittest.defaultTestLoader.discover(str(HERE / 'tests'), pattern='test_'+phase+'.py')
    with (out / 'tests.log').open('w') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print((out / 'tests.log').read_text())
    status = {'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
              'skipped': len(result.skipped), 'successful': result.wasSuccessful(), **provenance}
    (out / 'RESULT.json').write_text(json.dumps(status, indent=2, sort_keys=True)+'\n')
    if not result.wasSuccessful() or result.testsRun == 0 or result.skipped:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
