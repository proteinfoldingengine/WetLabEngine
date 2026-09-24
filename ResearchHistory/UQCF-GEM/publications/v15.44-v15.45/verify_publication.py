"""Verify a selective main-branch publication without rewriting scientific files.

This verifies copied Git objects and integration scope, not a new scientific
certification. Historical branch-ancestry checkers remain unmodified.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess


def _git(root: Path, *args: str) -> bytes:
    result = subprocess.run(['git', *args], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError('git_evidence_failure: ' + result.stderr.decode('utf-8', 'replace'))
    return result.stdout


def _path(value):
    if (type(value) is not str or not value or '\\' in value or
            PurePosixPath(value).is_absolute() or
            any(p in ('', '.', '..') for p in value.split('/'))):
        raise ValueError('unsafe_publication_path')
    return value


def _sha(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{40}', value) is None:
        raise ValueError('invalid_git_sha')
    return value


def _inventory(root, ref):
    records = {}
    for item in _git(root, 'ls-tree', '-r', '-z', '--full-tree', ref).split(b'\0'):
        if not item:
            continue
        metadata, path = item.split(b'\t', 1)
        mode, kind, sha = metadata.decode('ascii').split()
        records[path.decode('utf-8')] = (mode, kind, sha)
    return records


def verify(root: Path, manifest: dict, expected_head: str | None = None) -> dict:
    root = Path(root).resolve()
    keys = {'schema', 'base_main', 'source_head', 'snapshot_trees', 'pinned_files',
            'index_preservation', 'auxiliary_added'}
    if type(manifest) is not dict or set(manifest) != keys or manifest['schema'] != 'uqcf-main-publication-v1':
        raise ValueError('publication_manifest_schema')
    base = _sha(manifest['base_main'])
    _sha(manifest['source_head'])
    head = _git(root, 'rev-parse', 'HEAD').decode('ascii').strip()
    if expected_head is not None and head != _sha(expected_head):
        raise ValueError('head_mismatch')
    _git(root, 'merge-base', '--is-ancestor', base, head)
    if _git(root, 'diff', '--name-only', 'HEAD', '--').strip():
        raise ValueError('tracked_worktree_changed')
    for name in ('snapshot_trees', 'pinned_files', 'index_preservation'):
        if type(manifest[name]) is not dict or not manifest[name]:
            raise ValueError('empty_or_invalid_manifest_inventory')
    roots = {_path(p): _sha(s) for p, s in manifest['snapshot_trees'].items()}
    pins = {_path(p): _sha(s) for p, s in manifest['pinned_files'].items()}
    indices = {}
    for path, item in manifest['index_preservation'].items():
        if type(item) is not dict or set(item) != {'archive', 'blob'}:
            raise ValueError('index_preservation_schema')
        indices[_path(path)] = (_path(item['archive']), _sha(item['blob']))
    aux = manifest['auxiliary_added']
    if type(aux) is not list or len(aux) != len(set(aux)):
        raise ValueError('auxiliary_inventory')
    aux = {_path(path) for path in aux}
    before, after = _inventory(root, base), _inventory(root, head)
    allowed_exact = set(pins) | set(indices) | {a for a, _ in indices.values()} | aux
    changed = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
    if not changed:
        raise ValueError('empty_publication')
    for path in sorted(changed):
        in_snapshot = any(path.startswith(prefix + '/') for prefix in roots)
        if path not in allowed_exact and not in_snapshot:
            raise ValueError('outside_publication_scope: ' + path)
        if path in before and path not in indices:
            raise ValueError('existing_main_file_changed: ' + path)
        if path not in after:
            raise ValueError('publication_deletion: ' + path)
    for path, (archive, sha) in indices.items():
        want = ('100644', 'blob', sha)
        if before.get(path) != want or after.get(archive) != want:
            raise ValueError('index_archive_mismatch: ' + path)
        if path not in after or after[path][:2] != ('100644', 'blob'):
            raise ValueError('missing_publication_index')
    snapshot_count = 0
    for path, sha in roots.items():
        actual = _git(root, 'rev-parse', head + ':' + path).decode('ascii').strip()
        if actual != sha:
            raise ValueError('snapshot_tree_mismatch: ' + path)
        children = [entry for p, entry in after.items() if p.startswith(path + '/')]
        if not children or any(mode != '100644' or kind != 'blob' for mode, kind, _ in children):
            raise ValueError('invalid_snapshot_entries')
        snapshot_count += len(children)
    for path, sha in pins.items():
        if after.get(path) != ('100644', 'blob', sha):
            raise ValueError('pin_mismatch: ' + path)
    if any(path not in after or after[path][:2] != ('100644', 'blob') for path in aux):
        raise ValueError('missing_auxiliary_file')
    return {'status': 'PUBLICATION_INTEGRITY_VERIFIED', 'head': head,
            'base_main': base, 'source_head': manifest['source_head'],
            'snapshot_files': snapshot_count, 'pinned_files': len(pins),
            'historical_indices_preserved': len(indices),
            'changed_files': len(changed), 'unrelated_main_files_changed': 0,
            'scientific_files_modified': 0, 'new_scientific_certification': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', type=Path, default=Path(__file__).with_name('MANIFEST.json'))
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--expected-head')
    args = parser.parse_args()
    receipt = verify(args.root, json.loads(args.manifest.read_text('utf-8')), args.expected_head)
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
