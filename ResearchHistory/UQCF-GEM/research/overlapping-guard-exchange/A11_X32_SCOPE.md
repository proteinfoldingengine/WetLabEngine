# A11.X32 scope — deterministic witness-preserving patch placement

Live analytical parent:331480e780945633cd170db307745d915cb64d06.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Next unused checkpoint:X32. Analytical only.

Relax X31's requirement that every pair have MORE old witnesses than the entire patch budget. In a uniform ORIGINAL floor grade L of ell slots, let W(K) be actual source indices missing pair K. For p destination patch tokens, a p-slot subset J is unsafe for K exactly when W(K) subset J. Exact finite counting gives probability binom(ell-w_K,p-w_K)/binom(ell,p); if the SUM over pairs is<1, an actual safe J exists.

Disclosed construction: use conditional finite completion counts, not a heuristic/random scientific run. At each partial J, the average of next-slot conditional bad-pair counts equals the current count; select an eligible slot with nonincreasing count. With initial count<1, after p steps the integer bad-pair count is0. Supply well-founded progress p-|J| and exact next-choice existence. Full destination patch tokens can be permuted WITHIN the same original floor grade L via baseline M, saving the full reverse; background floors remain fixed.

Given actual minimum source witness count rho, the simple sufficient count is C(k,2)*(p/ell)^rho<1. X31's odd two-grade shared bounds supply rho=ceil((k-3-epsilon-3delta)/2)>=1, destinationp<=delta, under epsilon+3delta<k-3. Proposed structural theorem also assumes C(k,2)*(delta/ell)^rho<1. Prove full lower safety, upper conversion only between exact ends, renewed patch guard, actual next primitive/termination and complete labelled/noncompact restoration including compatible saved permutation.

Nonvacuous infinite extension: X29 constructor plus d HIGH duplicates, t0,k=2^m-1,m>=5,d=floor((k-7)/6). Then rho>=2,delta=d,epsilon3d,ell=k(k-1)(k-3)/24, and C(k,2)*(d/ell)^2 <=8k/((k-1)(k-3)^2)<1. These profiles violate X31's epsilon+5delta<k-3 (k31 check directly; k>=63 use floor lower bound), so the placement theorem genuinely extends the derived complete-repair domain. Constructor defines a NEW FIXED carrier, never native changes to slots/floors. Algebraic coordinates specify subsets only.

No scientific enumeration/numerical execution/test/workflow/run ID, implementation/benchmark or certified integration merge. No probabilistic empirical inference or newly imposed geometry. Fresh independent whole-argument review and immutable exact packet readback required. Prior stronger classes/failure classifications preserved. v16.55/directed/unrestricted mixed/higher-target/nested/physical remain open; certified baseline and efficiency design unchanged, runner execution unstarted.
