"""Supplied-only directed-corpus validation cannot detect omission."""
import unittest
def supplied_only(records,identities):
 for row in records:
  if row['case'] not in identities:raise ValueError('identity')
class Red(unittest.TestCase):
 def test_missing_corpus_case_must_be_rejected(self):
  with self.assertRaises(ValueError):supplied_only([],['binary4-all1-minimal-identity'])
if __name__=='__main__':unittest.main()
