# Physical ordered-channel paths and one-sided polar obstruction

The inherited local source on pair (2,3) is L_D(X)=U X U†-X, where U=(Z⊗I+X⊗X)/√2. Its two Hermitian Pauli terms anticommute and square to identity, hence U†U=I. Therefore E_s(X)=(1-s)X+sUXU† is CPTP for every 0≤s≤1. The parameter s is a mixture strength, not a fundamental time.

The local depolarizing middle map has Pauli weights ((1+3a)/4,(1-a)/4,(1-a)/4,(1-a)/4), nonnegative and normalized for the frozen a values. Plane preparation has weights (1/2,1/4,1/4,0); isotropic preparation has (1/2,1/6,1/6,1/6). Their tensor products and compositions are CPTP.

For an exactly normalized positive state, the two paths

    rho_after(s) = Q E_s M_a rho,
    rho_before(s) = Q M_a E_s rho

are density-state paths throughout [0,1]. They share z=Q M_a rho at s=0 and have state derivatives x_after=Q L_D M_a rho and x_before=Q M_a L_D rho. Their derivative difference is Q[L_D,M_a]rho, exactly the inherited contrast. This does not equate that difference with either individual path.

For raw archived matrix R with trace τ, the physical input used here is explicitly R/τ. The raw R is preserved as a separate algebraic control. Exact rational-complex LDL reconstruction with strictly positive diagonal pivots proves R positive definite; τ>0 and Tr(R/τ)=1 then certify the physical input. Because connected moments are nonlinear, their matrices must be rebuilt: C_normalized=B/τ−uv^T/τ², not C_raw/τ. Exact support may depend on small binary residues, so all ranks and projectors are recomputed separately. This parameter-free normalization is a new disclosed input convention, not a silent correction to earlier runs.

If the affine state path is z+s x, let its pair moment be B+s B', and one-body moments u+s u', v+s v'. Then

    C(s) = (B−uv^T) + s(B'−u'v^T−uv'^T) − s²u'v'^T.

The implementation records all three coefficients and checks that its linear term equals the full connected differential. A first-order affine approximation to C(s) is not substituted for the physical path.

For C=C(0) and V=C'(0), use exact support projectors P=C C+ and Qr=C+ C. A nonzero N=(I−P)V(I−Qr), of rank k, forces rank(C(s))≥rank(C)+k for all sufficiently small positive s. The Schur complement in support/null coordinates is sN+o(s). This proof is one-sided and therefore applies at the endpoint of the CPTP mixture interval; no negative mixture is required.

The canonical polar partial isometry, zero on the kernel, has Frobenius norm squared equal to matrix rank. For baseline rank r and nearby rank r'≥r+k, the trace inequality Re tr(U(0)†U(s))≤r gives ||U(s)−U(0)||_F²≥r'−r≥k. Thus the actual normalized physical path has discontinuous canonical support transport whenever k>0. No finite lower bound on the size of the neighborhood is asserted.

If N=0, physical-path existence is still certified by the CPTP construction. The inherited label TANGENT_COMPATIBLE_NOT_PATH_CERTIFIED refers only to constant-rank stability not yet being certified: higher-order rank growth may still occur. At a=1 both ordered paths coincide, but neither individual derivative is required to vanish; only their contrast vanishes.

This theorem concerns the specified source family and canonical polar partial transport. A scalar observable might remain smooth and needs its own definition and test. The chosen source law is not derived here from retained consistency. Time is pruning / ordered recoverability update; no gravity claim follows.
