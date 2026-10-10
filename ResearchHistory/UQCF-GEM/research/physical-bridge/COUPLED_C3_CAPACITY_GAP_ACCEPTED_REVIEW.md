# Independent mathematical assessment: capacity and reachability gap

Verdict: ACCEPTED. Not formal certification or broad C3/C4 closure.

Science/workflow 927836d37fbe858dea36c3e88856a53cbb69d7db; run38013084106; modelgemini-3.1-pro-preview; 20 inputs; 22017 tokens; response SHA256 34271b49122723e6a4ae167c934a1b2d8de6fb8c042aa472c3d04808a5e470b1.

[Unmodified response](evidence/capacity-gap/mathematical-review-response.txt); manifests and original archives are preserved. Zero missing assumptions and counterexamples listed.

Findings:

- The integer allocation formulation kappa correctly and exactly characterizes the static reserve capacity by mapping current footprints to maximal original footprints, preserving floors and the upper-four cover condition.
- The obstruction family n>=2 rigorously demonstrates an unbounded reachability gap: static capacity is exactly 5, allowing n-2 labels to be absent for n>=3, yet the saturated antichain source is isolated under all uniformly safe core toggles.
- The upper control example correctly proves that the upper-four cover condition is independent of the floor and footprint-domination conditions, as the candidate has tau=5 despite satisfying the latter two.
- The RED log accurately reflects a module import error (producer not found), resulting in zero executed test bodies, rather than mathematical test failures.
- The independent reconstruction correctly implements set-based minimal representative unions and exhaustive three-label candidates, providing a robust cross-check against the producer's bitwise subset covers and integer allocations.

Limitations:

- The theorem characterizes static admissibility and capacity but does not provide a general path-existence condition or resolve connectivity for arbitrary exact targets.
- The results apply to the declared finite core domains and do not extend to unbounded root creation, arbitrary floors exceeding core sizes, or hidden-label operations.
- The framework relies on supplied native observer access, static addresses, and protected-band promises, without deriving physical observer genesis or progress laws.
- Broad C3 and general C4 remain OPEN.

Author reconciliation: arbitrary-object statements rest on proof, finite tests cover the frozen domain; upper-control establishes insufficiency of two candidate conditions, not a changed minimum kappa in that example. No reserve is absent at n=2; unbounded surplus is for n>=3. RED executes a loader placeholder and zero scientific bodies. API reviews supplied records; author immutable readback separately verifies freeze history and executed bytes. Static safe endpoint does not imply a safe route. See closeout/evidence ledger.
