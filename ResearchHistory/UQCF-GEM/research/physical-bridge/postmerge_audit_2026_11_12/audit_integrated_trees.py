#!/usr/bin/env python3
"""Audit actual research merge trees and final publication blobs; no science run.

Usage: python audit_integrated_trees.py REPO PR_SNAPSHOT.json OUTPUT.json
Requires git objects for the snapshot, reviewed heads, and their ancestors.
Does not check out, modify, merge, or update any ref.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main(repo, snapshot_path, output_path):
    def git(*args, check=True):
        return subprocess.run(['git', '-C', repo, *args], check=check,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def out(*args):
        return git(*args).stdout.decode().strip()

    cache = {}

    def tree(ref):
        if ref not in cache:
            rows = {}
            for row in git('ls-tree', '-rz', ref).stdout.split(b'\0'):
                if row:
                    spec, name = row.split(b'\t', 1)
                    mode, kind, sha = spec.decode().split()
                    rows[name.decode()] = {'mode': mode, 'kind': kind, 'sha': sha}
            cache[ref] = rows
        return cache[ref]

    snapshot_bytes = Path(snapshot_path).read_bytes()
    snapshot = json.loads(snapshot_bytes)
    final = snapshot['snapshot_head']
    start = snapshot['baseline_before_merges']
    assert len({p['pr'] for p in snapshot['prs']}) == len(snapshot['prs']), 'duplicate PR'
    final_tree = tree(final)
    results = []
    all_changed = set()
    total_checks = 0
    previous_merge = start
    for pr in sorted(snapshot['prs'], key=lambda p: p['merged_at']):
        assert pr['merged'] and pr['state'] == 'closed'
        head, merge = pr['head'], pr['merge_sha']
        parents = out('show', '-s', '--format=%P', merge).split()
        assert len(parents) == 2, (pr['pr'], parents)
        assert parents[0] == previous_merge, (pr['pr'], 'missing or reordered first-parent integration')
        assert parents[1] == head, (pr['pr'], 'reviewed-head parent mismatch')
        git('merge-base', '--is-ancestor', merge, final)
        ancestor = out('merge-base', parents[0], head)
        actual_tree = out('show', '-s', '--format=%T', merge)
        reconstructed = git('merge-tree', '--write-tree', parents[0], head, check=False)
        reconstructed_lines = reconstructed.stdout.decode().splitlines()
        assert reconstructed.returncode == 0, (pr['pr'], reconstructed.stdout.decode(), reconstructed.stderr.decode())
        assert reconstructed_lines and reconstructed_lines[0] == actual_tree, (pr['pr'], 'merge tree mismatch')
        old, proposed, integrated = tree(ancestor), tree(head), tree(merge)
        changed = sorted(p for p in set(old) | set(proposed) if old.get(p) != proposed.get(p))
        assert changed, (pr['pr'], 'empty PR delta')
        at_merge, at_final, differing = [], [], []
        for path in changed:
            h = proposed.get(path)
            m, f = integrated.get(path), final_tree.get(path)
            row = {'path': path, 'reviewed': h, 'at_merge': m, 'at_final': f,
                   'merge_identical': m == h, 'final_identical': f == h}
            at_merge.append(row['merge_identical'])
            at_final.append(row['final_identical'])
            if not row['merge_identical'] or not row['final_identical']:
                differing.append(row)
            all_changed.add(path)
        total_checks += len(changed)
        results.append({'pr': pr['pr'], 'head': head, 'merge': merge,
                        'parents': parents, 'common_ancestor': ancestor,
                        'actual_tree': actual_tree, 'reconstructed_tree': reconstructed_lines[0],
                        'automatic_merge_tree_exact': True,
                        'merge_is_ancestor_of_snapshot': True,
                        'changed_paths': changed, 'changed_path_count': len(changed),
                        'identical_at_merge_count': sum(at_merge),
                        'identical_at_final_count': sum(at_final),
                        'differences_requiring_inspection': differing})
        previous_merge = merge
    assert previous_merge == final, 'snapshot not reached'
    end_to_end = {p.decode() for p in git('diff', '--name-only', '-z', start, final).stdout.split(b'\0') if p}
    assert all_changed == end_to_end, ('full path universe mismatch', sorted(all_changed ^ end_to_end))
    result = {'schema': 'uqcf-integrated-tree-audit/v1',
              'repository': snapshot['repository'], 'snapshot_head': final,
              'baseline_before_merges': start,
              'first_parent_chain_complete': True,
              'canonical_end_to_end_path_universe_exact': True,
              'snapshot_sha256': hashlib.sha256(snapshot_bytes).hexdigest(),
              'git_version': out('--version'), 'merge_count': len(results),
              'path_identity_comparisons_per_destination': total_checks,
              'distinct_changed_paths': len(all_changed),
              'reconstructed_merge_trees_exact': all(r['automatic_merge_tree_exact'] for r in results),
              'all_changed_paths_identical_at_merge': all(not r['differences_requiring_inspection'] for r in results),
              'results': results,
              'limits': ['Exact Git integration and source/evidence preservation only.',
                         'No new scientific execution, mathematical review, native derivation, or numbered-stage recertification.',
                         'Any differing path requires explicit inspection before a preservation claim.']}
    Path(output_path).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: result[k] for k in ['snapshot_head', 'merge_count',
          'path_identity_comparisons_per_destination', 'distinct_changed_paths',
          'reconstructed_merge_trees_exact', 'all_changed_paths_identical_at_merge']}, indent=2))
    print(json.dumps([{'pr': r['pr'], 'paths': r['changed_path_count'],
                      'at_merge': r['identical_at_merge_count'],
                      'at_final': r['identical_at_final_count'],
                      'differences': r['differences_requiring_inspection']} for r in results], indent=2))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
