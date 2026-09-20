"""Ordered exact certification of the manufactured transport protocol only."""
from __future__ import annotations

import argparse
import ast
from dataclasses import asdict, is_dataclass
from enum import Enum
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

from controls import ControlExecutionError, ControlFamily, run_control_family
from evidence import git_blob_sha, verify_evidence
from fixtures import periodic_square_input
from operational_complex import (ConnectionStatus, construct_operational_complex,
                                 enumerate_baseline_connection)
from protocol_types import TransportManifest
from selection import SelectionAudit, audit_selection

ROOT = Path(__file__).resolve().parent
PARENT_HEAD = 'b9c5f29d8687a7dbc2af0595430aa73fbc5b8553'
VENDORED = {'exact_algebra.py':'c67ea42b61321469f7735ce589f2e729b241666a',
            'operational_complex.py':'8163beba8e52bc2a3a6d0c8cf59dd1257222f65c'}
PRODUCTION_FILES = tuple(ROOT / (name + '.py') for name in (
    'exact_algebra','operational_complex','evidence','fixtures','protocol_types',
    'selection','transport','holonomy','controls','protocol_gate'))
SCIENTIFIC_MODULES = frozenset(p.stem for p in PRODUCTION_FILES if p.stem not in ('evidence','protocol_gate'))
PURE_IMPORTS = frozenset(('__future__','collections','dataclasses','enum','fractions',
                          'functools','itertools','math','typing'))
PURE_SYMBOLS = {
    '__future__': {'annotations'}, 'collections': {'Counter','deque'},
    'dataclasses': {'dataclass','replace'}, 'enum': {'Enum'},
    'fractions': {'Fraction'}, 'functools': {'lru_cache'},
    'itertools': {'combinations','permutations','product'},
    'math': {'isqrt'}, 'typing': {'Callable','Iterable'},
}
FORBIDDEN = frozenset(('response_inputs','response_generation','source_target','coordinates',
    'spectrum','numpy','newton','einstein','observational','fit','svd','eig','pinv'))
DYNAMIC = frozenset(('__import__','importlib','eval','exec','compile','globals','locals','vars',
                     '__builtins__','__getattribute__','__globals__','__dict__','__subclasses__','__class__'))
IO_NAMES = frozenset(('open','read_text','read_bytes','write_text','write_bytes','input'))


def verify_firewall(paths=PRODUCTION_FILES):
    """Static capability audit, not a runtime query counter.

    Scientific modules have only reviewed local imports and pure stdlib imports;
    they have no filesystem/network/process imports or dynamic code loading.
    Evidence hashing and CLI I/O are separately restricted to gate modules.
    """
    for path in paths:
        path = Path(path)
        tree = ast.parse(path.read_text())
        scientific = path.stem in SCIENTIFIC_MODULES
        allowed = PURE_IMPORTS | SCIENTIFIC_MODULES
        if not scientific:
            allowed |= {'argparse','ast','json','pathlib','subprocess','sys','hashlib','evidence'}
        names = set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Name):
                names.add(node.id)
            elif isinstance(node,ast.Attribute):
                names.add(node.attr)
            elif isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                names.add(node.name)
            elif isinstance(node,ast.arg):
                names.add(node.arg)
            elif isinstance(node,ast.alias):
                names.update(node.name.split('.'))
                if node.asname:
                    names.add(node.asname)
            if isinstance(node,(ast.Import,ast.ImportFrom)):
                if scientific:
                    if isinstance(node,ast.Import):
                        raise ValueError('scientific imports must name reviewed symbols explicitly')
                    if node.module in PURE_SYMBOLS and any(
                            a.name not in PURE_SYMBOLS[node.module] for a in node.names):
                        raise ValueError('unreviewed standard-library symbol')
                modules = [a.name for a in node.names] if isinstance(node,ast.Import) else [node.module or '']
                if isinstance(node,ast.ImportFrom) and node.level:
                    raise ValueError('relative imports excluded from reviewed closure')
                for module in modules:
                    parts = set(module.split('.'))
                    names.update(parts)
                    if module not in allowed:
                        raise ValueError(f'unreviewed import in {path.name}: {module}')
                if any(a.name == '*' for a in node.names):
                    raise ValueError('wildcard imports excluded')
            if scientific and isinstance(node,ast.Constant) and isinstance(node.value,str):
                if node.value.startswith('__') and node.value.endswith('__'):
                    raise ValueError('reflective capability access excluded')
        rejected = names & (FORBIDDEN | DYNAMIC | (IO_NAMES if scientific else set()))
        if rejected:
            raise ValueError(f'prohibited capability in {path.name}: {sorted(rejected)}')
    return {'basis':'static AST identifier and import-capability audit; not runtime telemetry',
            'import_closure_verified':True,
            'reviewed_modules':[p.name for p in paths],
            'scientific_modules_have_no_io_or_dynamic_import_capability':True,
            'prohibited_input_queries':dict.fromkeys((
                'response_arrays_or_generation','source_targets_signs_or_labels',
                'historical_connection_or_curvature','spectra_fits_or_external_embeddings',
                'physical_or_observational_targets','floating_tolerances',
                'post_output_convention_selection'),0),
            'parent_ledger_access':'bytes hashed as evidence only; never parsed or queried'}


