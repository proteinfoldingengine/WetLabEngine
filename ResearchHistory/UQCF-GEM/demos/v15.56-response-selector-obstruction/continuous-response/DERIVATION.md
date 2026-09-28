# Continuous weighted response versus polar normalization

For any real matrix C with canonical polar partial isometry U, U|C|=C. Thus multiplying polar transport by its positive singular-value factor retains the full matrix rather than forcing every supported direction to unit magnitude. This familiar identity supplies no new dynamics or canonical reason to call C a geometric transport.

The frozen physical family has exact polynomial coefficients C(s,λ)=C+s(V0+λV1)+s²(W0+λW1+λ²W2). Because the Frobenius norm is bounded by the entrywise absolute sum, for all |λ|≤1 and 0≤s≤1,

`||C(s,λ)−C||F ≤ s (||V0||entry1+||V1||entry1) + s² sum_i ||Wi||entry1`.

This proves continuity uniformly across the coherence interval, including joint approaches with s→0. It is a theorem about C (equivalently weighted polar), not the unweighted polar limits of 16.09–16.11.

Let P=CC⁺ and Q=C⁺C be frozen at the baseline. Their complementary projections kill C. For K=(I−P)C(s,λ)(I−Q), direct coefficient projection gives K=sN(λ)+s²M(λ). If the archived identity N(λ)=λN+ holds, then K/s→λN+. New directions disappear continuously in amplitude but their signed first derivative remains. When N_before=a N_after with a>0, the derivative contrast is λ(1−a)N_after. At a=1 the complete ordered paths coincide; for a≠1 and λ≠0 a nonzero N_after gives nonzero ordering contrast.

For H=CᵀC, the derivative at C in direction V is CᵀV+VᵀC. A normal direction N=(I−P)V(I−Q) obeys CᵀN=0 and NᵀC=0. Thus the Gram derivative cannot detect this normal component, although tangential parts of V may still give a coherence or ordering response.

The isolated normal energy is

`KᵀK = s² λ² N+ᵀN+ + s³ λ(N+ᵀM+MᵀN+) + s⁴ MᵀM`.

Only the leading coefficient is asserted to be even in λ. For a pure-normal synthetic path diag(2,±s,0), the Gram matrices agree exactly at every s while the matrices themselves differ. This demonstrates actual information loss by squaring; it does not assert equal Gram matrices for every real ensemble path.

No rank threshold, source-strength adjustment, null-space completion, external alignment or determinant correction is introduced. The full matrix is covariant under the same endpoint frame changes; K also transforms covariantly when its baseline projectors transform with it. The Gram and normal-energy matrices transform at the right endpoint. Inversion, polar normalization or a new connection constructed from these quantities would require a separate domain and interpretation audit.

The sixth edge remains distinct from the original five-edge readout. Recovering an amplitude response here does not retroactively change that readout's null result. Sources remain supplied CPTP channels, not derived sourcehood. Time is pruning / ordered recoverability update; no clock or gravity law is claimed.
