# 16.11 — Full coherence interval and its zero-coherence stratum

Frozen before ensemble measurement. Parent: 16.10 final publication `3bc9218b9e0fff1cd13722deca4419c5b3fcdb8b`, scientific head `1e9a5e8029e53b09998f99b122a9df3324178b1b`.

Question: how does the one-sided boundary polar value depend on the entire existing source-coherence parameter λ∈[−1,1], and what actually happens at λ=0?

Use Lλ=((1+λ)/2)L+ + ((1−λ)/2)L− and Eλ,s=I+sLλ. The three channel weights are 1−s, s(1+λ)/2, s(1−λ)/2; they are nonnegative and sum to one on the full rectangle 0≤s≤1, −1≤λ≤1. No new source family or physical law is inserted. Direct exact transfer reconstruction and normalized-input positivity are inherited and rechecked. All 12 candidates, 3 archived binary a values, 2 preparation arms, and 2 orders remain: 144 families.

Compute the exact connected polynomial C(s,λ)=C+sV(λ)+s²W(λ) directly from the global Pauli coefficients. V must be affine and W at most quadratic in λ; verify every coefficient and both ±1 endpoints against 16.10. Test N(λ)=λN+ symbolically, rather than sampling λ. For λ≠0, exact common-plane or ambient rank bounds plus the first-order normal rank certify r+k for every fixed nonzero λ. If a structural bound is absent, label the continuum limit uncertified; do not infer it from finitely many λ samples.

At λ=0 compute the exact polynomial rank in s. N(0)=0 alone is insufficient. If the polynomial rank equals baseline rank r, certify constant rank in a sufficiently small neighborhood and limit polar(C). Otherwise label ZERO_COHERENCE_RANK_CHANGE and do not assign a missing higher-order limit. Test common order limits via the exact positive normal scaling and common baseline; verify identity-middle path equality separately.

If all certificates hold, the predicted fixed-λ boundary classes are polar(C)+polar(N+) for λ>0, polar(C) for λ=0, and polar(C)−polar(N+) for λ<0. This is a conditional theorem about the fixed-λ, s↓0 limit. No uniformity in λ or joint-limit claim is made.

Numerical audit at λ=−1/2,0,+1/2, 80/120 digits and both inherited frames. Record 1,728 limits if all144 families certify. At 120 digits use s=2^-32,2^-128,2^-192 in both frames: 2,592 finite polar records. Exact finite rank, no numerical rank cutoff. Controls: polar positivity/reconstruction, partial-isometry identities, covariance and class-gap squared (k to zero, 4k across signs) ≤1e-35; cross-precision ≤1e-30. Convergence is descriptive, no fitting or finite-grid pass threshold. Preserve orientation.

Verdicts: THREE_COHERENCE_BOUNDARY_CLASSES_CERTIFIED if all symbolic identities/rank certificates/order identities hold; ZERO_COHERENCE_RANK_CHANGE if any zero-coherence rank increases; CONTINUUM_LIMIT_NOT_CERTIFIED for other missing certificates; FAMILY_IDENTITIES_NOT_CONFIRMED for valid negative symbolic tests; INVALID for provenance, physicality, completeness or numerical-control failure. Publish every case and negative outcome.

Final synthesis must distinguish: .09 fixed-source order agreement; .10 source-choice dependence; .11 full-family classification. The goal is to identify what the retained data determine without fitted completion or a silently chosen source. Time is pruning / ordered recoverability update. No universal source, clock, gravity or dark-matter derivation follows.
