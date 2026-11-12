# Exact guard check on the balanced pair, fiber {p,u}, p=(0,) depth1 with children u=(0,0), v=(0,1).
import sys; sys.dont_write_bytecode=True
from fractions import Fraction as Fr
def w(x,A,B,g1,g2):  # reference A*x + B*T1(x) + M*D_g on the fiber; M=1
    xo,xp,xu,xv=x; m_p=xp+xu+xv
    return (A*xp+B*m_p+(g1-2*g2), A*xu+g2)
def fixed(x,ref): return x[1]*ref[1]==x[2]*ref[0]
xp=tuple(Fr(a,5) for a in (1,1,2,1)); xm=tuple(Fr(a,5) for a in (1,1,1,2))
rows=[]
for A in (0,1,2):
  for B in (0,1):
    for g1 in (0,1,3,5):
      for g2 in (0,1):
        rp,rm=w(xp,A,B,g1,g2),w(xm,A,B,g1,g2)
        if min(rp+rm)<=0: continue
        rows.append((A,B,g1,g2,fixed(xp,rp),fixed(xm,rm)))
for r in rows: print(r, "SEPARATES" if r[4]!=r[5] else "blind")
glob=[r for r in rows if r[2]==0 and r[3]==0]
print("globally-positive (g=0) cases all blind:",all(r[4]==r[5] for r in glob), len(glob))
print("some locally-positive g!=0 case separates:",any(r[4]!=r[5] for r in rows if (r[2],r[3])!=(0,0)))
