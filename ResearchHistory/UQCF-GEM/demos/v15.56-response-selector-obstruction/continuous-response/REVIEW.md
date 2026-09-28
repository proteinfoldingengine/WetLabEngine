# Pre-measurement review

Independent reviewer review1607 found no blockers and independently passed all five tests without an ensemble run. Reviewed the exact uniform coefficient bound, frozen-support normal expansion, Gram first-derivative blindness, full normal-energy polynomial, frame covariance, exact finite ranks, 144/72/3456 record counts and negative-result handling.

The numerical algebra controls use the actual projected normal; the hypothesis N(λ)=λN+ remains a separately reported scientific test. The reviewer emphasized that nonidentity contrast coefficients are nonzero only as a statement about ΔN: the actual first-order contrast λΔN vanishes at λ=0. Weighted polar reconstruction is C itself, not a new transport law.

Both local and preregistered GitHub RED failed the five expected absent-implementation tests. During local test development, the energy-coefficient test compared an expanded polynomial with an equal factored polynomial using structural equality. Expanding the expected polynomial corrected this test-expression issue; no scientific criterion changed and no ensemble had been measured. All five tests then passed locally and independently.

Only the dedicated continuous-response GitHub workflow executes the ensemble. Protocol, source hashes, input coefficients, precision, grid, tolerances and physical interpretation remain frozen before that run.
