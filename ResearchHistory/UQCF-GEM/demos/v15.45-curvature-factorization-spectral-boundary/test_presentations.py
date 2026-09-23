from __future__ import annotations
import unittest
from presentations import check_all_presentations, reject_raw_mismatch
from evidence import actual_carriers


class PresentationFactorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.carriers = actual_carriers()

    def test_l5_complete_presentation_family(self):
        receipt = check_all_presentations(self.carriers[0])
        self.assertTrue(receipt["exact"])
        self.assertGreater(receipt["gauge_comparisons"], 0)
        self.assertGreater(receipt["orientation_comparisons"], 0)
        self.assertGreater(receipt["relabel_comparisons"], 0)

    def test_all_four_actual_carriers_scale_and_presentations(self):
        receipts = tuple(check_all_presentations(carrier) for carrier in self.carriers)
        self.assertEqual(tuple((r["L"], r["scale"]) for r in receipts),
                         ((5, "1"), (5, "7/3"), (7, "1"), (7, "7/3")))
        self.assertTrue(all(r["exact"] for r in receipts))

    def test_raw_mismatched_presentations_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "presentation_alignment_required"):
            reject_raw_mismatch(self.carriers[0])


if __name__ == "__main__":
    unittest.main()
