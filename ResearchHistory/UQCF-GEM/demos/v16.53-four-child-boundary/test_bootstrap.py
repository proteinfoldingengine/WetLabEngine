import importlib.util
import unittest

def fixture():
    state=[7,9,17]
    return {'schema':1,'kind':'canonical_admission_control','records':[{'identity':['CONTROL','canonical_q3'],'status':'ok','tree':[[],[],[],[]],'q':[3],'k':3,'start':state,'end':state,'path':[state]}]}

class Bootstrap(unittest.TestCase):
    def test_real_control_verifier(self):
        self.assertIsNotNone(importlib.util.find_spec('verifier'),'VERIFIER_MISSING')
        import verifier
        self.assertEqual(verifier.verify(fixture())['status'],'VERIFIED')

if __name__=='__main__':unittest.main(verbosity=2)