def verify_gate_evidence():
    result = verify_evidence()
    for name, expected in VENDORED.items():
        actual = git_blob_sha(ROOT/name)
        if actual != expected:
            raise ValueError(f'vendored evidence mismatch: {name}')
        result[name] = actual
    ancestry = subprocess.run(['git','merge-base','--is-ancestor',PARENT_HEAD,'HEAD'],
                              cwd=ROOT, capture_output=True, check=False)
    if ancestry.returncode != 0:
        raise ValueError('certified parent is not an ancestor of HEAD')
    result['parent_head'] = PARENT_HEAD
    result['parent_ancestry_verified'] = True
    return result


def verify_operational():
    records = []
    for L in (5,7):
        built = construct_operational_complex(*periodic_square_input(L))
        if built.status != ConnectionStatus.IDENTIFIABLE or built.complex is None:
            raise ValueError(f'L={L}: operational complex not identifiable')
        complex_ = built.complex
        baseline = enumerate_baseline_connection(complex_)
        if (baseline.status != ConnectionStatus.IDENTIFIABLE or baseline.connection is None
                or not baseline.connection.flat or len(complex_.labels) != L*L
                or len(complex_.cycles) != L*L or complex_.tangent_rank != 2):
            raise ValueError(f'L={L}: canonical substrate or baseline verification failed')
        records.append({'L':L,'vertices':len(complex_.labels),'faces':len(complex_.cycles),
                        'tangent_rank':complex_.tangent_rank,'baseline_flat':True,
                        'baseline_gauge_orbits':baseline.connection.gauge_orbit_count})
    return records


def _exact_json(value):
    if isinstance(value,Fraction):
        return str(value)
    if isinstance(value,Enum):
        return value.value
    if is_dataclass(value):
        return _exact_json(asdict(value))
    if isinstance(value,dict):
        return {str(k):_exact_json(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [_exact_json(v) for v in value]
    if value is None or type(value) in (str,int,bool):
        return value
    raise TypeError('ledger accepts exact values only')


def _ledger():
    result = dict.fromkeys(('scientific_breakthrough','response_geometry_applied',
        'source_target_constructed','source_correspondence_evaluated','physical_connection_derived',
        'physical_curvature_derived','stress_energy_derived','einstein_equations_derived',
        'continuum_limit_derived','spacetime_derived'),False)
    result.update(Pillar_3='OPEN',status='PROTOCOL_INVALID',failed_gate=None,
                  next_required_object='REPAIR_PROTOCOL_BEFORE_ANY_APPLICATION')
    return result


def _audit(evidence_verifier=verify_gate_evidence, operational_verifier=verify_operational,
           manifest_factory=TransportManifest.certified, selection_auditor=audit_selection,
           control_runner=run_control_family):
    result = _ledger()
    stage = 'evidence'
    try:
        result['evidence'] = _exact_json(evidence_verifier())
        result['construction_firewall'] = verify_firewall()
        stage = 'operational'
        result['operational'] = _exact_json(operational_verifier())
        stage = 'manifest'
        manifest = manifest_factory()
        if type(manifest) is not TransportManifest:
            raise TypeError('typed manifest required')
        manifest.validate()
        result['manifest'] = _exact_json(manifest)
        stage = 'selection'
        selection = selection_auditor()
        if type(selection) is not SelectionAudit or type(selection.identifiable) is not bool:
            raise TypeError('typed selection audit required')
        result['selection'] = _exact_json(selection)
        if not selection.identifiable:
            result.update(status='PROTOCOL_NOT_IDENTIFIABLE',failed_gate=stage,
                          next_required_object='ADD_FIRST_PRINCIPLES_SELECTION_AXIOM')
            return result
        stage = 'controls'
        controls = control_runner()
        if type(controls) is not ControlFamily:
            raise TypeError('typed control family required')
        summary = asdict(controls)
        summary['results'] = [dict(L=item.L, root=item.root, amplitude=item.amplitude,
                                   faces=len(item.curvatures), invariant_counts=item.invariant_counts,
                                   all_covariances_exact=item.all_covariances_exact)
                              for item in controls.results]
        result['controls'] = _exact_json(summary)
        if not controls.all_required_pass:
            order = ('covariance_exact','constant_null','l5_nonflat','every_root_equivalent',
                     'l7_holdout_nonflat','scale_exact','superposition_exact')
            first = next(name for name in order if getattr(controls,name) is not True)
            result['failed_gate'] = 'covariance' if first == 'covariance_exact' else first
            return result
    except Exception as error:
        result['failed_gate'] = error.stage if isinstance(error,ControlExecutionError) else stage
        result['error'] = f'{type(error).__name__}: {error}'
        return result
    result.update(status='TRANSPORT_PROTOCOL_CERTIFIED',
                  next_required_object='APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION')
    return result


def audit():
    return _audit()


def render_result(result):
    return json.dumps(_exact_json(result),sort_keys=True,indent=2) + '\n'


def write_result(path: Path):
    path = Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(render_result(audit()))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--out',type=Path)
    group.add_argument('--check',type=Path)
    args=parser.parse_args(argv)
    result=audit()
    rendered=render_result(result)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(rendered)
    if args.check:
        try:
            matches=args.check.read_bytes() == rendered.encode()
        except OSError:
            matches=False
        if not matches:
            print('canonical ledger mismatch',file=sys.stderr)
            return 1
    sys.stdout.write(rendered)
    return 0 if result['status'] == 'TRANSPORT_PROTOCOL_CERTIFIED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
