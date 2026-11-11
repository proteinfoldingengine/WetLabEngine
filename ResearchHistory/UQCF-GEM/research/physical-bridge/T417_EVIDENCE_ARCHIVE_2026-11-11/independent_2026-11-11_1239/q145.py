# Q145: can a fixed state omega on A_0 supply the survivor label covariantly?
# Witness from Q144: X0={0,p,l1,l2}, block {p,l1,l2} merged; chain automorphisms = S_3 on the block.
# Claim: for any S_3-covariant rule sigma(omega) (sigma(omega o a^-1) = a sigma(omega)),
#   sum over the S_3/Stab orbit of omega of 1[sigma = {p}] <= 1, so under any exchangeable
#   preparation measure P(sigma(omega) = survivor) <= 1/3.
import itertools, numpy as np
rng = np.random.default_rng(145)
B = ['p','l1','l2']
perms = list(itertools.permutations(range(3)))
def act(a, w): # (a.w)[a[i]] = w[i]
    out = [None]*3
    for i in range(3): out[a[i]] = w[i]
    return tuple(out)
rules = {
 'argmax':    lambda w: int(np.argmax(w)) if len(set(w))==3 else None,
 'argmin':    lambda w: int(np.argmin(w)) if len(set(w))==3 else None,
 'median':    lambda w: int(np.argsort(w)[1]) if len(set(w))==3 else None,
 'closest_to_third': lambda w: int(np.argmin(np.abs(np.array(w)-np.mean(w)))) if len(set(np.round(np.abs(np.array(w)-np.mean(w)),15)))==3 else None,
}
N=20000; viol=0; covfail=0; agree={k:0 for k in rules}
for _ in range(N):
    x = rng.dirichlet(np.ones(4)); w = tuple(x[1:])
    for k,f in rules.items():
        s = f(w)
        if s is None: continue
        if s==0: agree[k]+=1
        orbit_hits = 0
        for a in perms:
            sa = f(act(a,w))
            if sa != a[s]: covfail+=1   # covariance check
            orbit_hits += (sa==0)
        # each survivor-hit coset counted |Stab(sigma)|=2 times among 6 perms
        if orbit_hits/2 > 1: viol+=1
print('samples',N,'covariance failures',covfail,'orbit-bound violations',viol)
for k in rules: print(k,'P(select survivor p)=%.4f'%(agree[k]/N),'(bound 1/3)')
# symmetric state: w with w_p = w_l1 -> no covariant singleton rule can pick p (stabilizer contains (p l1))
w=(0.3,0.3,0.1); stab=[a for a in perms if act(a,w)==w]
print('stabilizer of (0.3,0.3,0.1):',stab,'-> covariant sigma must be stab-invariant; {p} invariant?', all(a[0]==0 for a in stab))
