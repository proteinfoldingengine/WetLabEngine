"""v15.48 type-obstruction verifier RED."""
from pathlib import Path
import unittest
import signature_contract as sc
import verify_type_obstruction as vt

class TypeObstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=sc.load_contract(cls.root)

    def test_obstruction_verifies(self):
        r=vt.verify(self.root,self.c)
        self.assertEqual(r["status"],"VERIFIED_NO_COMMON_TYPE_CERTIFIED")
        self.assertFalse(r["comparison_executable"])
        self.assertEqual(r["required_new_axiom"],
                         "CROSS_DOMAIN_RECOVERABILITY_EQUALITY_OR_FUNCTOR")

    def test_no_hidden_dictionary(self):
        r=vt.verify(self.root,self.c)
        self.assertFalse(r["hidden_dictionary_found"])

    def test_no_downstream_rescue(self):
        r=vt.verify(self.root,self.c)
        self.assertFalse(r["downstream_selector_permitted"])

    def test_type_promotion_rejected(self):
        bad=dict(self.c)
        bad["type_audit"]=dict(self.c["type_audit"])
        bad["type_audit"]["status"]="COMMON_TYPE_CERTIFIED"
        with self.assertRaisesRegex(ValueError,"unsupported_type_promotion"):
            vt.verify(self.root,bad)

if __name__=="__main__": unittest.main()
