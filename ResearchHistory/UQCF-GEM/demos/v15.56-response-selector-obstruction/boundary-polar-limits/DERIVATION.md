# One-sided rank-saturated polar limit

For a differentiable real matrix path C(s)=C0+sV+O(s²), let C0 have rank r. In orthonormal support/null coordinates, the active block is invertible and the null-to-null Schur complement is sN+O(s²), where N=(I-P)V(I-Q). Existing singular subspaces converge to the support of C0. Newly born first-order singular subspaces converge to those of N. If the path's eventual rank is exactly r+rank(N), there are no additional slower-born modes. The one-sided zero-on-kernel polar limit for s↓0 is therefore polar(C0)+polar(N). The two summands have orthogonal initial and final supports.

Rank saturation is essential: C(s)=diag(1,s,s²) has N=diag(0,1,0), but a third polar direction survives for every s>0. The proposed formula would miss it without the rank certificate. Plane paths are certified by a common exact zero row/column in all coefficients; full three-dimensional saturation bounds isotropic paths. An exact polynomial-rank fallback handles other cases.

If the two paths share C0 and N_before=a N_after with a>0, their limiting polar factors agree exactly. Positive scalar multiplication leaves a canonical polar partial isometry unchanged. This sufficient criterion is not necessary and its failure does not prove inequality. At a=1 the entire path polynomials agree.

The limit is covariant under left/right orthogonal changes of frame, because both canonical polar summands are covariant. No null-space frame is chosen and no determinant correction is applied. For planar rank-two limits, a separate cofactor completion would be a different object and is not introduced in this run. Full-rank isotropic limits may have either orientation, which is recorded.

The finite grid only displays approach to the analytic limit. Tiny baseline singular values can delay that approach; fitting a convergence rate or treating the last finite point as the proof would be invalid. Equal limits for two fixed ordered paths do not show independence from source law or all admissible paths. Time is pruning / ordered recoverability update.
