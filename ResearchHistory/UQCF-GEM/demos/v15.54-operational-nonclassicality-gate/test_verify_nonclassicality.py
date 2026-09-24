"""v15.54 Task 7 RED: independent semantic certification."""
from copy import deepcopy
from pathlib import Path
import json, unittest
import nonclassicality_contract as nc
import operational_family as of
import nonclassicality_search as ns
import verify_nonclassicality as vn
ROOT=Path(__file__).resolve().parents[4]
class VerifyTests(unittest.TestCase):
 def setUp(self): self.c=nc.load_contract(ROOT); self.raw=of.enumerate_raw_candidates(self.c)
 def test_agrees_with_producer(self): self.assertEqual(vn.verify(self.c,self.raw)["primary_verdict"],ns.search_frozen_family(self.c)["primary_verdict"])
 def test_expected_candidate_is_independently_certified(self):
  r=vn.verify(self.c,self.raw); self.assertEqual(r["primary_verdict"],"CERTIFIED_OPERATIONAL_NONCLASSICAL_OBSTRUCTION"); self.assertEqual(r["witness"]["operational_score"],[4,1])
 def test_controls_remain_classical(self):
  r=vn.verify(self.c,self.raw); self.assertEqual(r["controls"]["V1553_PERMUTATION_CLASSICAL"],"CLASSICAL_COMPARATOR_FOUND"); self.assertEqual(r["controls"]["NONCOMMUTING_PERMUTATION_CLASSICAL"],"CLASSICAL_COMPARATOR_FOUND")
 def test_injected_nonclassical_flag_fails(self):
  raw=deepcopy(self.raw); raw[-1]["nonclassical"]=True; self.assertEqual(vn.verify(self.c,raw)["primary_verdict"],"FAMILY_INVALID")
 def test_negative_probability_fails(self):
  raw=deepcopy(self.raw); raw[-1]["operational_table"]["x0y0"]["00"]=[-1,2]; self.assertEqual(vn.verify(self.c,raw)["primary_verdict"],"FAMILY_INVALID")
 def test_operational_mutation_closes_positive_gate(self):
  raw=deepcopy(self.raw); raw[-1]["operational_table"]["x1y1"]={"00":[1,2],"01":[0,1],"10":[0,1],"11":[1,2]}; self.assertNotEqual(vn.verify(self.c,raw)["primary_verdict"],"CERTIFIED_OPERATIONAL_NONCLASSICAL_OBSTRUCTION")
 def test_id_relabel_invariant(self):
  raw=deepcopy(self.raw); raw[-1]["id"]="renamed"; a=vn.verify(self.c,self.raw); b=vn.verify(self.c,raw); self.assertEqual(a["primary_verdict"],b["primary_verdict"])
 def test_json_roundtrip(self): self.assertEqual(vn.verify(self.c,self.raw),vn.verify(self.c,json.loads(json.dumps(self.raw))))
 def test_double_replay_canonical(self):
  a=json.dumps(vn.verify(self.c,self.raw),sort_keys=True,separators=(",",":")); b=json.dumps(vn.verify(self.c,self.raw),sort_keys=True,separators=(",",":")); self.assertEqual(a,b)
 def test_firewall(self):
  r=vn.verify(self.c,self.raw); self.assertEqual(r["source_correspondence"],"NOT_EVALUATED"); self.assertEqual(r["Pillar_3"],"OPEN"); self.assertFalse(r["universal_quantum_derivation"]); self.assertFalse(r["physical_gravity"])
if __name__=="__main__": unittest.main()
