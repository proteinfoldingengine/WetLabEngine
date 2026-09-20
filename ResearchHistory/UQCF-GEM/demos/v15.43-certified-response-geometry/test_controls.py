from __future__ import annotations
import unittest
from dataclasses import replace
from fractions import Fraction as Q
from unittest.mock import patch
from test_carriers import manufactured_payload
from carriers import build_carrier
from projection import Field, FAMILY_KEYS


def control_inputs(L=5):
    payload = manufactured_payload(L)
    unit = build_carrier(payload)
    scaled = build_carrier(replace(payload, scale=Q(7,3), work=tuple(tuple(Q(7,3)*v for v in row) for row in payload.work)))
    fields = tuple(Field(family, root, tuple(Q(i == root)-Q(1,L*L) for i in range(L*L))) for family in FAMILY_KEYS for root in range(L*L))
    return unit, scaled, fields, tuple(replace(f, values=tuple(Q(7,3)*v for v in f.values)) for f in fields)


class ControlsTests(unittest.TestCase):
    def test_wrong_scale_is_rejected(self):
        from application_controls import check_response_controls
        unit, scaled, fields, _ = control_inputs()
        bad = tuple(replace(f, values=tuple(Q(2)*v for v in f.values)) for f in fields)
        with self.assertRaises(ValueError):
            check_response_controls(unit, scaled, fields, bad)

    def test_response_identities(self):
        from application_controls import check_response_controls
        for L in (5,7):
            receipt = check_response_controls(*control_inputs(L))
            self.assertEqual(receipt['scale_pairs'], 5*L*L)
            self.assertEqual(receipt['shift_cases'], 10*L*L)
            self.assertEqual(receipt['superpositions'], 10)

    def test_presentations_and_mutations(self):
        import presentation_checks as checks
        from application import evaluate_field
        for L in (5,7):
            carrier = build_carrier(manufactured_payload(L))
            raw = tuple(Q((i*i+3*i)%17,7) for i in range(L*L))
            mixed = tuple(v-sum(raw)/len(raw) for v in raw)
            for values in ((Q(0),)*(L*L), tuple(Q(i==0) for i in range(L*L)), mixed):
                receipt = checks.check_presentations(carrier, values)
                self.assertEqual(receipt['oriented_faces'], 8*L*L)
                self.assertEqual(receipt['gauge_presentations'], 8*L*L+1)
                self.assertGreater(receipt['relabel_cycle_rotations'], 0)
                self.assertGreater(receipt['relabel_cycle_reversals'], 0)
            good = evaluate_field(carrier, mixed)
            edge, matrix = good.transport.tangent_deltas[0]
            damaged = replace(good.transport, tangent_deltas=((edge, ((matrix[0][0]+1,matrix[0][1]), matrix[1])),)+good.transport.tangent_deltas[1:])
            with patch.object(checks, 'evaluate_field', return_value=replace(good, transport=damaged)):
                with self.assertRaises(ValueError): checks.check_presentations(carrier, mixed)
            with patch.object(checks, '_relabel_values', side_effect=lambda labels, values, names: values):
                with self.assertRaises(ValueError): checks.check_presentations(carrier, mixed)
            with patch.object(checks, 'cotangent_holonomy', side_effect=lambda b,t,c: checks.expanded(dict(t.baseline),dict(t.cotangent_pullback_deltas),c)):
                with self.assertRaises(ValueError): checks.check_presentations(carrier, mixed)

    def test_actual_carrier_controls(self):
        from application_controls import check_carrier_controls
        for L in (5,7):
            unit, scaled, _, _ = control_inputs(L)
            for carrier in (unit, scaled):
                receipt = check_carrier_controls(carrier)
                self.assertEqual(receipt['impulses'],L*L)
                self.assertEqual(receipt['basis_core_comparisons'],9*L*L+2)
                self.assertEqual(receipt['algebraically_certified_gauge_comparisons'],(L*L+2)*(8*L*L+1))
                self.assertEqual(receipt['local_linear_certificate']['gradient_basis_comparisons'],32)

if __name__ == '__main__': unittest.main()
