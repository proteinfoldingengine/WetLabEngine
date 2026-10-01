"""Inherited single-chain interface cannot normalize a fork of chains."""
from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'v16.48-recursive-chain-repair'))
from producer import normalize
class ForkRed(unittest.TestCase):
 def test_fork_contract(self):
  try:path=normalize([2047],(2,2),(2,2),1,[1,1,1,0,0,0,1,1,0,0,0])
  except TypeError:path=None
  self.assertIsInstance(path,list)
if __name__=='__main__':unittest.main()
