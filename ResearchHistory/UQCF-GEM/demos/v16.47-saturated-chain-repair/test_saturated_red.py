"""The inherited restricted normalizer does not satisfy the saturated contract."""
from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'v16.46-nested-chain-repair'))
from producer import normalize
class SaturatedRed(unittest.TestCase):
 def test_saturated_path_required(self):
  try:path=normalize([65,63],2,2,2,2,[2,1,1,0,0,0,0])
  except ValueError:path=None
  self.assertIsInstance(path,list)
if __name__=='__main__':unittest.main()
