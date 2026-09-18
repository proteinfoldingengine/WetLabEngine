import unittest

import p8b_verify_artifact as v

TARGETS=("1VII","1L2Y","1UAO")
SEEDS=range(6)
MODES=("recovered_state_gate","fixed_step99_lockin","static_lockin","compaction_only")

def fixture(controller_ok=True):
    scores={
        "recovered_state_gate":0.8,
        "fixed_step99_lockin":0.4,
        "static_lockin":0.3,
        "compaction_only":0.2,
    }
    rows=[]
    for target in TARGETS:
        for seed in SEEDS:
            for mode in MODES:
                candidate=mode=="recovered_state_gate"
                rows.append({
                    "target":target,
                    "seed":str(seed),
                    "mode":mode,
                    "start_topk_native_contact_precision":"0.1",
                    "final_topk_native_contact_precision":str(scores[mode]),
                    "final_rg_ratio":"1.0",
                    "max_bond_length_drift_A":"1e-12",
                    "max_bond_angle_drift_rad":"1e-12",
                    "failed":"False",
                    "final_step":"2000",
                    "transitioned_to_lockin":str(controller_ok if candidate else False),
                    "lockin_active_steps":str(10 if candidate and controller_ok else 0),
                })
    return rows

class VerifierTests(unittest.TestCase):
    def test_exact_sign_flip_known_all_positive(self):
        p=v.exact_sign_flip_p([1.0]*18)
        self.assertEqual(2/(1<<18),p)

    def test_holm_three_known_case(self):
        self.assertEqual((0.03,0.08,0.2),v.holm_three((0.01,0.04,0.2)))

    def test_fixture_go(self):
        out=v.recompute(fixture())
        self.assertEqual("GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",out["decision"])
        self.assertTrue(all(out["conditions"].values()))

    def test_controller_condition_is_load_bearing(self):
        out=v.recompute(fixture(controller_ok=False))
        self.assertEqual("NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",out["decision"])
        self.assertFalse(out["conditions"]["all_candidate_trajectories_exercise_lockin"])

if __name__=="__main__":
    unittest.main()
