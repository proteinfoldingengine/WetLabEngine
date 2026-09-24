"""v15.53 Task 6 RED: independent semantic verifier."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import realization_contract as rc
import realization_family as rf
import reduction as producer_reduction
import equivalence as producer_equivalence
import witness_search as producer_search
import verify_realization_obstruction as vr

ROOT = Path(__file__).resolve().parents[4]

def canonical_bytes(x):
    return (json.dumps(x,sort_keys=True,separators=(",",":"))+"\n").encode()

class IndependentVerifierTests(unittest.TestCase):
    def setUp(self):
        self.c=rc.load_contract(ROOT)
        self.family=vr.independent_frozen_family()

    def test_frozen_family_reconstructed_independently(self):
        self.assertEqual(
            json.loads(json.dumps(self.family)),
            json.loads(json.dumps(rf.enumerate_raw_realizations(self.c))),
        )

    def test_verifier_matches_producer_primary_verdict(self):
        p=producer_search.search_frozen_family(self.c)
        v=vr.verify_realization_obstruction(self.c)
        self.assertEqual(v["primary_verdict"],p["primary_verdict"])
        self.assertEqual(v["candidate_count"],p["candidate_count"])
        self.assertEqual(v["admissible_count"],p["admissible_count"])
        self.assertEqual(v["retained_fiber_count"],p["retained_fiber_count"])
        self.assertEqual(v["target_class_count"],p["target_class_count"])

    def test_producer_semantics_can_be_poisoned_without_affecting_verifier(self):
        originals=(rf.check_admissibility,producer_reduction.reduce_to_retained,
                   producer_equivalence.canonical_class_key,producer_search.search_frozen_family)
        try:
            rf.check_admissibility=lambda *a,**k: {"status":"ADMISSIBLE"}
            producer_reduction.reduce_to_retained=lambda *a,**k: {"poison":True}
            producer_equivalence.canonical_class_key=lambda *a,**k: ("poison",)
            producer_search.search_frozen_family=lambda *a,**k: {"primary_verdict":"VERIFICATION_FAILED"}
            a=vr.verify_realization_obstruction(self.c)
        finally:
            (rf.check_admissibility,producer_reduction.reduce_to_retained,
             producer_equivalence.canonical_class_key,producer_search.search_frozen_family)=originals
        b=vr.verify_realization_obstruction(self.c)
        self.assertEqual(a,b)

    def test_changed_composition_invalidates_family(self):
        fam=deepcopy(self.family); fam[0]["multiplication"][1][1]=1
        r=vr.verify_realization_obstruction(self.c,fam)
        self.assertEqual(r["primary_verdict"],"FAMILY_INVALID")
        self.assertIn("INADMISSIBLE_REALIZATION",r["reasons"])

    def test_recovery_typing_break_invalidates_family(self):
        fam=deepcopy(self.family); fam[0]["recovery_operations"].append(9)
        r=vr.verify_realization_obstruction(self.c,fam)
        self.assertEqual(r["primary_verdict"],"FAMILY_INVALID")

    def test_injected_target_class_is_rejected(self):
        fam=deepcopy(self.family); fam[0]["target_class"]="smuggled"
        r=vr.verify_realization_obstruction(self.c,fam)
        self.assertEqual(r["primary_verdict"],"FAMILY_INVALID")

    def test_copied_readout_is_rejected(self):
        fam=deepcopy(self.family); fam[0]["E_observables"]={"object_count":999}
        r=vr.verify_realization_obstruction(self.c,fam)
        self.assertEqual(r["primary_verdict"],"FAMILY_INVALID")

    def test_duplicate_candidate_rejected(self):
        fam=deepcopy(self.family); fam.append(deepcopy(fam[0]))
        r=vr.verify_realization_obstruction(self.c,fam)
        self.assertEqual(r["primary_verdict"],"FAMILY_INVALID")
        self.assertIn("DUPLICATE_REALIZATION",r["reasons"])

    def test_independent_reduction_separates_no_hidden_target(self):
        a=vr.independent_reduce(self.c,self.family[0])
        b=vr.independent_reduce(self.c,self.family[1])
        self.assertEqual(a,b)
        self.assertEqual(len(a["recoverability_relation"]),16)

    def test_independent_classes_distinguish_c4_v4(self):
        self.assertNotEqual(
            vr.independent_class_key(self.c,self.family[0]),
            vr.independent_class_key(self.c,self.family[1]),
        )

    def test_omitted_allowed_isomorphism_packet_detected(self):
        r=self.family[0]
        expected=vr.independent_isomorphisms(self.c,r,r)
        self.assertGreater(len(expected),0)
        audit=vr.verify_isomorphism_packet(self.c,r,r,expected[:-1])
        self.assertEqual(audit["status"],"INCOMPLETE_ISOMORPHISM_PACKET")

    def test_invented_isomorphism_packet_detected(self):
        r=self.family[0]
        expected=list(vr.independent_isomorphisms(self.c,r,r))
        bad=tuple(range(4))+tuple((1,0,2,3))
        if bad not in expected: expected.append(bad)
        audit=vr.verify_isomorphism_packet(self.c,r,r,tuple(expected))
        self.assertEqual(audit["status"],"INVALID_ISOMORPHISM_PACKET")

    def test_json_roundtrip_preserves_verdict(self):
        fam=json.loads(json.dumps(self.family))
        self.assertEqual(
            vr.verify_realization_obstruction(self.c,fam)["primary_verdict"],
            vr.verify_realization_obstruction(self.c)["primary_verdict"],
        )

    def test_double_replay_is_byte_identical(self):
        a=vr.verify_realization_obstruction(self.c)
        b=vr.verify_realization_obstruction(self.c)
        self.assertEqual(canonical_bytes(a),canonical_bytes(b))

    def test_claim_firewall(self):
        r=vr.verify_realization_obstruction(self.c)
        self.assertEqual(r["scope"],"FROZEN_V15_53_FINITE_FAMILY_ONLY")
        self.assertEqual(r["source_correspondence"],"NOT_EVALUATED")
        self.assertEqual(r["Pillar_3"],"OPEN")
        self.assertFalse(r["physical_gravity"])
        self.assertFalse(r["universal_quantum_origin_theorem"])
        self.assertFalse(r["physical_source_law"])

if __name__=="__main__":
    unittest.main()
