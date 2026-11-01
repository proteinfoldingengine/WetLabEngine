import unittest,json,sys
from pathlib import Path
import uqcf_owner_scope_publication as old
import uqcf_owner_recovery_audit as new
class FormatRepair(unittest.TestCase):
 def test_actual_raw_response(self):
  v=json.loads(Path('owner_scope_review/verdict.json').read_bytes())
  self.assertEqual(v['verdict'],'ACCEPTED')
  self.assertIsInstance(v['constructive_analysis'],str)
  with self.assertRaises(ValueError): old.validate_constructive_response(v)
  new.validate_constructive_response(v)
 def test_preserved_list_and_rejection_controls(self):
  valid={'constructive_analysis':['Nonempty reconstruction'], 'next_native_obligation':'Bind actual retained receiver'}
  new.validate_constructive_response(valid)
  for value in [None,'', '  ',[],[None],[{}],[' '], 3, {}]:
   with self.subTest(value=value), self.assertRaises(ValueError):
    new.validate_constructive_response(dict(valid,constructive_analysis=value))
  for value in ['',None,[]]:
   with self.assertRaises(ValueError):new.validate_constructive_response(dict(valid,next_native_obligation=value))
if __name__=='__main__':unittest.main()
