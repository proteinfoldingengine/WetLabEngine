# Preregistration — covariant refinement boundary (analytical stage)

Date: 2026-10-16 America/New_York (~06:10 ET). Branch: `research/uqcf-overlapping-guard-exchange`.
Verified parent (git fetch + rev-parse vs origin): `b20429c2e692d3ea219ab44404366cdfa3a5b119` (audited center_growth_law_screen receipt).
Workflow SHA: none (analytical stage). Scientific checked-out SHA: `b20429c2e692d3ea219ab44404366cdfa3a5b119`.

**Status at commit time: prospective for this stage's RESULT.** No RESULT draft for this stage is committed. Exploratory knowledge is disclosed below and is not a preregistered prediction.

## Already-known findings (disclosed; NOT preregistered predictions)
1. `center_access_growth` (conditional): under supplied center retention Z(A_k) ⊆ A_{k+1} and supplied central reader P2, a pair blind at stage k becomes distinguishable at k+1 iff some new central atom z' has Tr(z'Δ) ≠ 0. Growth step P1a and reader P2 SUPPLIED.
2. `center_growth_law_screen`: no inspected source derives a source-independent law Φ selecting A_{k+1}, nor justified Z(A) access. Eligible re-entry includes "a precise impossibility for a bounded candidate class".
3. `center_access_growth` C4: the swap commutant {X : XF = FX} ⊆ M_4 grows the center from ℂI to span{I,F}; that law is invariant under the collective group U⊗U only.
4. **Author exploratory sketch (disclosed before this commit):** the author has an informal sketch that a center-retaining refinement law covariant under the full inner unitary group U(A_k) cannot enlarge the center (via irreducibility of the adjoint action on traceless block matrices), together with candidate controls (fixed basis, collective/tensor, Pauli, real-orthogonal, tracial reference, source centralizer, ensemble-mean reference, randomized basis). This sketch is NOT counted as a preregistered prediction; the frozen outcomes below remain open until RESULT.

## Frozen objects
- Finite-dimensional H (inherited conditional interface); current algebra A = A_k = ⊕_i M_{n_i} ⊗ I (unital *-subalgebra of B(H)); center Z(A).
- Declared candidate class 𝓛_G: refinement laws Φ assigning to A (and optionally to source-independent data X on which U(H) acts) a unital *-subalgebra B = Φ(A, X) with Z(A) ⊆ B ⊆ A (inherited center retention), covariant: Φ(gAg*, g·X) = gΦ(A,X)g* for g in a declared group. Canonical case: G = U(A), X absent or U(A)-invariant.
- Randomized variant: a probability measure on labelled choices (B, z_1..z_r), invariant under Ad G, with the choice label not retained.
- State-relative variant: B = A ∩ {E_A(ω)}' for a source-independent reference state ω.
- Source pair ρ_0, ρ_1 (supplied), Δ = ρ_1 − ρ_0, blind at stage k.

## Primary objective
Determine, with typed proof or explicit counterexample, whether any law in 𝓛_{U(A)} can strictly enlarge Z(A) and hence (via center_access_growth) produce an accessible contrast for a blind pair; if not, characterize exactly what symmetry-breaking datum is necessary.

## Diagnostic objectives
(a) Sharpness of hypotheses: is Schur irreducibility of G sufficient? is reducibility of the adjoint action sufficient for growth? (b) Randomized laws with unretained choice. (c) State-relative laws, including the inherited tracial reference and an ensemble-mean reference. (d) Iteration along a chain.

## Competing outcomes (frozen)
- O1 BOUNDED_NO_GO: no U(A)-covariant center-retaining law enlarges the center; blind pairs stay blind; necessary symmetry-breaking datum characterized. Milestone NOT ACHIEVED (the no-go applies only to the declared class).
- O2 COVARIANT_GROWTH_EXISTS: some U(A)-covariant center-retaining law enlarges the center → derive its accessible consequence and audit its premises (may approach the milestone).
- O3 DEGENERATE: the class is vacuous or ill-posed, or the result re-proves center_access_growth / smuggles a basis.

## Controls (frozen, analytic hand calculations)
K1 fixed computational basis M_2 → diag; K2 collective swap commutant in M_4; K3 source centralizer A ∩ {ρ_b}'; K4 tracial reference; K5 Pauli-covariant law on M_2; K6 real-orthogonal SO(3) covariance on M_3; K7 center erasure B = ℂI in M_2 ⊕ M_2; K8 block collapse B_i = ℂI_{n_i}; K9 Haar-randomized basis with unretained/retained label; K10 ensemble-mean reference for pure and mixed pairs.

## Resource and stopping rules
Analytical only: no numerics, simulation, enumeration, module import or replay. Stop after RESULT + INDEX_APPEND + continuation append; then argument review, two-stage publication audit, receipt, author readback. No CLOSED/CERTIFIED; no PR, merge or deletion. No new primitive; covariance is a declared class hypothesis, NOT a claimed native law. Time remains pruning / ordered recoverability update.
