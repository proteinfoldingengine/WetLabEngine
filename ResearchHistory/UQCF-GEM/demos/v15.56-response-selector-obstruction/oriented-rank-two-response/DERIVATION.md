# Oriented rank-two retained readout

v15.92 excluded singular C from its frozen regular readout. It did not prove absence of rotations at rank two. We now specify an additive oriented extension, retaining every historical verdict.

For real rank-two C, let V be its support polar partial isometry. Define

R = V + cof(V), P = R^T C.

Here cof is the matrix of signed minors, not its transpose. In oriented three-dimensional endpoint spaces, R is the unique element of SO(3) agreeing with V on its initial support. To prove this, use oriented singular frames: V=U diag(1,1,0) Z^T with U,Z in SO(3), so cof(V)=U diag(0,0,1) Z^T. Hence R=UZ^T, and any proper extension must map the final missing axis in this way. Under A,B in SO(3), R(ACB^T)=A R(C) B^T. This uses the already specified Bloch-space orientation (unitary qubit frames act by SO(3)); it is not an external alignment or a uniquely selected physical source law. General O(3) frame equivariance is not claimed for the oriented extension.

For a smooth constant-rank-two curve, write dR=RW and W^T=-W. Differentiating C=RP and removing the symmetric dP gives

P W + W P = Q = R^T dC - dC^T R.

P has eigenvalues p1,p2>0,0. On skew matrices the three Sylvester eigenvalues are p1+p2,p1,p2: all positive. Solve only off-diagonal entries in the P eigenbasis; the zero diagonal 0/0 is never evaluated. At rank one a skew kernel remains. C=diag(1,0,0) admits both I and a quarter-turn about x as proper completions, so uniqueness fails there.

The frozen planar preparation channel has T=diag(1/2,1/2,0). Every C and dC is supported on its xy block. The proper completion can rotate only within that plane, so the three-edge derivative map has rank at most three. The frozen source touches the first two sites; its hidden leakage reaches only edges (1,2) and (2,0), giving the sharper prediction of rank two for coherent arms and zero for the incoherent arm. This is a preregistered prediction, not an imposed rank.

Independent planar formula: let the xy block be [[a,b],[c,d]], k=sign(ad-bc), x=a+k*d, y=c-k*b, n=sqrt(x*x+y*y). Its O(2) polar factor is [[x,-k*y],[y,k*x]]/n. The SO(3) completion appends k on the third axis. For perturbation dx,dy, dtheta=(x*dy-y*dx)/(x*x+y*y), and W_xy=k*dtheta*[[0,-1],[1,0]]. Both determinant signs must be supported.

Central differences below differentiate C+epsilon*dC in matrix space. They are a numerical derivative check, not a finite quantum-state trajectory or an ordered source-composition theorem. Physical center/probe checks are separately inherited and recomputed.
