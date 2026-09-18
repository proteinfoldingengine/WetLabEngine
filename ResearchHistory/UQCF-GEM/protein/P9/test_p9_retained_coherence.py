import copy
import csv
import io
import unittest

import numpy as np

import p9_retained_coherence as p9


class TestP9Contract(unittest.TestCase):
    def toy_rows(self):
        rows = []
        for seed in (0, 1):
            for step in (0, 100, 200, 300, 400, 499):
                rows.append({
                    "mode": "bridge_patch_v9",
                    "seed": str(seed),
                    "step": str(step),
                    "rmsd": str(9.0 - 0.002 * step + 0.1 * seed),
                    "energy": str(10.0 - 0.01 * step + seed),
                    "sigma_bridge": str(0.10 + 0.0002 * step + 0.01 * seed),
                    "closure_ready": str(0.02 + 0.0001 * step + 0.005 * seed),
                    "rg": str(50.0 - 0.02 * step + seed),
                })
        return rows

    def test_current_steps_and_future_map_are_frozen(self):
        self.assertEqual(p9.CURRENT_STEPS, (100, 200, 300, 400))
        self.assertEqual(p9.FUTURE_STEP, {100: 200, 200: 300, 300: 400, 400: 499})

    def test_feature_firewall_does_not_depend_on_rmsd(self):
        rows = self.toy_rows()
        changed = copy.deepcopy(rows)
        for row in changed:
            row["rmsd"] = str(float(row["rmsd"]) * 37.0 + 123.0)
        a = p9.build_predictor_rows(rows, target="toy")
        b = p9.build_predictor_rows(changed, target="toy")
        self.assertEqual(len(a), len(b))
        for ra, rb in zip(a, b):
            self.assertEqual(ra["key"], rb["key"])
            np.testing.assert_array_equal(ra["m0"], rb["m0"])
            np.testing.assert_array_equal(ra["m1"], rb["m1"])
            np.testing.assert_array_equal(ra["m2"], rb["m2"])

    def test_label_is_next_checkpoint_rmsd_change(self):
        rows = self.toy_rows()
        predictors = p9.build_predictor_rows(rows, target="toy")
        labels = p9.attach_labels(predictors, rows)
        row = next(x for x in labels if x["key"] == ("toy", 0, 100))
        expected = (9.0 - 0.002 * 200) - (9.0 - 0.002 * 100)
        self.assertAlmostEqual(row["y"], expected)

    def test_retained_features_use_only_prior_checkpoints(self):
        rows = self.toy_rows()
        predictors = p9.build_predictor_rows(rows, target="toy")
        row = next(x for x in predictors if x["key"] == ("toy", 0, 200))
        # M2 appends prior mean sigma, prior mean closure, prior sigma slope, prior closure slope.
        prior_sigma_mean = np.mean([0.10, 0.12])
        prior_closure_mean = np.mean([0.02, 0.03])
        self.assertAlmostEqual(row["m2"][-4], prior_sigma_mean)
        self.assertAlmostEqual(row["m2"][-3], prior_closure_mean)

    def test_transfer_split_never_mixes_targets(self):
        ua = p9.attach_labels(p9.build_predictor_rows(self.toy_rows(), "1UAO"), self.toy_rows())
        lb = p9.attach_labels(p9.build_predictor_rows(self.toy_rows(), "1L2Y"), self.toy_rows())
        train, test = p9.transfer_split(ua + lb, train_target="1UAO", test_target="1L2Y")
        self.assertTrue(train and test)
        self.assertEqual({r["key"][0] for r in train}, {"1UAO"})
        self.assertEqual({r["key"][0] for r in test}, {"1L2Y"})

    def test_go_requires_both_transfer_directions(self):
        good = {
            "rmse_m1": 1.0,
            "rmse_m2": 0.85,
            "delta": 0.15,
            "p_value": 0.01,
            "corr_m1": 0.2,
            "corr_m2": 0.5,
        }
        bad = dict(good, rmse_m2=0.95)
        self.assertEqual(
            p9.adjudicate({"1UAO_to_1L2Y": good, "1L2Y_to_1UAO": good}, True),
            "GO_RETAINED_COHERENCE_TRANSFER_SIGNAL",
        )
        self.assertEqual(
            p9.adjudicate({"1UAO_to_1L2Y": good, "1L2Y_to_1UAO": bad}, True),
            "NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL",
        )


if __name__ == "__main__":
    unittest.main()
