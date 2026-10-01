"""Coverage mutation control: checking supplied rows cannot detect omission."""
import unittest
def supplied_only(records, identities):
    for row in records:
        if (row['state'],row['q']) not in identities:raise ValueError('identity')
class Red(unittest.TestCase):
    def test_missing_representative_must_be_rejected(self):
        with self.assertRaises(ValueError):
            supplied_only([],[(0,[1,1,1,0,0,0,0])])
if __name__=='__main__':unittest.main()
