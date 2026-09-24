import sys
import unittest
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
from bootstrap import check_pure_modules, deny_archive_access, load_pinned_modules
from operator_types import build_actual_carrier, canonical_bytes, load_geometry, validate_inventory
from derive import derive_operator, require_equal
from oracle import reference_operator
sys.path.insert(1, str(HERE.parent / 'v15.42-duality-covariant-transport-repair'))
from fixtures import periodic_square_input


def fixture_carrier(L, scale='1'):
    labels, work, edges = periodic_square_input(L)
    factor = Q(scale)
    wire = {'L': L, 'scale': scale, 'labels': list(labels),
            'work': [[str(factor * x) for x in row] for row in work],
            'neighbors': [list(e) for e in sorted(tuple(sorted(e)) for e in edges)]}
    return build_actual_carrier(load_geometry(canonical_bytes(wire)))


def replace_entry(operator, row=1, column=0, increment=Q(1)):
    rows = [list(values) for values in operator.entries]
    rows[row][column] += increment
    return replace(operator, entries=tuple(tuple(values) for values in rows))


def actual_geometries():
    parent = load_pinned_modules(ROOT)
    raw = (HERE.parent / 'v15.43-certified-response-geometry/docs/INPUTS.json').read_bytes()
    projection = parent['projection'].decode_projection(raw)
    geometries = tuple(load_geometry(canonical_bytes({
        'L': p.L, 'scale': str(p.scale), 'labels': list(p.labels),
        'work': [[str(value) for value in row] for row in p.work],
        'neighbors': [list(edge) for edge in p.neighbors]
    })) for p in projection.payloads)
    return validate_inventory(geometries)


class OperatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_pinned_modules(ROOT)

    def test_complete_basis_agreement(self):
        c = fixture_carrier(5)
        self.assertEqual(derive_operator(c), reference_operator(c))

    def test_reject_changed_coefficient(self):
        c = fixture_carrier(5)
        a = derive_operator(c)
        damaged = replace_entry(a, row=1, column=0, increment=Q(1))
        with self.assertRaisesRegex(ValueError, 'operator_mismatch'):
            require_equal(damaged, reference_operator(c))

    def test_all_four_actual_carriers_every_column(self):
        for geometry in actual_geometries():
            with self.subTest(L=geometry.L, scale=geometry.scale):
                c = build_actual_carrier(geometry)
                check_pure_modules(HERE)
                with deny_archive_access():
                    actual = derive_operator(c)
                expected = reference_operator(c)
                self.assertEqual(actual.labels, expected.labels)
                self.assertEqual(actual.cycles, expected.cycles)
                self.assertEqual(len(actual.entries), 4*geometry.L*geometry.L)
                self.assertTrue(all(len(row) == geometry.L*geometry.L for row in actual.entries))
                for row in range(4*geometry.L*geometry.L):
                    for col in range(geometry.L*geometry.L):
                        self.assertEqual(actual.entries[row][col], expected.entries[row][col],
                                         (geometry.L, geometry.scale, row, col))


if __name__ == '__main__': unittest.main()
