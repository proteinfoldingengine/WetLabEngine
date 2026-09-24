"""v15.49 RED: independent bridge-typing verifier."""
from pathlib import Path
import copy, unittest
import bridge_contract as bc
import verify_bridge_typing as vt

class BridgeTypingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=bc.load_contract(cls.root)
    def test_typing_obstruction_verifies(self):
        r=vt.verify(self.root,self.c)
        self.assertEqual(r["status"],"VERIFIED_NO_CROSS_DOMAIN_MORPHISM_TYPE")
        self.assertFalse(r["bridge_enumeration_executable"])
    def test_required_new_object_explicit(self):
        r=vt.verify(self.root,self.c)
        self.assertEqual(r["required_new_object"],"CROSS_DOMAIN_HOMSET_OR_TYPED_BRIDGE_AXIOM")
    def test_no_cardinality_coercion(self):
        self.assertFalse(vt.verify(self.root,self.c)["equal_cardinality_used_as_typing"])
    def test_type_promotion_rejected(self):
        c=copy.deepcopy(self.c); c["typing"]=dict(c["typing"])
        c["typing"]["status"]="CROSS_DOMAIN_MORPHISM_TYPE_CERTIFIED"
        with self.assertRaisesRegex(ValueError,"unsupported_type_promotion"): vt.verify(self.root,c)
if __name__=="__main__": unittest.main()
