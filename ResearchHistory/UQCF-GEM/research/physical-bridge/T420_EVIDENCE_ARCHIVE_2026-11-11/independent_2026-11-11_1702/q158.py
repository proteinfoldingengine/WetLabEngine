from fractions import Fraction as F
xp=(F(1,5),F(2,5)); xm=(F(1,5),F(1,5))  # (x_p,x_u) on fiber {p,u}
def fixed(x,w):  # omega∘E_w = omega on fiber iff x ∝ w (w_p,w_u >= 0, not both 0)
    return x[0]*w[1]==x[1]*w[0]
rows=[]
for g in (1,2,3):
    W={'COUNTING':(F(1),F(1)),'ABS_DEPTH(|p|=0)':(F(1),F(1,2**g)),'FIBER_DEPTH':(F(1),F(1,2**g)),
       'NORMALIZED_RESTRICTION=L8 indicator':(F(1),F(0))}
    for k,w in W.items(): rows.append((g,k,str(w[0]/w[1]) if w[1] else 'inf',fixed(xp,w),fixed(xm,w)))
for g,k,r,a,b in rows: print(f"g={g} {k:40s} w_p/w_u={r:5s} fixed(x+)={a} fixed(x-)={b} separates={a!=b}")
# actual state as its own reference
print('self-reference: fixed(x+,x+)=',fixed(xp,xp),' fixed(x-,x-)=',fixed(xm,xm),' separates=False')
# ABS_DEPTH ratio is depth-independent of |p|: 2^-|p| / 2^-|u| = 2^g
for p in range(4):
    for g in (1,2):
        assert F(1,2**p)/F(1,2**(p+g))==2**g
print('ABS_DEPTH ratio = 2^g for |p|=0..3, g=1,2: OK')
