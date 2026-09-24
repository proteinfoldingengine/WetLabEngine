"""Fixed evidence pins; repository files cannot expand the executable closure."""
from __future__ import annotations
import json
import subprocess
from hashlib import sha1, sha256
from pathlib import Path

PARENT = 'f121358c53ffdf88f9c0dcf351b850819ecb0298'
PARENT_TREE = '7c4fba405790be9efd320795485c0e7845c6eeb6'
MANIFEST_SHA256 = '5c5c4fea188910aa73785df941de0809993b6d6c25011f25d7ff4cdbfb5cf7c0'
DEMO = Path('ResearchHistory/UQCF-GEM/demos/v15.44-intrinsic-curvature-interpretation')

def git_blob(raw: bytes) -> str:
    return sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def _unique(pairs):
    output = {}
    for key, value in pairs:
        if key in output: raise ValueError('duplicate_key')
        output[key] = value
    return output

def parse_manifest(raw: bytes) -> dict:
    try: manifest = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique)
    except (UnicodeDecodeError, json.JSONDecodeError) as error: raise ValueError('invalid_manifest') from error
    if type(manifest) is not dict or set(manifest) != {'schema','parent','parent_tree','spec','inputs','results','closure'}:
        raise ValueError('manifest_schema')
    return manifest

def _git(root, *args):
    result = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True)
    if result.returncode: raise ValueError('git evidence failure: ' + result.stderr.strip())
    return result.stdout.strip()

def _parent_changes(root):
    result = _git(root, 'diff', '--name-status', PARENT, '--')
    return [tuple(line.split('\t', 1)) for line in result.splitlines() if line]

def _checked_item(root, item):
    if type(item) is not dict or set(item) != {'path','blob'} or any(type(x) is not str for x in item.values()):
        raise ValueError('invalid_pin')
    path = (root / item['path']).resolve(strict=True)
    if root not in path.parents or path.is_dir(): raise ValueError('pin path escape')
    actual = git_blob(path.read_bytes())
    if actual != item['blob']: raise ValueError('blob mismatch: ' + item['path'])
    return {'path': str(path), 'blob': actual}

def verify_evidence(root: Path) -> dict:
    root = Path(root).resolve(strict=True)
    raw = (root / DEMO / 'dependencies.json').read_bytes()
    manifest = parse_manifest(raw)
    if sha256(raw).hexdigest() != MANIFEST_SHA256 or manifest['schema'] != 'uqcf-v1544-dependencies-v1':
        raise ValueError('manifest pin drift')
    if manifest['parent'] != PARENT or manifest['parent_tree'] != PARENT_TREE:
        raise ValueError('parent pin drift')
    if _git(root, 'rev-parse', PARENT+'^{tree}') != PARENT_TREE:
        raise ValueError('parent tree mismatch')
    _git(root, 'merge-base', '--is-ancestor', PARENT, 'HEAD')
    prefix = DEMO.as_posix() + '/'
    allowed = {'docs/superpowers/specs/2026-09-22-v1544-intrinsic-curvature-interpretation-design.md',
               'docs/superpowers/plans/2026-09-22-v1544-intrinsic-curvature-interpretation-implementation.md',
               '.github/workflows/uqcf-v1544-intrinsic-curvature-interpretation.yml'}
    for status, path in _parent_changes(root):
        if status != 'A' or not (path.startswith(prefix) or path in allowed):
            raise ValueError('parent mutation: ' + path)
    receipt = {'schema': manifest['schema'], 'parent': PARENT, 'parent_tree': PARENT_TREE}
    for name in ('spec','inputs','results'):
        receipt[name] = _checked_item(root, manifest[name])
    if set(manifest['closure']) != {'exact_algebra','operational_complex','protocol_types','transport','holonomy','projection','carriers'}:
        raise ValueError('closure inventory')
    receipt['closure'] = {name: _checked_item(root, pin) for name,pin in manifest['closure'].items()}
    return receipt
