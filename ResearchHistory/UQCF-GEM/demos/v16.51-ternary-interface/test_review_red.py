"""Prospectively declared verifier-level and full-palette mechanism mutations."""
import unittest,types
from pathlib import Path
import producer as p
import verifier as v
class ReviewRed(unittest.TestCase):
 def test_full_verifier_omission(self):
  doc=p.produce();self.assertEqual(v.verify(doc)['cases'],2592)
  doc['cases'].pop()
  original=v.verify_identities
  def supplied_only(rows,expected):
   for row in rows:
    if row not in expected:raise ValueError('unknown identity')
   return True
  v.verify_identities=supplied_only
  try:
   with self.assertRaisesRegex(ValueError,'identities',msg='FULL_VERIFIER_OMISSION_ACCEPTED'):v.verify(doc)
  finally:v.verify_identities=original
 def test_whole_palette_exception(self):
  source=Path(p.__file__).read_text();needle='i in chosen and w[c]<k'
  self.assertEqual(source.count(needle),1)
  module=types.ModuleType('mutant_producer');module.__file__=p.__file__
  exec(compile(source.replace(needle,'i in chosen'),p.__file__,'exec'),module.__dict__)
  q=[2,1,1,1,2,2,2];start=p.initial(p.U,4,q,'reversal','compact')
  self.assertEqual(module.normalize(start,p.U,4,q)[-1],p.canonical(p.U,4,q),'FULL_PALETTE_ORDER_LOST')
 def test_start_failure_retained(self):
  from unittest.mock import patch
  with patch.object(p,'initial',side_effect=ValueError('INJECTED_START_FAILURE')):
   try:doc=p.produce()
   except Exception:self.fail('START_FAILURE_ESCAPED')
  self.assertEqual(len(doc['cases']),2592)
  self.assertTrue(all(row['failure'] is not None for row in doc['cases']))
 def test_failure_outcome_classifier(self):
  import run_campaign
  self.assertTrue(callable(getattr(run_campaign,'failure_outcome',None)),'MISSING_FAILURE_OUTCOME_CLASSIFIER')
if __name__=='__main__':unittest.main(verbosity=2)
