#!/usr/bin/env python3
"""Reject four false integration records; checks audit plumbing, not science.

Usage: python check_audit_rejections.py REPO PR_SNAPSHOT.json OUTPUT.json
"""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

repo, source, output = sys.argv[1:]
valid = json.loads(Path(source).read_text())
cases = {}
missing = copy.deepcopy(valid)
missing['prs'] = [p for p in missing['prs'] if p['pr'] != 132]
cases['missing_rank_refinement_merge'] = missing
duplicate = copy.deepcopy(valid)
duplicate['prs'].append(copy.deepcopy(duplicate['prs'][0]))
cases['duplicated_pr_record'] = duplicate
substitute = copy.deepcopy(valid)
next(p for p in substitute['prs'] if p['pr'] == 128)['head'] = next(p for p in substitute['prs'] if p['pr'] == 135)['head']
cases['substituted_reviewed_head'] = substitute
wrong_merge = copy.deepcopy(valid)
next(p for p in wrong_merge['prs'] if p['pr'] == 132)['merge_sha'] = next(p for p in wrong_merge['prs'] if p['pr'] == 110)['merge_sha']
cases['wrong_actual_merge_identity'] = wrong_merge
records = []
with tempfile.TemporaryDirectory(prefix='uqcf-merge-audit-controls-') as temp:
    for name, case in cases.items():
        raw = (json.dumps(case, indent=2) + '\n').encode()
        f = Path(temp) / (name + '.json')
        f.write_bytes(raw)
        p = subprocess.run([sys.executable, str(Path(__file__).with_name('audit_integrated_trees.py')),
                            repo, str(f), str(Path(temp) / 'rejected-output.json')],
                           capture_output=True, text=True)
        assert p.returncode != 0 and 'AssertionError' in p.stderr, (name, p.returncode, p.stderr)
        records.append({'name': name, 'mutation_sha256': hashlib.sha256(raw).hexdigest(),
                        'rejected': True, 'exit_code': p.returncode,
                        'assertion': p.stderr.strip().splitlines()[-1]})
result = {'status': 'PASS', 'scope': 'Four rejecting integration-audit controls; no scientific simulation or theorem test.',
          'controls': records}
Path(output).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
