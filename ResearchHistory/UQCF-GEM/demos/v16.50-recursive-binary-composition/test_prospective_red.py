"""Prospective failures against inherited implementation and supplied-only coverage."""
import unittest,importlib.util
from pathlib import Path
import sys
OLD=Path(__file__).resolve().parent.parent/'v16.49-fork-chain-interface'
sys.path.insert(0,str(OLD))
spec=importlib.util.spec_from_file_location('historical_fork',OLD/'producer.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def supplied_only(records):return all('path' in r for r in records)
class Red(unittest.TestCase):
 def test_missing_recursive_interface(self):self.assertTrue(callable(getattr(old,'normalize_recursive',None)),'MISSING_RECURSIVE_BINARY_INTERFACE')
 def test_supplied_only_omission(self):
  with self.assertRaises(ValueError):supplied_only([])
if __name__=='__main__':unittest.main()
