import unittest
from dataclasses import replace
from fractions import Fraction as Q
from operator_types import Operator
from exact_matrix import apply_matrix, identity, zeros
from kernel import analyze_kernel, verify_kernel
from test_operator import actual_geometries
from operator_types import build_actual_carrier
from bootstrap import check_pure_modules, deny_archive_access
from derive import derive_operator
from oracle import reference_operator
from pathlib import Path


def operator_from_matrix(entries):
    # Deliberately algebra-only: production geometry has 4F rows.
    return Operator(tuple(range(len(entries[0]))), (), entries)


class KernelTests(unittest.TestCase):
    def test_kernel_completeness_and_centering(self):
        a = operator_from_matrix(((Q(1), Q(-1), Q(0)),))
        k = analyze_kernel(a)
        self.assertEqual((k.rank, k.nullity, k.pivots), (1, 2, (0,)))
        self.assertEqual(k.null_basis, ((Q(1), Q(0)), (Q(1), Q(0)), (Q(0), Q(1))))
        self.assertEqual(k.image_basis, ((Q(1),),))
        self.assertEqual(k.projector, ((Q(1, 2), Q(1, 2), Q(0)),
                                       (Q(1, 2), Q(1, 2), Q(0)),
                                       (Q(0), Q(0), Q(1))))
        self.assertEqual(k.centered_basis, ((Q(-1, 2),), (Q(-1, 2),), (Q(1),)))
        self.assertTrue(verify_kernel(a, k))
        with self.assertRaises(ValueError):
            verify_kernel(a, replace(k, null_basis=tuple(row[:-1] for row in k.null_basis)))

    def test_rank_forgery_with_valid_kernel_vectors_rejected(self):
        a = operator_from_matrix(((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0))))
        k = analyze_kernel(a)
        forged = replace(k, rank=1, nullity=2)
        with self.assertRaises(ValueError): verify_kernel(a, forged)
        with self.assertRaises(ValueError):
            verify_kernel(a, replace(k, image_basis=((Q(1), Q(1)), (Q(1), Q(1)))))

    def test_zero_matrix_and_full_column_rank(self):
        zero = operator_from_matrix(((Q(0), Q(0)), (Q(0), Q(0))))
        k = analyze_kernel(zero)
        self.assertEqual((k.rank, k.nullity, k.pivots), (0, 2, ()))
        self.assertEqual(k.projector, ((Q(1), Q(0)), (Q(0), Q(1))))
        self.assertTrue(verify_kernel(zero, k))
        full = operator_from_matrix(((Q(1), Q(0)), (Q(0), Q(1))))
        f = analyze_kernel(full)
        self.assertEqual((f.rank, f.nullity, f.null_basis), (2, 0, ((), ())))
        self.assertEqual(f.projector, zeros(2, 2))
        self.assertEqual(f.centered_basis, ((), ()))
        self.assertTrue(verify_kernel(full, f))

    def test_row_operation_record_detects_tampering(self):
        a = operator_from_matrix(((Q(0), Q(2)), (Q(1), Q(1))))
        k = analyze_kernel(a)
        self.assertTrue(verify_kernel(a, k))
        with self.assertRaises(ValueError):
            verify_kernel(a, replace(k, reduction=replace(k.reduction, operations=())))
        with self.assertRaises(ValueError):
            verify_kernel(a, replace(k, projector=identity(2)))

    def test_all_four_actual_carriers_oracle_vectors(self):
        for geometry in actual_geometries():
            with self.subTest(L=geometry.L, scale=geometry.scale):
                carrier = build_actual_carrier(geometry)
                check_pure_modules(Path(__file__).resolve().parent)
                with deny_archive_access():
                    operator = derive_operator(carrier)
                    certificate = analyze_kernel(operator)
                    self.assertTrue(verify_kernel(operator, certificate))
                oracle = reference_operator(carrier)
                self.assertEqual(oracle.entries, operator.entries)
                n = len(operator.labels)
                self.assertEqual(apply_matrix(oracle.entries, (Q(1),)*n), (Q(0),)*len(oracle.entries))
                for col in range(certificate.nullity):
                    vector = tuple(row[col] for row in certificate.null_basis)
                    self.assertEqual(apply_matrix(oracle.entries, vector), (Q(0),)*len(oracle.entries))
                print('observed kernel', geometry.L, geometry.scale,
                      'rank', certificate.rank, 'nullity', certificate.nullity,
                      'centered_nullity', len(certificate.centered_basis[0]))


if __name__ == '__main__': unittest.main()
