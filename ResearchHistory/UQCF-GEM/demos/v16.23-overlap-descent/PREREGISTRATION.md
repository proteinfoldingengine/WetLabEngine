# v16.23 — Frozen overlap-descent verification

Frozen before implementing the new producer/verifier. Parent a02202bc218adb4080489c54dd37a1f9e5ec77d1 (v16.22), not the historical conditional quantum-response branch. Purpose: adjudicate signed overlap gluing, nonnegative membership, response compatibility, and whether these already-earned operations further restrict the parent solution space. Proof hypotheses are explicit in TYPE_LEDGER.md / PROOFS.md. No outcome is a fixed reporting flag.

## Universe and coverage

U1: every rooted unordered tree shape with 1..5 vertices. Producer: ancestor-first parent-array enumeration deduplicated by balanced-parenthesis rooted shape codes. Verifier: independent Pruefer-tree enumeration rooted at vertex 0 and shape-code deduplication. Counts are computed and compared, not used to manufacture records.

U2: the same four fine trees in inherited pruning_consistency_audit.py CASES, separately tagged regression instances. All root-containing ancestor-closed subsets are retained, including root and whole tree. No deduplication of isomorphic actual subsets within a carrier. Every ordered pair and every ordered triple of these subsets is covered, including repeated/nested views; the relevant union may be smaller than the initial X. General proofs concern all finite sizes; this bound is only implementation coverage.

For every pair preserve labels/domains, union/intersection, joint-readout matrix A, overlap-difference matrix D and proposed gluing matrix B, separately in full source and root-zero response coordinates. Require DA=0, BA=id, and AB=id on ker D, with exact rank/nullspace checks and correct dimensions, including zero-dimensional response carriers. Off-domain extensions B+KD are allowed if their restriction to compatible data is identical; do not reject harmless representational freedom.

For every triple verify two binary parenthesizations on the complete compatible-data space, repeat-view identities, inclusion-exclusion, and the joint-readout kernel ker P_XU. Reconstruct source coordinate selection and response classes rather than trusting declared pass fields. Record all triple keys or a reproducible coverage digest over the exact independently enumerated ordered keys.

Positive cone: for every ordered pair in U1/U2, enumerate ALL nonnegative integer local sources of total 0,1,2. Compare local overlap compatibility and the signed-gluing positivity criterion against independently enumerated nonnegative sources on the UNION at the same total. Exclude totals >2 and noninteger samples from bounded enumeration; the general rational-cone theorem is proved separately. Store per-pair counts and an explicit failure witness where one exists. Include the fixed three-node two-view and four-node triple-view witnesses from O5/O6, plus a genuinely feasible control. These are logical witnesses, not new physical models.

## Parent solution-space check

Load the complete v16.22 raw certificate, SHA256 59c2c2f6d1091e7102e51932ed4ee7827668d12db7f1b08ffb0724791c8df713. Test every certified unrestricted parent nullspace basis vector on every new pair-gluing diagram in U1 after justified isomorphism to the appropriate parent shape. Do not assume diagonal response in place of this check. General O4 covers every comparison-compatible family and shows which premise implication is tested. The fixed inverse remains unchanged.

## Metamorphic and deliberate-defect checks

Consistent root/parent-preserving relabeling plus storage reordering; non-permutation rational source/potential coordinate changes; replacing potentials by other representatives; swapping and repeating views; changing a gluer off the compatible domain. Reject wrong pushforward, wrong overlap, wrong gluer on compatible data, foreign Genesis, malformed parent/retained sets, floating/Boolean identifiers or coefficients, omitted pairs/triples, false positive feasibility, corrupt witnesses and omitted required fields. Include an ordinary linear section that is rejected for failing retained naturality under sibling exchange. Missing-module RED is only wiring evidence. Deliberate corruptions must be rejected for mathematical reasons.

## Computation and publication

Exact rational arithmetic only. GitHub: Python 3.11, SymPy 1.13.3 and mpmath 1.3.0. Separate producer and verifier modules; verifier imports no producer/enumerator and reconstructs maps from raw carriers. Unit/development tests precede campaign production; preserve RED. Run complete new suite and inherited v16.22, v16.21 and exact pruning suites. Archive commands, exit codes, source SHA, run/job/attempt, dependencies, source snapshots and invalid attempts. Durable repository evidence and fresh reproduction are required before completion.

Outputs distinguish execution status, input validity, scientific conclusion, proof status, and exact scope. A correctly certified negative feasibility result passes CI; wrong/incomplete inputs do not. Self-review must not be presented as separate review.

Time is pruning / ordered recoverability update. No metric, geometric target, new CPTP/Hilbert primitive, coupling fit, external alignment, or physical source law is introduced.
