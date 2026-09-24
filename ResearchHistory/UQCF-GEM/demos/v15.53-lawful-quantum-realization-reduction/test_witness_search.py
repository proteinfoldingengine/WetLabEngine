"""v15.53 Task 5 RED: exhaustive producer-side witness search."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import realization_contract as rc
import realization_family as rf
import reduction as red
import equivalence as eq
import witness_search as ws

ROOT=Path(__file__).resolve().parents[4]

class WitnessSearchTests(unittest.TestCase):
    def setUp(self):
        self.c=rc.load_contract(ROOT)
        self.family=rf.enumerate_raw_realizations(self.c)

    def test_deterministic_frozen_search(self):
        a=ws.search_frozen_family(self.c)
        b=ws.search_frozen_family(self.c)
        self.assertEqual(a,b)
        json.dumps(a,sort_keys=True)

    def test_result_uses_exactly_allowed_primary_verdict(self):
        r=ws.search_frozen_family(self.c)
        self.assertIn(r["primary_verdict"],self.c["primary_verdicts"])
        self.assertEqual(r["candidate_count"],2)
        self.assertEqual(r["admissible_count"],2)

    def test_enumeration_order_does_not_change_scientific_verdict(self):
        a=ws.search_family(self.c,self.family)
        b=ws.search_family(self.c,tuple(reversed(self.family)))
        self.assertEqual(a["primary_verdict"],b["primary_verdict"])
        self.assertEqual(a["retained_fiber_count"],b["retained_fiber_count"])
        self.assertEqual(a["target_class_count"],b["target_class_count"])

    def test_candidate_id_relabeling_does_not_change_verdict(self):
        fam=deepcopy(self.family)
        fam[0]["id"]="renamed-A"; fam[1]["id"]="renamed-B"
        self.assertEqual(ws.search_family(self.c,fam)["primary_verdict"],ws.search_frozen_family(self.c)["primary_verdict"])

    def test_duplicate_candidate_injection_fails_family_closed(self):
        fam=list(deepcopy(self.family)); fam.append(deepcopy(fam[0]))
        r=ws.search_family(self.c,tuple(fam))
        self.assertEqual(r["primary_verdict"],"FAMILY_INVALID")
        self.assertIn("DUPLICATE_REALIZATION",r["reasons"])

    def test_positive_witness_if_present_is_real(self):
        r=ws.search_frozen_family(self.c)
        if r["primary_verdict"]=="CERTIFIED_FAMILY_OBSTRUCTION_WITNESS":
            self.assertIsNotNone(r["witness"])
            left=next(x for x in self.family if x["id"]==r["witness"]["left_id"])
            right=next(x for x in self.family if x["id"]==r["witness"]["right_id"])
            self.assertEqual(rf.check_admissibility(self.c,left)["status"],"ADMISSIBLE")
            self.assertEqual(rf.check_admissibility(self.c,right)["status"],"ADMISSIBLE")
            self.assertEqual(red.reduce_to_retained(self.c,left),red.reduce_to_retained(self.c,right))
            self.assertNotEqual(eq.canonical_class_key(self.c,left),eq.canonical_class_key(self.c,right))

    def test_no_witness_verdict_contains_no_pair(self):
        r=ws.search_frozen_family(self.c)
        if r["primary_verdict"]=="NO_WITNESS_IN_FROZEN_FAMILY":
            self.assertIsNone(r["witness"])

    def test_claim_firewall_and_scope_language(self):
        r=ws.search_frozen_family(self.c)
        self.assertEqual(r["scope"],"FROZEN_V15_53_FINITE_FAMILY_ONLY")
        self.assertEqual(r["source_correspondence"],"NOT_EVALUATED")
        self.assertEqual(r["Pillar_3"],"OPEN")
        self.assertFalse(r["physical_gravity"])
        forbidden=("universal impossibility","all quantum theories","gravity derived","physical source law established")
        text=r["interpretation"].lower()
        self.assertFalse(any(x in text for x in forbidden))

if __name__=="__main__":
    unittest.main()
