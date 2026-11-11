import numpy as np, itertools
rng=np.random.default_rng(154)
n,dq=4,4
I2=np.eye(2);X=np.array([[0,1],[1,0]])
P=[np.diag([1,0]),np.diag([0,1])]
def blk(parts): # projections of partition on C^n
    return [np.diag([1.0 if i in p else 0 for i in range(n)]) for p in parts]
pi={0:[{i} for i in range(n)],1:[{0,2},{1,3}],2:[{0,1,2,3}]}
# pinching algebras: basis spans
def AS(j):
    if j==0: return [np.eye(4)[:,[a]]@np.eye(4)[[b],:] for a in range(4) for b in range(4)]
    if j==1: return [np.eye(4)[:,[a]]@np.eye(4)[[b],:] for a in range(4) for b in range(4) if a//2==b//2]
    return [np.eye(4)[:,[a]]@np.eye(4)[[a],:] for a in range(4)]
def span(parts,j): return [np.kron(e,a) for e in blk(parts) for a in AS(j)]
def proj_basis(ops):
    M=np.array([o.ravel() for o in ops]).T
    u,s,_=np.linalg.svd(M,full_matrices=False); return u[:,s>1e-9]
def inside(op,B): v=op.ravel(); return np.linalg.norm(v-B@(B.conj().T@v))<1e-8
Aj={j:proj_basis(span(pi[j],j)) for j in range(3)}
G=[p for p in itertools.permutations(range(n)) if all(sorted(sorted(p[i] for i in b) for b in pi[j])==sorted(sorted(b) for b in pi[j]) for j in range(3))]
print("|G|=",len(G))
def rphase(k): return np.exp(1j*rng.uniform(0,2*np.pi,k))
def sample():
    p=G[rng.integers(len(G))]
    W=np.diag(rphase(4))@np.kron(np.linalg.matrix_power(X,rng.integers(2)),np.linalg.matrix_power(X,rng.integers(2)))
    Db={0:np.diag(rphase(4)),1:np.diag(rphase(4))}  # per pi_1 block
    blockof=lambda x:0 if x in (0,2) else 1
    U=np.zeros((16,16),complex)
    for x in range(n):
        f=rphase(2); F=np.diag([f[0],f[0],f[1],f[1]])
        Ux=W@Db[blockof(x)]@F
        U+=np.kron(np.outer(np.eye(n)[p[x]],np.eye(n)[x]),Ux)
    return U
gs=[sample() for _ in range(60)]
for g in gs:
    for j in range(3):
        for k in range(Aj[j].shape[1]):
            op=Aj[j][:,k].reshape(16,16); assert inside(g@op@g.conj().T,Aj[j]),"not in G_J"
print("all sampled g preserve A_0,A_1,A_2")
def core(parts,j):
    B=proj_basis(span(parts,j))
    for g in gs:
        Bg=proj_basis([g@B[:,k].reshape(16,16)@g.conj().T for k in range(B.shape[1])])
        # intersection of subspaces
        M=np.hstack([B,-Bg]); _,s,vh=np.linalg.svd(M); null=vh[np.sum(s>1e-9):].conj().T
        B=proj_basis([(B@v[:B.shape[1]]).reshape(16,16) for v in null.T]) if null.shape[1] else np.zeros((256,0))
    return B.shape[1]
S1=[{0},{1},{2},{3}]; S2=[{0},{2},{1,3}]
print("dim Core^J_1 =",core(S1,1),"expected",4*8)
print("dim Core^J_2 =",core(S2,2),"expected",2*4)
