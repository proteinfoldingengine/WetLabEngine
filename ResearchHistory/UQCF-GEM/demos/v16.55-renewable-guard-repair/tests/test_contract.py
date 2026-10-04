"""Contract-first rejecting controls; run only on GitHub."""
import copy, importlib, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

class Contract(unittest.TestCase):
    def api(self):
        try: return importlib.import_module("verifier")
        except ModuleNotFoundError:
            self.fail("independent verifier implementation is missing")
    def base(self):
        a=[[0],[1],[2],[3]]
        case={"identity":["T",{},None,None],"k":4,"floors":[1]*4,"A":a,"C":a,"method":"boundary"}
        rec={"identity":case["identity"],"status":"PATH","preliminary":[a],"final":[a],"meta":{}}
        return case,rec
    def reject(self,change):
        v=self.api();c,r=self.base();change(c,r)
        self.assertTrue(v.verify_record(c,r),"corrupt record was accepted")
    def test_missing_identity(self):
        self.assertTrue(self.api().verify_universe([["a"],["b"]],[["a"]]))
    def test_duplicate_identity(self):
        self.assertTrue(self.api().verify_universe([["a"]],[["a"],["a"]]))
    def test_equal_count_substitution(self):
        self.assertTrue(self.api().verify_universe([["a"],["b"]],[["a"],["c"]]))
    def test_valid_record(self):
        c,r=self.base();self.assertEqual(self.api().verify_record(c,r),[])
    def test_wrong_tau(self):
        self.reject(lambda c,r:r.update(final=[[[0],[0],[0],[0]]]))
    def test_below_floor(self):
        self.reject(lambda c,r:r.update(final=[[[],[1],[2],[3]]]))
    def test_external_label(self):
        self.reject(lambda c,r:r.update(final=[[[4],[1],[2],[3]]]))
    def test_extra_root(self):
        self.reject(lambda c,r:r.update(final=[c["A"]+[[0]]]))
    def test_two_incidence_primitive(self):
        self.reject(lambda c,r:r.update(final=[c["A"],[[0,1],[1,2],[2],[3]],c["C"]]))
    def test_wrong_destination(self):
        self.reject(lambda c,r:r.update(final=[c["A"],[[0,1],[1],[2],[3]]]))
    def test_false_minimum_cover(self):
        self.reject(lambda c,r:r.update(meta={"cover":[0,1]}))
    def test_false_progress(self):
        self.reject(lambda c,r:r.update(meta={"progress":[{"before":1,"after":1}]}))
    def test_false_exact_entry(self):
        self.reject(lambda c,r:r.update(meta={"upper_entry":[[[0],[0],[0],[0]],c["C"]]}))
    def test_missing_assignment_token(self):
        self.reject(lambda c,r:r.update(meta={"assignment":[0,1,2]}))
    def test_illegal_grade_assignment(self):
        self.reject(lambda c,r:(c.update(floors=[2,1,1,1]),r.update(meta={"assignment":[1,0,2,3]})))
    def test_lost_pair_witness(self):
        self.reject(lambda c,r:r.update(meta={"pair_witnesses":[{"pair":[0,1],"index":0}]}))
    def test_false_conditional_count(self):
        self.reject(lambda c,r:r.update(meta={"placement":{"L":[0,1,2,3],"p":1,"steps":[{"D":[],"phi":"0"}]}}))
    def test_false_provenance(self):
        self.assertTrue(self.api().verify_provenance({"scientific_sha":"fake"},{"scientific_sha":"0"*40}))
    def test_corrupt_digest(self):
        self.assertTrue(self.api().verify_manifest({"a":b"x"},{"a":"0"*64}))
    def test_fake_diagnostics(self):
        self.assertTrue(self.api().verify_diagnostics({"cycle":0},["cycle"]))
    def test_nested_second_unit(self):
        self.assertTrue(self.api().verify_nested({"k":4,"target":4,"floors":[1]*4,"A":[[0],[1],[2],[3]],"C":[[0],[1],[2],[3]]},{"vertices":[{"parent":[[0],[0],[0],[0]],"leaves":[[[0]],[[1]],[[2]],[[3]]]}]}))
    def test_complete_reconstruction(self):
        try:
            u=importlib.import_module("universe")
        except ModuleNotFoundError:
            self.fail("producer identity generator is missing")
        v=self.api()
        self.assertEqual(list(u.generate_cases()),list(v.reconstruct_cases()))
    def test_all_producer_contracts(self):
        try:m=importlib.import_module("mechanisms")
        except ModuleNotFoundError:self.fail("proof-derived producer implementation is missing")
        v=self.api()
        for c in v.smoke_cases():
            r=m.produce(c)
            self.assertEqual(v.verify_record(c,r),[],c["identity"])

if __name__=="__main__":unittest.main(verbosity=2)
