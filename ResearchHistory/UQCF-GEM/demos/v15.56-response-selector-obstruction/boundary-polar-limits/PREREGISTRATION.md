# v16.09 one-sided boundary polar limits

Parent publication37b0f8129b747d8097106f450f215c3e0462766e; scientific16.08 head8739e9db7ce1cb2c4ae0a91600e20fb4a2e953f5. User authorized16.09–16.11 on2026-09-28. This first protocol is frozen before measurement; follow-on protocols depend on its result.

Use all144 NORMALIZED physical paths from16.08 (12 candidates, a=1,binary1/3,1/6, both preparations, both orders). Preserve exact C(s)=C+sV+s²W and N=(I-P)V(I-Q), all source/input choices unchanged.

The proposed one-sided canonical polar limit is B=polar(C)+polar(N) for s↓0, provided eventual rankC(s)=r+k, where r=rankC and k=rankN. Nonzero N alone is insufficient if additional slower-born modes exist. Check r+k=3 for isotropic paths, or r+k=2 and exact zero third row/column in every plane coefficient. More general cases require exact generic polynomial rank equal to r+k. Failure to certify is a scientific LIMIT_NOT_CERTIFIED outcome, not permission to discard a path.

Compute canonical zero-on-kernel polar factors using exact ranks at80/120 digits in native and transformed frames. Check input reconstruction, support/projector identities, covariance, limit partial-isometry identities and cross-precision agreement. Absolute tolerance1e-35 within precision and1e-30 across precisions. Record determinants without SO correction. No new edge is inserted into a loop readout.

For every state/a/preparation pair test exact N_before=a*N_after. If true, a>0 proves equality of the normal polar factors and thus of both boundary limits. This sufficient test is not claimed necessary. If it fails, preserve numerical limit differences: >1e-9 at both precisions gives observed difference; <=1e-35 gives numerical agreement without that exact certificate; otherwise unresolved. At a=1 enforce exact identical path polynomials.

At120 digits additionally inspect the fixed positive grid s=2^-8,2^-32,2^-64,2^-128,2^-192 in both frames. Evaluate the exact polynomial and exact finite rank; compute canonical polar and residual to B. Grid errors are descriptive, never fitted or used to claim a uniform convergence rate/neighborhood. Check arithmetic/covariance, but do not reject a scientific result for slow convergence caused by tiny baseline singular values.

Validity requires hashes, parent identity/completeness, exact parent-normal reconstruction, all arithmetic controls, all144 limits and72 order comparisons present. INVALID has precedence. All rank-limit and order-scaling certificates gives COMMON_ORDER_BOUNDARY_LIMIT_CERTIFIED. Otherwise publish LIMIT_NOT_CERTIFIED or ORDER_LIMITS_NOT_FULLY_CERTIFIED, preserving every case. No physical-path/canonical-at-baseline equivalence is assumed: B may differ from the baseline partial isometry. No source-law selection, gravity claim or external alignment. Time is pruning / ordered recoverability update.
