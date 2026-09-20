from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
CORE = HERE.parent / "v15.42-duality-covariant-transport-repair"
for location in (str(HERE), str(CORE)):
    if location not in sys.path:
        sys.path.insert(0, location)

from fixtures import periodic_square_input
from operational_complex import (BaselineConnectionAudit, ConnectionStatus,
                                 OperationalComplexAudit)
from projection import Payload


def manufactured_payload(L: int) -> Payload:
    labels, work, edges = periodic_square_input(L)
    neighbors = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    return Payload(L, Fraction(1), tuple(labels), tuple(tuple(row) for row in work),
                   neighbors, ())


class CarrierTests(unittest.TestCase):
    def test_identifies_manufactured_periodic_carrier(self):
        from carriers import Carrier, build_carrier

        carrier = build_carrier(manufactured_payload(5))
        self.assertIs(type(carrier), Carrier)
        self.assertEqual(carrier.complex.tangent_rank, 2)
        self.assertTrue(carrier.baseline.flat)
        self.assertEqual(carrier.baseline.gauge_orbit_count, 1)
        self.assertEqual(dict(carrier.receipt)["status"], "IDENTIFIABLE")

    def test_complete_graph_is_not_an_actual_carrier(self):
        from carriers import build_carrier

        payload = manufactured_payload(5)
        complete = tuple((i, j) for i in payload.labels for j in payload.labels if i < j)
        with self.assertRaisesRegex(ValueError, "neighbor_work_not_minimum"):
            build_carrier(Payload(payload.L, payload.scale, payload.labels,
                                  payload.work, complete, payload.fields))

    def test_nonidentification_retains_reason_and_stops_before_baseline(self):
        from carriers import build_carrier

        stopped = OperationalComplexAudit(ConnectionStatus.NOT_IDENTIFIABLE,
                                          "manufactured_stop", None)
        with patch("carriers.construct_operational_complex", return_value=stopped), \
             patch("carriers.enumerate_baseline_connection") as baseline:
            with self.assertRaisesRegex(ValueError, "manufactured_stop"):
                build_carrier(manufactured_payload(5))
        baseline.assert_not_called()

    def test_baseline_nonidentification_retains_reason(self):
        from carriers import build_carrier

        stopped = BaselineConnectionAudit(ConnectionStatus.NOT_IDENTIFIABLE,
                                          "baseline_manufactured_stop", None)
        with patch("carriers.enumerate_baseline_connection", return_value=stopped):
            with self.assertRaisesRegex(ValueError, "baseline_manufactured_stop"):
                build_carrier(manufactured_payload(5))

    def test_rejects_invalid_work_before_identification(self):
        from carriers import build_carrier

        payload = manufactured_payload(5)
        changed = [list(row) for row in payload.work]
        changed[0][1] = Fraction(2)
        with self.assertRaisesRegex(ValueError, "work_asymmetry"):
            build_carrier(Payload(payload.L, payload.scale, payload.labels,
                                  tuple(tuple(row) for row in changed),
                                  payload.neighbors, payload.fields))


if __name__ == "__main__":
    unittest.main()
