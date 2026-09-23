from __future__ import annotations
import sys
import unittest
import os
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CORE = HERE.parent / 'v15.42-duality-covariant-transport-repair'
sys.path.insert(0, str(CORE))
sys.path.insert(0, str(HERE))
from fixtures import periodic_square_input
from operator_types import canonical_bytes


def geometry_wire_from_fixture(L=5, scale='1'):
    labels, work, edges = periodic_square_input(L)
    factor = Fraction(scale)
    return {'L': L, 'scale': scale, 'labels': list(labels),
            'work': [[str(factor * x) for x in row] for row in work],
            'neighbors': [list(e) for e in sorted(tuple(sorted(e)) for e in edges)]}


class EvidenceTests(unittest.TestCase):
    def test_frozen_pins(self):
        from evidence import verify_evidence
        receipt = verify_evidence(ROOT)
        self.assertEqual(receipt['parent'], 'f121358c53ffdf88f9c0dcf351b850819ecb0298')
        self.assertEqual(len(receipt['closure']), 7)

    def test_pin_drift(self):
        from evidence import verify_evidence
        original = Path.read_bytes
        def altered(path):
            data = original(path)
            return data + b'\n' if path.name == 'transport.py' else data
        with patch.object(Path, 'read_bytes', altered), self.assertRaisesRegex(ValueError, 'blob mismatch'):
            verify_evidence(ROOT)

    def test_parent_mutation(self):
        from evidence import verify_evidence
        with patch('evidence._parent_changes', return_value=[('M', 'ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py')]), self.assertRaisesRegex(ValueError, 'parent mutation'):
            verify_evidence(ROOT)

    def test_manifest_duplicate_key(self):
        from evidence import parse_manifest
        with self.assertRaisesRegex(ValueError, 'duplicate_key'):
            parse_manifest(b'{"schema":1,"schema":2}')

    def test_module_wrong_origin(self):
        from bootstrap import load_pinned_modules, verify_origins
        modules = load_pinned_modules(ROOT)
        bogus = SimpleNamespace(__name__='carriers', __file__=str(HERE / 'carriers.py'))
        with self.assertRaisesRegex(ValueError, 'module origin mismatch'):
            verify_origins(ROOT, {'carriers': bogus})
        self.assertEqual(len(verify_origins(ROOT, modules)), 7)
        self.assertIs(load_pinned_modules(ROOT)['carriers'], modules['carriers'])

    def test_preloaded_same_name_module_is_rejected(self):
        from bootstrap import load_pinned_modules
        bogus = SimpleNamespace(__name__='carriers', __file__=str(HERE / 'carriers.py'))
        with patch.dict(sys.modules, {'carriers': bogus}):
            with self.assertRaisesRegex(ValueError, 'module origin mismatch'):
                load_pinned_modules(ROOT)

    def test_frozen_projection_geometry_inventory(self):
        from bootstrap import load_pinned_modules
        from operator_types import build_actual_carrier, load_geometry, validate_inventory
        parent = load_pinned_modules(ROOT)
        projection = parent['projection'].decode_projection(
            (HERE.parent / 'v15.43-certified-response-geometry/docs/INPUTS.json').read_bytes())
        geometries = tuple(load_geometry(canonical_bytes({
            'L': p.L, 'scale': str(p.scale), 'labels': list(p.labels),
            'work': [[str(v) for v in row] for row in p.work],
            'neighbors': [list(edge) for edge in p.neighbors]
        })) for p in projection.payloads)
        self.assertEqual(len(validate_inventory(geometries)), 4)
        for g in geometries:
            carrier = build_actual_carrier(g)
            self.assertEqual(len(carrier.complex.cycles), g.L*g.L)

    def test_operator_exposes_full_face_entry_contract(self):
        from operator_types import Geometry, Operator
        from dataclasses import fields
        self.assertEqual(tuple(f.name for f in fields(Geometry)), ('L','scale','labels','work','neighbors'))
        self.assertEqual(tuple(f.name for f in fields(Operator)), ('labels','cycles','entries'))

    def test_direct_carrier_construction_rejects_spoofed_import(self):
        from operator_types import load_geometry, build_actual_carrier
        geometry = load_geometry(canonical_bytes(geometry_wire_from_fixture()))
        fake = SimpleNamespace(__name__='carriers', __file__=str(HERE / 'spoofed_carriers.py'),
                               build_carrier=lambda payload: SimpleNamespace(
                                   complex=SimpleNamespace(labels=geometry.labels,
                                       neighbors=geometry.neighbors,
                                       cycles=((),) * (geometry.L*geometry.L))))
        with patch.dict(sys.modules, {'carriers': fake, 'projection': SimpleNamespace(__name__='projection', __file__=str(HERE / 'spoofed_projection.py'), Payload=lambda *args: args)}):
            with self.assertRaisesRegex(ValueError, 'module origin mismatch'):
                build_actual_carrier(geometry)

    def test_construction_runtime_denies_relative_symlink_and_process(self):
        from bootstrap import deny_archive_access, load_pinned_modules
        load_pinned_modules(ROOT)
        archive = HERE.parent / 'v15.43-certified-response-geometry/docs/RESULTS.json'
        with tempfile.TemporaryDirectory() as tmp:
            alias = Path(tmp) / 'alias.json'
            alias.symlink_to(archive)
            with deny_archive_access():
                for path in ('docs/RESULTS.json', str(archive), alias, HERE / 'operator_types.py'):
                    with self.subTest(path=path), self.assertRaisesRegex(PermissionError, 'construction'):
                        open(path, 'rb')
                    with self.subTest(path=path), self.assertRaisesRegex(PermissionError, 'construction'):
                        Path(path).read_bytes()
                with self.assertRaisesRegex(PermissionError, 'construction'):
                    os.open(alias, os.O_RDONLY)
                with self.assertRaisesRegex(PermissionError, 'construction'):
                    subprocess.run(['true'])
                with self.assertRaisesRegex(PermissionError, 'construction'):
                    os.system('true')

    def test_duplicate_geometry_key(self):
        from operator_types import load_geometry
        raw = canonical_bytes(geometry_wire_from_fixture())
        with self.assertRaisesRegex(ValueError, 'duplicate_key'):
            load_geometry(raw.replace(b'"L": 5', b'"L": 5, "L": 5', 1))

    def test_construction_rejects_response_source_target(self):
        from operator_types import load_geometry
        for key in ('fields', 'families', 'sources', 'targets', 'source', 'target'):
            wire = geometry_wire_from_fixture()
            wire[key] = []
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'unknown_field'):
                load_geometry(canonical_bytes(wire))

    def test_bool_float_noncanonical_fraction(self):
        from operator_types import load_geometry
        for key, value in [('L', True), ('L', 5.0), ('scale', '7/03'), ('scale', 1.0)]:
            wire = geometry_wire_from_fixture()
            wire[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                load_geometry(canonical_bytes(wire))
        for key, value in [('work', '1.0'), ('neighbors', True)]:
            wire = geometry_wire_from_fixture()
            if key == 'work': wire[key][0][1] = value
            else: wire[key][0][0] = value
            with self.assertRaises(ValueError): load_geometry(canonical_bytes(wire))

    def test_swapped_labels(self):
        from operator_types import load_geometry
        wire = geometry_wire_from_fixture()
        wire['labels'][0], wire['labels'][1] = wire['labels'][1], wire['labels'][0]
        with self.assertRaisesRegex(ValueError, 'invalid_label_order'):
            load_geometry(canonical_bytes(wire))

    def test_exact_four_carrier_inventory(self):
        from operator_types import load_geometry, validate_inventory
        items = tuple(load_geometry(canonical_bytes(geometry_wire_from_fixture(L, s)))
                      for L,s in ((5,'1'),(5,'7/3'),(7,'1'),(7,'7/3')))
        self.assertEqual(validate_inventory(items), items)
        for bad in (items[:3], items[::-1], items[:3] + items[:1]):
            with self.assertRaisesRegex(ValueError, 'carrier_inventory'): validate_inventory(bad)

    def test_actual_carrier_counts(self):
        from bootstrap import load_pinned_modules
        from operator_types import build_actual_carrier, load_geometry
        load_pinned_modules(ROOT)
        for L in (5,7):
            carrier = build_actual_carrier(load_geometry(canonical_bytes(geometry_wire_from_fixture(L))))
            self.assertEqual(len(carrier.complex.labels), L*L)
            self.assertEqual(len(carrier.complex.neighbors), 2*L*L)
            self.assertEqual(len(carrier.complex.cycles), L*L)

    def test_static_isolation_snippets(self):
        from bootstrap import check_pure_source
        for source in ('import oracle', 'from compare import read', 'import os',
                       'from pathlib import Path', 'open("docs/RESULTS.json")',
                       'import subprocess', 'from transport import construct_transport'):
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'isolation'):
                check_pure_source(source)
        check_pure_source('from fractions import Fraction\ndef f(x):\n    return Fraction(x)\n')

    def test_pure_import_cannot_reach_builtin_or_process_capabilities(self):
        from bootstrap import check_pure_source
        dangerous = (
            "from operator_types import __builtins__ as b\nb['__import__']('_io').FileIO('docs/RESULTS.json').read()",
            "from operator_types import Path as p\np('docs/RESULTS.json').read_bytes()",
            "from operator_types import os as system\nsystem.posix_spawn('/bin/true', ('true',), {})",
            "from exact_matrix import __builtins__ as b\nb['__import__']('os').posix_spawn('/bin/true', ('true',), {})",
            "import operator_types as types\ntypes.os.posix_spawn('/bin/true', ('true',), {})",
            "from fractions import Fraction as __builtins__",
            "__builtins__['__import__']('_io').FileIO('docs/RESULTS.json').read()",
        )
        for source in dangerous:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'isolation'):
                check_pure_source(source)
        check_pure_source('from operator_types import Geometry, Operator, Matrix\n')

    def test_verified_carrier_then_pure_guard_sequence(self):
        from bootstrap import deny_archive_access, load_pinned_modules
        from operator_types import build_actual_carrier, load_geometry
        load_pinned_modules(ROOT)
        carrier = build_actual_carrier(load_geometry(canonical_bytes(geometry_wire_from_fixture())))
        with deny_archive_access():
            self.assertEqual(len(carrier.complex.cycles), 25)
            self.assertEqual(Fraction(7, 3) * Fraction(3, 7), 1)
            with self.assertRaisesRegex(PermissionError, 'construction'):
                (HERE.parent / 'v15.43-certified-response-geometry/docs/RESULTS.json').read_bytes()

    def test_runtime_archive_reader_denied(self):
        from bootstrap import deny_archive_access, load_pinned_modules
        load_pinned_modules(ROOT)
        archive = HERE.parent / 'v15.43-certified-response-geometry/docs/RESULTS.json'
        with deny_archive_access():
            with self.assertRaisesRegex(PermissionError, 'construction'): archive.read_bytes()
            with self.assertRaisesRegex(PermissionError, 'construction'): open(archive, 'rb')

if __name__ == '__main__': unittest.main()
