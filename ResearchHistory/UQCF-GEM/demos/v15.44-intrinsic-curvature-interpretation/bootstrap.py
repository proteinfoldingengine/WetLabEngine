"""Pinned parent module loading and geometry-construction access boundaries."""
from __future__ import annotations
import ast
import builtins
import importlib.util
import io
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from evidence import verify_evidence, git_blob

ORDER = ('exact_algebra','operational_complex','protocol_types','transport','holonomy','projection','carriers')


def verify_origins(root: Path, modules: dict) -> dict:
    pins = verify_evidence(root)['closure']
    if type(modules) is not dict or not set(modules) <= set(ORDER): raise ValueError('module origin mismatch')
    for name, module in modules.items():
        path = pins[name]['path']
        if (getattr(module, '__name__', None) != name or
                not isinstance(getattr(module, '__file__', None), str) or
                Path(module.__file__).resolve() != Path(path) or
                git_blob(Path(path).read_bytes()) != pins[name]['blob']):
            raise ValueError('module origin mismatch: ' + name)
    return {name: pins[name] for name in modules}


def load_pinned_modules(root: Path) -> dict:
    pins = verify_evidence(root)['closure']
    # Preflight all names before executing any module, so a spoofed already-loaded
    # dependency is never consulted by imports inside the frozen closure.
    for name in ORDER:
        if name in sys.modules:
            verify_origins(root, {name: sys.modules[name]})
    modules = {}
    for name in ORDER:
        if name not in sys.modules:
            spec = importlib.util.spec_from_file_location(name, pins[name]['path'])
            if spec is None or spec.loader is None: raise ValueError('module origin mismatch: ' + name)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            try: spec.loader.exec_module(module)
            except BaseException:
                del sys.modules[name]
                raise
        modules[name] = sys.modules[name]
    verify_origins(root, modules)
    return modules

# A pure module receives named algebraic values, never a module object whose
# globals expose import machinery or filesystem/process capabilities.
_ALLOWED_FROM = {
    '__future__': {'annotations'},
    'fractions': {'Fraction'},
    'dataclasses': {'dataclass', 'replace'},
    'typing': {'Any', 'Iterable', 'Sequence'},
    'collections': {'deque'},
    'itertools': {'product', 'combinations'},
    'math': {'isqrt'},
    'operator_types': {'Geometry', 'Operator', 'Matrix', 'canonical_bytes'},
    'exact_matrix': {'Matrix', 'Reduction', 'shape', 'matmul', 'transpose', 'add',
                     'identity', 'zeros', 'apply_matrix', 'rref', 'inverse',
                     'rank', 'nullspace', 'solve', 'scale'},
}
_DENIED_CALLS = {'open','exec','eval','compile','__import__','getattr','setattr',
                 'globals','locals','vars'}
_DENIED_ATTRS = {'open','read_bytes','read_text','write_bytes','write_text','run',
                 'Popen','system','posix_spawn','FileIO','exec_module','import_module'}

def check_pure_source(source: str) -> None:
    """Conservatively admit named pure values, never module/global capabilities."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            raise ValueError('isolation: module import')
        if isinstance(node, ast.ImportFrom):
            names = _ALLOWED_FROM.get(node.module)
            if node.level or names is None or any(
                    alias.name not in names or alias.asname is not None and
                    alias.asname.startswith('__') for alias in node.names):
                raise ValueError('isolation: import symbol')
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in _DENIED_CALLS:
                raise ValueError('isolation: call')
            if isinstance(node.func, ast.Attribute) and node.func.attr in _DENIED_ATTRS:
                raise ValueError('isolation: call')
        if isinstance(node, (ast.Name, ast.Attribute)):
            name = node.id if isinstance(node, ast.Name) else node.attr
            if name.startswith('__') and name.endswith('__') and name != '__future__':
                raise ValueError('isolation: dynamic access')
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.startswith('__') and node.value.endswith('__'):
            raise ValueError('isolation: dynamic key')

def check_pure_modules(directory: Path) -> None:
    for name in ('derive.py','kernel.py'):
        path = Path(directory) / name
        if not path.is_file(): raise ValueError('isolation: missing pure module ' + name)
        check_pure_source(path.read_text())

@contextmanager
def deny_archive_access():
    """Deny file opening and process creation throughout a pure construction phase.

    Invoke after pinned bootstrap, with all required modules already imported.
    This is a guard for normal Python APIs, not an OS security sandbox.
    """
    old_open, old_io_open = builtins.open, io.open
    old_os_open, old_system = os.open, os.system
    old_popen, old_run = subprocess.Popen, subprocess.run
    def denied(*args, **kwargs):
        raise PermissionError('construction filesystem/process access denied')
    try:
        builtins.open = io.open = os.open = os.system = denied
        subprocess.Popen = subprocess.run = denied
        yield
    finally:
        builtins.open, io.open = old_open, old_io_open
        os.open, os.system = old_os_open, old_system
        subprocess.Popen, subprocess.run = old_popen, old_run
