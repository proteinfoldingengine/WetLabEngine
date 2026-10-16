# Preregistration — center access growth (analytical stage)

Date: 2026-10-15/16 America/New_York (revised 2026-10-16 00:15 ET). Branch: `research/uqcf-overlapping-guard-exchange`.
Verified parent (git ls-remote, gh authenticated as proteinfoldingengine): `d63aea606eb9e73bab812aef2934f799f3bb281a` (receipt commit of `collective_covariance_candidate`; its scientific commit is `64c2ac3c0957b743201977df0a2a7054cd8bec20`).
Workflow SHA: none (no workflow run is part of this analytical stage). Scientific checked-out SHA: `d63aea606eb9e73bab812aef2934f799f3bb281a`.
Drafting history (disclosed): a first draft was written on 2026-10-15 against parent `0583236e…` while gh was unauthenticated; it was never committed. This revision rebases it on `d63aea6`.

**Status: DRAFT, NOT YET COMMITTED.** It must be committed alone, before `RESULT.md`, once gh login is available.

## Already-known findings (disclosed; NOT preregistered)
The following were obtained by direct reasoning in the 2026-10-15 orientation report before this document existed. They are exploratory and must never be relabelled as preregistered predictions:
1. Under center retention Z(A_k) ⊆ A_{k+1}, centers nest: Z(A_k) ⊆ Z(A_{k+1}) (inherited from `record_compatibility_bridge/RESULT.md` §2).
2. Proposed route: take the stage-k accessible reader to be R_k = Z(A_k); a blind source pair can become distinguishable on R_{k+1}, and the inherited tracial identity then retains that law.
3. Sketched controls: non-growing center, center erasure, source-chosen chain, swap outside reader, trivial-seed M_2 → diagonal.
4. Objections 1–6 of that report, especially Objection 1 (the chain growth is supplied by RAS).
5. The full first draft of RESULT.md (theorem (a)–(d), provenance table, controls C1–C5, Objection 1 section, disposition O2) existed before this preregistration is committed. Its results are therefore ALREADY KNOWN, not predictions. The preregistration is retained to freeze scope, controls and claim boundaries, not to claim prospective discovery.
6. Published after the first draft, in `collective_covariance_candidate` (`64c2ac3`, receipt `d63aea6`): under common SU(2) invariance a two-qubit unitary is a partial swap, with memory contrast sin^2θ on |00>/|10>. Every V⊗V-invariant effect lies in span{I,F}, and P_- has input probabilities 0 and 1/2 that are already present and retained ("not an initially blank acquired record"). This bears directly on control C4 and is read before revision.

## Frozen objects
- Finite-dimensional H; GIVEN unital *-subalgebra chain A_0 ⊇ … ⊇ A_n of B(H) with Z(A_k) ⊆ A_{k+1}.
- E_k: ordinary-trace-preserving conditional expectation onto A_k.
- Reader premise P2: R_k = Z(A_k), readout = central-atom POVM of Z(A_k).
- Source pair ρ_0, ρ_1 (density matrices), Δ = ρ_1 − ρ_0, blind at stage k: Tr(zΔ)=0 ∀ z ∈ Z(A_k).

## Primary objective
State and prove (general proof, finite dimension): retention of every R_j law under the nonselective chain, and an exact iff criterion for stage-(k+1) acquisition, with its sector-sum constraint.

## Diagnostic objective
Classify each premise as DERIVED (from inherited published results) or SUPPLIED, and assess Objection 1.

## Competing outcomes (frozen)
- O1 DERIVED_ACCESS: chain growth and reader premise both derived from inherited native premises → milestone candidate.
- O2 CONDITIONAL_ACCESS: theorem holds but growth and/or reader premise remain supplied → milestone NOT ACHIEVED.
- O3 DEGENERATE: the theorem gives no contrast beyond restating a supplied answer, or a control fails.

## Controls (frozen, analytic only)
C1 non-growing center; C2 center erasure; C3 source-chosen chain; C4 swap outside reader; C5 trivial-seed M_2 → diagonal positive case (incl. partial and coherence-blind sub-cases).

## Resource and stopping rules
Analytical only. No numerics, simulation, enumeration, module import or historical replay. Stop after note + continuation append; then independent review and two-stage publication audit (separately authorized). No CLOSED/CERTIFIED status; no PR, merge or deletion.
