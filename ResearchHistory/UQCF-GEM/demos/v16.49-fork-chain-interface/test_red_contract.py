"""Checking supplied directed records does not detect an omitted case."""
import unittest
def supplied_only(records,identities):
 for row in records:
  if row['case'] not in identities:raise ValueError('identity')
class Red(unittest.TestCase):
 def test_missing_case(self):
  with self.assertRaises(ValueError):supplied_only([],['overlapping-fork-singleton-identity'])
if __name__=='__main__':unittest.main()
