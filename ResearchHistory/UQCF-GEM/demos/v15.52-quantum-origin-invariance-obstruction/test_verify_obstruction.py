"""Task 4: independent audit, including regressions missed by Tasks 1--3."""
from copy import deepcopy
from itertools import permutations, product
from pathlib import Path
import unittest
import obstruction_contract as oc
import source_automorphisms as sa
import obstruction_witness as ow
try:
    import verify_obstruction as vo
except ModuleNotFoundError as exc:
    if exc.name != "verify_obstruction":
        raise
    vo = None


class IndependentAuditTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(vo, "Task 4 independent verifier is not implemented")
        self.c = deepcopy(oc.load_contract(Path(__file__).resolve().parents[4]))
        self.f = sa.frozen_fixture(self.c)
        self.a = sa.enumerate_automorphisms(self.c, self.f)
        self.w = ow.find_witness(self.c, self.f, self.a)

    def audit(self, **changes):
        args = dict(contract=self.c, fixture=self.f, automorphisms=self.a,
                    witness=self.w, selector_mode="deterministic")
        args.update(changes)
        return vo.verify_obstruction(**args)

    def test_label_only_candidate_is_not_a_quantum_certificate(self):
        r = self.audit()
        self.assertEqual(r["status"], "WITNESS_REJECTED")
        self.assertIn("LABEL_ONLY_QUANTUM_OUTPUTS", r["reasons"])
        self.assertFalse(r["quantum_origin_certified"])
        self.assertEqual(r["T2"], "NOT_CERTIFIED")

    def test_unregistered_semantics_cannot_be_self_attested(self):
        self.w["Q1"]["admissible"] = True
        self.w["Q2"]["admissible"] = True
        self.w["semantic_validator_passed"] = True
        r = self.audit()
        self.assertFalse(r["quantum_origin_certified"])
        self.assertIn("QUANTUM_ADMISSIBILITY_AND_REDUCTION_NOT_REGISTERED", r["reasons"])

    def test_arbitrary_structured_records_do_not_create_a_validator(self):
        for q in ("Q1", "Q2"):
            for k in vo.TARGET_FIELDS:
                self.w[q][k] = {"claimed_valid": True, "name": q}
        self.assertFalse(self.audit()["quantum_origin_certified"])

    def test_complete_automorphisms_recomputed_independently(self):
        self.assertEqual(vo.independent_automorphisms(self.f), self.a)
        self.assertEqual(self.a, ((0, 1, 2, 3),))
        self.assertEqual(self.audit()["nontrivial_source_automorphism_count"], 0)

    def test_empty_automorphism_packet_rejected(self):
        self.assertIn("AUTOMORPHISM_ACTION_INCOMPLETE", self.audit(automorphisms=())["reasons"])

    def test_duplicate_automorphism_packet_rejected(self):
        self.assertIn("DUPLICATE_AUTOMORPHISM", self.audit(automorphisms=self.a+self.a)["reasons"])

    def test_non_permutation_rejected(self):
        self.assertIn("INVALID_AUTOMORPHISM", self.audit(automorphisms=((0, 0, 2, 3),))["reasons"])

    def test_invented_automorphism_rejected(self):
        self.assertIn("AUTOMORPHISM_ACTION_INCOMPLETE", self.audit(automorphisms=self.a+((2,3,0,1),))["reasons"])

    def test_reported_automorphism_count_not_trusted(self):
        self.w["automorphism_count"] = 55
        self.assertIn("AUTOMORPHISM_COUNT_MISMATCH", self.audit()["reasons"])

    def test_shared_observable_dictionary_detected(self):
        self.assertIs(self.w["Q1"]["E_observables"], self.w["Q2"]["E_observables"])
        self.assertIn("ALIASED_OBSERVABLE_RECORDS", self.audit()["reasons"])

    def test_common_mode_corruption_detected_against_source(self):
        self.w["Q1"]["E_observables"]["object_count"] = 999
        self.assertIsNone(ow.find_separating_E_observable(self.c, self.w))
        r = self.audit()
        self.assertIn("SOURCE_OBSERVABLE_MISMATCH:Q1:object_count", r["reasons"])
        self.assertIn("SOURCE_OBSERVABLE_MISMATCH:Q2:object_count", r["reasons"])

    def test_one_sided_readout_difference_detected(self):
        self.w["Q2"]["E_observables"] = deepcopy(self.w["Q2"]["E_observables"])
        self.w["Q2"]["E_observables"]["object_count"] = 5
        r = self.audit()
        self.assertEqual(r["reported_separating_observables"], ["object_count"])
        self.assertFalse(r["quantum_origin_certified"])

    def test_missing_observable_rejected(self):
        del self.w["Q1"]["E_observables"]["object_count"]
        self.assertIn("OBSERVABLE_DOMAIN_MISMATCH:Q1", self.audit()["reasons"])

    def test_extra_observable_rejected(self):
        self.w["Q1"]["E_observables"]["target_dimension"] = 2
        self.assertIn("OBSERVABLE_DOMAIN_MISMATCH:Q1", self.audit()["reasons"])

    def test_observable_checklist_not_trusted(self):
        self.w["E_observables_checked"] = self.w["E_observables_checked"][:-1]
        self.assertIn("OBSERVABLE_CHECKLIST_MISMATCH", self.audit()["reasons"])

    def test_invented_gauge_rejected(self):
        self.c["quantum_equivalence"] = "ALL_LABELS_ARE_GAUGE"
        self.assertIn("FROZEN_CONTRACT_CHANGED", self.audit()["reasons"])

    def test_changed_observable_contract_rejected(self):
        self.c["E"]["observables"].append({"id":"made_up", "source_definable":True})
        self.assertIn("FROZEN_CONTRACT_CHANGED", self.audit()["reasons"])

    def test_target_selector_in_source_rejected(self):
        self.f["target_labels"] = ["Q_A"]
        self.assertIn("SOURCE_SCHEMA_INVALID", self.audit()["reasons"])

    def test_construction_manifest_not_accepted_with_target_input(self):
        self.w["construction_inputs"].append("target_dimension")
        self.assertIn("CONSTRUCTION_INPUTS_CHANGED", self.audit()["reasons"])

    def test_randomness_is_not_unique_recovery(self):
        self.assertIn("RANDOMIZED_OR_UNKNOWN_SELECTOR", self.audit(selector_mode="randomized")["reasons"])

    def test_identical_targets_rejected(self):
        self.w["Q2"] = deepcopy(self.w["Q1"])
        self.assertIn("IDENTICAL_TARGET_RECORDS", self.audit()["reasons"])

    def test_second_refinement_diagram_is_not_ignored(self):
        f = deepcopy(self.f)
        f["disjoint_composition"] = []
        self.assertEqual(len(vo.independent_automorphisms(f)), 2)
        f["refinement"].append(((0,0),(0,1)))
        self.assertEqual(len(vo.independent_automorphisms(f)), 1)
        self.assertEqual(len(sa.enumerate_automorphisms(self.c, f)), 2)

    def test_all_24_source_relabelings_preserve_audit_status(self):
        for p in permutations(range(4)):
            f = deepcopy(self.f)
            f["objects"] = [None]*4
            for i in range(4):
                f["objects"][p[i]] = self.f["objects"][i]
            for k in ("lineage", "dependency", "recoverability", "composition", "disjoint_composition"):
                f[k] = [tuple(p[i] for i in row) for row in self.f[k]]
            f["refinement"] = [tuple(tuple(p[i] for i in row) for row in diag) for diag in self.f["refinement"]]
            a = vo.independent_automorphisms(f)
            w = ow.find_witness(self.c, f, a)
            self.assertEqual(self.audit(fixture=f, automorphisms=a, witness=w)["status"], "WITNESS_REJECTED")
            self.assertEqual(len(a), 1)

    def test_json_replay_not_dependent_on_tuple_or_alias_identity(self):
        import json
        r = self.audit(witness=json.loads(json.dumps(self.w)))
        self.assertIn("LABEL_ONLY_QUANTUM_OUTPUTS", r["reasons"])
        self.assertFalse(r["quantum_origin_certified"])
        self.assertFalse(any(x.startswith("SOURCE_OBSERVABLE_MISMATCH") for x in r["reasons"]))

    def test_malformed_source_is_rejected(self):
        self.f["lineage"] = [(0, 44)]
        self.assertIn("SOURCE_SCHEMA_INVALID", self.audit()["reasons"])

    def test_claim_firewall_preserved(self):
        r = self.audit()
        self.assertEqual(r["source_correspondence"], "NOT_EVALUATED")
        self.assertEqual(r["Pillar_3"], "OPEN")
        self.assertFalse(r["physical_gravity"])
        self.assertEqual(r["quantum_witness_search"], "NOT_PERFORMED_NO_REGISTERED_REALIZATION_FAMILY")


class FactorizationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(vo, "Task 4 independent verifier is not implemented")

    def test_equal_readouts_distinct_targets_obstruct_uniform_recovery(self):
        r = vo.finite_factorization((0,0), ("A","B"))
        self.assertFalse(r["factorable"])
        self.assertEqual(r["conflict"], [0,1])

    def test_constant_choice_exists_but_is_not_recovery(self):
        readouts, targets = (0,0), ("A","B")
        choice = lambda _readout: "A"
        self.assertEqual(choice(readouts[0]), choice(readouts[1]))
        self.assertEqual(sum(choice(x)==t for x,t in zip(readouts,targets)), 1)
        self.assertFalse(vo.finite_factorization(readouts,targets)["factorable"])

    def test_coarse_target_can_be_recovered(self):
        self.assertTrue(vo.finite_factorization((0,0),("same_class","same_class"))["factorable"])

    def test_new_separating_datum_allows_recovery(self):
        self.assertTrue(vo.finite_factorization(((0,0),(0,1)),("A","B"))["factorable"])

    def test_empty_domain(self):
        self.assertTrue(vo.finite_factorization((),())["factorable"])

    def test_mismatched_domains_rejected(self):
        with self.assertRaises(ValueError):
            vo.finite_factorization((0,),())

    def test_exhaustive_1555_finite_cases_against_all_selectors(self):
        checked = 0
        for n in range(5):
            for obs in product(range(3), repeat=n):
                image = tuple(sorted(set(obs)))
                for targets in product(range(2), repeat=n):
                    exists = any(all(dict(zip(image,out))[obs[i]]==targets[i] for i in range(n))
                                 for out in product(range(2),repeat=len(image)))
                    self.assertEqual(vo.finite_factorization(obs,targets)["factorable"], exists)
                    checked += 1
        self.assertEqual(checked, 1555)


if __name__ == "__main__":
    unittest.main()
