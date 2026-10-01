"""Actual verifier mutation before recursive producer implementation."""
import unittest,copy
from pathlib import Path
from unittest.mock import patch
import verifier as v

def control_corpus():
 rows=[]
 for spec in v.expected_specs():
  M,start,end=v.model(v.SHAPES[spec['tree']],spec['q'],spec['k'])
  rows.append({'spec':copy.deepcopy(spec),'width':M,'start':end,'path':[end],'failure':None})
 return {'schema':1,'scope':v.SCOPE,'kind':'canonical_coverage_control','cases':rows}
class Prospective(unittest.TestCase):
 def test_recursive_interface_present(self):
  self.assertTrue(Path(__file__).with_name('producer.py').is_file(),'MISSING_RECURSIVE_TERNARY_INTERFACE')
 def test_full_verifier_omission_rejected(self):
  doc=control_corpus();self.assertEqual(v.verify(doc)['cases'],7236)
  missing=copy.deepcopy(doc);missing['cases'].pop()
  with self.assertRaisesRegex(ValueError,'canonical case identities'):v.verify(missing)
  with patch.object(v,'verify_identities',lambda records,expected:True):
   with self.assertRaises(ValueError,msg='FULL_VERIFIER_OMISSION_ACCEPTED'):v.verify(missing)
if __name__=='__main__':unittest.main(verbosity=2)
