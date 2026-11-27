"""Run separately with the pinned v16.53 directory."""
from itertools import product
from pathlib import Path
import sys
sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import verifier as v

A,B,D={0},{1},{0,1}
# Keep chart one at D while two of the three exterior charts exchange the A-only role.
steps=[[D,A,B,B],[D,A,D,B],[D,A,A,B],[D,D,A,B],[D,B,A,B]]
path=[v.raw_roots(2,s) for s in steps]
assert v.path_check(v.Q,2,[2],path,path[0],path[-1])==0
# Holding chart one and chart two both double leaves only opposite singleton exteriors.
compatible=[(left,right) for left,right in product((A,B,D),repeat=2)
            if v.profile_check(v.Q,2,v.raw_roots(2,[D,D,left,right]))==[2]]
assert compatible==[(A,B),(B,A)]
print('one held double: exact role exchange in',len(path)-1,'edits')
print('two held doubles: compatible exteriors (A,B) and (B,A); single edit cannot connect them')
