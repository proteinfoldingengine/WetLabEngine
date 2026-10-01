"""Inherited three-internal interface cannot normalize a four-internal chain."""
from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'v16.47-saturated-chain-repair'))
from producer import normalize
class RecursiveRed(unittest.TestCase):
 def test_recursive_contract(self):
  try:path=normalize([511],(2,2,2,2),1,[1,1,1,1,0,0,0,0,0])
  except TypeError:path=None
  self.assertIsInstance(path,list)
if __name__=='__main__':unittest.main()
