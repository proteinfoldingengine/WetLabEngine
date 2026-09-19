import ast
import inspect
import json
from fractions import Fraction
from pathlib import Path
import unittest

from geometry_specificity_gate import ALLOWED_GATE_STATUSES, CONTROL_KEYS, audit, canonical_json, classify_gate, compare_geometry, next_required_object_for_status
from response_generation import deterministic_permutation
from response_geometry import construct_response_geometry, metric_passes
from incidence_target import IncidenceTarget, construct_incidence_target


class GlobalBalanceGeometrySpecificityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.result = audit()

    def test_evidence_and_exact_generation_protocol(self):
        self.assertTrue(self.result["evidence_verified"])
        self.assertTrue(self.result["canonical_augmentation_isomorphism_exact"])
        self.assertTrue(self.result["all_response_equations_exact"])
        for size in self.result["size_audits"]:
            L = size["L"]
            self.assertEqual(size["generation"]["B2_rank"], L*L-1)
            self.assertTrue(size["generation"]["B2_kernel_constant_line"])
            self.assertEqual(size["source_count_per_family"], L*L)

    def test_response_geometry_is_blind_exact_and_total(self):
        self.assertTrue(self.result["input_separation"]["response_constructor_blind"])
        self.assertTrue(self.result["all_required_pairs_evaluated"])
        self.assertTrue(self.result["all_required_ordered_triples_evaluated"])
        self.assertEqual(tuple(inspect.signature(construct_response_geometry).parameters), ("labels", "sources", "responses"))
        sources = ((1,0,0),(0,1,0),(0,0,1))
        def responses_for(distances):
            out = [[Fraction(0) for _ in range(3)] for _ in range(3)]
            for (i,j), distance in distances.items(): out[i][j] = out[j][i] = -Fraction(distance,2)
            return tuple(tuple(row) for row in out)
        self.assertTrue(metric_passes(construct_response_geometry((0,1,2), sources, responses_for({(0,1):1,(1,2):1,(0,2):2}))))
        bad = construct_response_geometry((0,1,2), sources, responses_for({(0,1):1,(1,2):1,(0,2):3}))
        self.assertTrue(bad.separated); self.assertFalse(bad.triangle)
        self.assertFalse(construct_response_geometry((0,1,2), sources, ((0,0,0),)*3).separated)
        with self.assertRaises(TypeError): construct_response_geometry((0,1), ((True,),(0,)), ((1,),(0,)))
        class Hostile:
            labels = (0,1); sources = ((1,0),(0,1)); responses = ((1,0),(0,1))
            def __getattr__(self, name):
                if name in {"B1","B2","A","D","translations","D4","coordinates","distances","spectrum","candidate_key"}: raise AssertionError(name)
                raise AttributeError(name)
        hostile = Hostile()
        self.assertTrue(metric_passes(construct_response_geometry(hostile.labels, hostile.sources, hostile.responses)))

    def test_incidence_target_is_blind_four_regular_and_connected(self):
        self.assertTrue(self.result["input_separation"]["target_constructor_blind"])
        self.assertTrue(self.result["all_targets_four_regular"]); self.assertTrue(self.result["all_targets_connected"])
        self.assertEqual(tuple(inspect.signature(construct_incidence_target).parameters), ("signed_support",))
        path = construct_incidence_target(((1,-1,0),(0,1,-1)))
        disconnected = construct_incidence_target(((1,-1,0,0),(0,0,1,-1)))
        self.assertEqual(path.distances[0], (0,1,2)); self.assertFalse(disconnected.connected); self.assertIsNone(disconnected.distances[0][2])
        class HostileSupport:
            rows = ((1,-1,0),(0,1,-1))
            def __len__(self): return len(self.rows)
            def __getitem__(self, index): return self.rows[index]
            def __getattr__(self, name):
                if name in {"A","D","responses","response_pairings","translations","D4","coordinates","precomputed_distances"}: raise AssertionError(name)
                raise AttributeError(name)
        self.assertTrue(construct_incidence_target(HostileSupport()).connected)
        for size in self.result["size_audits"]: self.assertEqual(size["target_edge_count"], 2*size["L"]*size["L"])

    def test_orientation_additivity_covariance_and_relabeling(self):
        self.assertTrue(self.result["all_orientation_rays_exact"]); self.assertTrue(self.result["all_additivity_exact"])
        self.assertTrue(self.result["all_translation_D4_covariance_exact"]); self.assertTrue(self.result["all_relabeling_equivariant"])
        for L in (5,7,9,11):
            p = deterministic_permutation(L); inverse = tuple(p.index(i) for i in range(L*L))
            self.assertEqual(tuple(inverse[p[i]] for i in range(L*L)), tuple(range(L*L)))

    def test_projective_scale_and_holdout_rules(self):
        self.assertEqual(self.result["projective_scales"], ["1","7/3"]); self.assertTrue(self.result["all_scale_verdicts_identical"])
        self.assertEqual(self.result["holdout_size"], 11); self.assertTrue(self.result["holdout_formula_unchanged"])

    def test_controls_and_mechanical_correspondence(self):
        self.assertEqual(tuple(self.result["control_keys"]), CONTROL_KEYS)
        self.assertTrue(self.result["matched_controls_structurally_admissible"]); self.assertTrue(self.result["matched_controls_metric_protocol"])
        self.assertTrue(self.result["mechanical_correspondence_rule_applied"]); self.assertTrue(self.result["protocol_valid"])
        self.assertTrue(any(not row["metric"]["passes"] for size in self.result["size_audits"] for row in size["rows"] if row["family"] in ("DIRECT_INHERITANCE","ONE_INCIDENCE_TRANSPORT")))
        geometry = construct_response_geometry((0,1,2), ((1,0,0),(0,1,0),(0,0,1)), ((1,0,0),(0,1,0),(0,0,1)))
        target = IncidenceTarget((0,1,2), geometry.neighbors, (2,2,2), True, ((0,1,1),(1,0,1),(1,1,0)))
        comparison = compare_geometry(geometry, target)
        self.assertTrue(comparison.metric_passes and comparison.neighbors_equal and comparison.distances_equal)

    def test_status_and_next_object_are_mechanical(self):
        self.assertIn(self.result["status"], ALLOWED_GATE_STATUSES)
        self.assertEqual(self.result["next_required_object"], next_required_object_for_status(self.result["status"]))
        self.assertEqual(self.result["status"], classify_gate(self.result["protocol_valid"], self.result["canonical_all_sizes"], self.result["control_all_sizes"]))
        controls = {key: False for key in CONTROL_KEYS}
        self.assertEqual(classify_gate(False,True,controls), "RESPONSE_GEOMETRY_PROTOCOL_INVALID")
        self.assertEqual(classify_gate(True,False,controls), "NO_RESPONSE_DERIVED_GEOMETRY")
        generic = dict(controls); generic[CONTROL_KEYS[0]] = True
        self.assertEqual(classify_gate(True,True,generic), "GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY")
        self.assertEqual(classify_gate(True,True,controls), "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES")
        for status in ALLOWED_GATE_STATUSES: self.assertIsInstance(next_required_object_for_status(status), str)

    def test_construction_and_interpretation_firewalls(self):
        self.assertTrue(all(value == 0 for value in self.result["construction_firewall"].values()))
        expected = {"new_source_semantics_axiom_inherited":True,"new_global_balance_response_axiom_inherited":True,"source_axiom_derived_from_frozen_ontology":False,"response_axiom_derived_from_frozen_ontology":False,"physical_metric_derived":False,"spacetime_derived":False,"physical_gravity_derived":False,"continuum_limit_derived":False,"einstein_equations_derived":False,"uses_pruning":False,"uses_entropy":False,"uses_physical_time":False,"scientific_breakthrough":False,"Pillar_3":"OPEN"}
        self.assertEqual({key:self.result[key] for key in expected}, expected)
        for filename, allowed, forbidden in (("response_geometry.py",{"dataclasses","fractions","itertools","__future__"},{"B1","B2","A","D","translations","D4","coordinates","distances","spectrum","candidate_key","inverse","solve","numpy"}),("incidence_target.py",{"collections","dataclasses","itertools","__future__"},{"A","D","responses","response_pairings","translations","D4","coordinates","precomputed_distances"})):
            tree = ast.parse(Path(filename).read_text()); imports = {a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names} | {n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}
            loaded = {n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
            self.assertLessEqual(imports, allowed); self.assertTrue(loaded.isdisjoint(forbidden))

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text(); self.assertEqual(committed, canonical_json(self.result)); self.assertEqual(json.loads(committed), self.result)
        def contains_float(value):
            if isinstance(value,float): return True
            if isinstance(value,dict): return any(contains_float(item) for item in value.values())
            if isinstance(value,(list,tuple)): return any(contains_float(item) for item in value)
            return False
        self.assertFalse(contains_float(self.result))


if __name__ == "__main__": unittest.main()
