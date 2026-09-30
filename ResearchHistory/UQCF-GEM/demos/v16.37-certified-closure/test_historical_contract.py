"""Intentionally fails the historical generic lexicographic contract."""
import importlib.util
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'v16.36-barrier-law-closure'/'producer.py'
s=importlib.util.spec_from_file_location('historical',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
A={'a':['u','v'],'u':['a','x'],'v':['a','x'],'x':['u','v','w'],'w':['x','b'],'b':['w']}
Q={'a':(2,2,2),'u':(4,2,2),'v':(3,3,3),'x':(2,2,2),'w':(3,3,3),'b':(2,2,2)}
m.q=lambda p,x:Q[x]
actual=m.exact(None,A,'a')['b']
assert actual==(3,1,3),('HISTORICAL_LABEL_LOSS',actual,(3,1,3))
