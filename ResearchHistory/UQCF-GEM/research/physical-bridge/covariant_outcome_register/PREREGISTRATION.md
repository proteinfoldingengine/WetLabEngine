# Preregistration — covariant outcome register (analytical stage)

Date: 2026-10-16 America/New_York (~09:20 ET). Branch: `research/uqcf-overlapping-guard-exchange`.
Verified parent (git fetch + rev-parse vs origin): `b2a78583eb14930f775e29b8eb05293810f1b098` (audited covariant_refinement_boundary receipt; tree `3b2351e5d13d8ee915e9d1741950360e334452bd`).
Workflow SHA: none (analytical stage). Scientific checked-out SHA: `b2a78583eb14930f775e29b8eb05293810f1b098`.

**Status at commit time: prospective for this stage's RESULT.** No RESULT draft for this stage is committed. Exploratory knowledge is disclosed below and is not a preregistered prediction.

## Motivation
`covariant_refinement_boundary` (Theorem 1) proved that center-retaining refinements B ⊆ A covariant under U(A_k) cannot grow the center; its review (R2) left carrier-ENLARGING refinements (B ⊄ A) eligible, and its Proposition 2 showed covariant randomization with an UNRETAINED choice is blind. Open question: does a retained-outcome covariant refinement — adjoining a classical outcome register through a U(A)-covariant instrument — force an accessible, retained, probabilistic consequence for a blind pair without any supplied orientation, needing only a unitary-INVARIANT datum? Where must that datum come from?

## Already-known findings (disclosed; NOT preregistered predictions)
1. `center_access_growth` (conditional): under supplied center retention and supplied central reader P2, a pair blind at stage k is distinguished at k+1 iff some new central atom z' has Tr(z'Δ) ≠ 0; δ_TV = ½Σ|Tr(z'Δ)|.
2. `covariant_refinement_boundary`: Theorem 1 (U(A)-covariant center-retaining B ⊆ A cannot grow Z(A)); Proposition 2 (unretained covariant randomization blind when A ∩ G' = Z(A)); Proposition 3 (state-relative growth needs a non-central reference; tracial reference inert); K9 (Haar-random basis: unretained blind, retained label "a supplied reference frame"); K5/K6 sharpness controls; review R2 leaves B ⊄ A eligible.
3. `collective_covariance_candidate`: partial-swap class gives sin²θ contrast with no uniform positive lower bound; `retained_reader_write`: fixed retained readers keep their law under nonselective reduction.
4. **Author exploratory sketch S1–S6 (given with the task; disclosed):**
   - S1 covariant POVMs on M_n under U(n) are E(dg) = g P0 g* dg, P0 ≥ 0, Tr P0 = n (Holevo-type); the family is fixed by the invariant spectrum of P0.
   - S2 retained register = carrier enlargement A → A ⊗ L^∞(outcomes); TV = ½∫|Tr(gP0g*Δ)|dg > 0 for every traceless Δ ≠ 0 iff P0 non-scalar; scalar seed inert.
   - S3 qubit rank-1 seed: TV = |δ|/4 = D/2 (half of Helstrom).
   - S4 rank-1 seed, general n: E_ψ⟨ψ|Δ|ψ⟩² = TrΔ²/(n(n+1)), TV ≥ ‖Δ‖₂²/(2(n+1)‖Δ‖_∞).
   - S5 unretained register gives a blind nonselective channel (reconciles Prop. 2); the realized outcome is an orientation earned per history, invariant in ensemble.
   - S6 candidate inherited source of the invariant datum: rank of an active support after a pruning deletion, seed (n/m)Π_m; instrument act and register access NOT derived.
5. **Author pre-commit exploratory derivations (worked out after reading the parent sources and before this commit; disclosed, NOT preregistered):**
   - S7 a finite (or discrete, continuous-action) register cannot carry a nontrivial U(A)-action (U(A) is compact connected, every element is a k!-th power), so a covariant instrument with a finite register has central effects and is blind; more generally a finite-dimensional covariant enlargement read through its center is blind. This suggests S2 holds only for continuous registers.
   - S8 a Radon–Nikodym reduction writing any covariant POVM's TV as a ν-average of regular-seed TVs; consequence in the qubit: TV ≤ D/2 for every covariant register (and every retained covariant chain).
   - S9 hand values: orthogonal pure pair, rank-1 seed, any n: TV = ½ (= D/2); pure vs maximally mixed: TV = (1−1/n)^n; M_2 ⊕ M_2 equal-weight rank-1 seeds: TV = D/3.
   - S10 under reduced covariance SO(3) on M_3, a real rank-1 seed is blind to an imaginary-antisymmetric Δ while a complex (helicity) rank-1 seed gives TV = 3/4 = 3D/4.
   These are sketches to be checked by typed proof in RESULT; any that fail are to be recorded as RED.

## Frozen objects
- Finite-dimensional H (inherited interface); current algebra A = A_k ≅ ⊕_i M_{n_i} (multiplicities absorbed into the A-reduced state ρ^A = ⊕ρ_i); central atoms z_i; U(A) = ∏U(n_i) with Haar probability dg.
- Declared class 𝓘_G of G-covariant instruments with retained classical outcome register: a standard Borel G-space Ω with jointly measurable action, a POVM E on Ω with effects in A (WLOG, since a reader acting after the stage-k reduction E_A is equivalent to its E_A-image), covariant E(gB) = gE(B)g* for g ∈ G; the register is the classical algebra L^∞(Ω, E) adjoined to A, so the enlarged center contains Z(A) ⊗ L^∞(Ω). Canonical G = U(A); also the regular case Ω = G (left translation) and seed P0 ∈ A⁺ with block traces Tr P0_i = n_i. Finite-dimensional variant: a covariant unital CP map T*: C → A from a finite-dimensional algebra C carrying an action α of G by *-automorphisms, read through Z(C).
- Seed P0 (invariant datum = its per-block spectrum / G-orbit).
- Source pair ρ_0, ρ_1 (supplied), Δ = ρ_1 − ρ_0, blind at stage k (Tr z_iΔ = 0 ∀i, i.e. each Δ_i traceless).
- Contrast: total-variation distance δ_TV of the two register laws; Helstrom D = ½‖Δ^A‖₁.

## Primary objective
Decide with typed proof or explicit counterexample whether a U(A)-covariant instrument with retained outcome register forces δ_TV > 0 for blind pairs using only an invariant seed datum (no supplied orientation), give the exact necessary and sufficient condition, and identify what is supplied (instrument act, register, access, seed source).

## Diagnostic objectives
(a) Necessity/sufficiency of a non-scalar seed. (b) Exact qubit constant. (c) General-n bound (verify S4). (d) Block (non-factor) case: covariance under ∏U(n_i); seed must be non-scalar on some block where Δ's block part is nonzero. (e) Retained vs unretained register. (f) Iteration / chains of covariant instruments. (g) Finite vs continuous registers (S7). (h) Where the invariant datum could come from (S6), with provenance.

## Competing outcomes (frozen)
- O1 INVARIANT_SPECTRAL_SEED_SUFFICES_FOR_RETAINED_OUTCOME_CONTRAST (conditional: instrument act and register access supplied; milestone NOT achieved unless both derived).
- O2 ORIENTATION_STILL_REQUIRED (sketch false: no covariant retained register distinguishes a blind pair without a supplied orientation).
- O3 DEGENERATE (re-proves standard measurement, or smuggles a basis).
- O4 NATIVE_MILESTONE (instrument, seed and access all derived from inherited structure — only if genuinely true).
- O5 CONTINUUM_REGISTER_REQUIRED (qualifier, may co-occur with O1): finite-dimensional covariant enlargements are blind; contrast exists only with an infinite (continuous) retained register.

## Controls (frozen, analytic hand calculations)
K1 scalar seed P0 = I inert; K2 unretained register (nonselective covariant channel) blind; K3 fixed-basis non-covariant measurement (distinguishes, supplied orientation → rejected for class); K4 source-dependent seed P0 = f(ρ_b) (excluded, source-supplied); K5 register erased after write (blind); K6 qubit exact TV = D/2 check; K7 block algebra M_2 ⊕ M_2 with Δ having only cross-block/central components vs block-traceless components; K8 reducible covariance (SO(3) on M_3) seed behaviour; K9 duplicated / substituted outcome record (false provenance: register relabelled by a source-dependent permutation); K10 pruning-rank seed (n/m)Π_m and whether the rank is inherited or supplied.

## Resource and stopping rules
Analytical only: no numerics, simulation, enumeration, module import or replay; exact hand calculations only. Stop after RESULT + INDEX_APPEND + continuation append; then argument review, publication audit, receipt and author readback by separate agents. No CLOSED/CERTIFIED; no PR, merge or deletion. No new primitive: covariance and the register are declared class hypotheses, NOT claimed native laws. Supplied inputs are not promoted to discoveries. Time remains pruning / ordered recoverability update; no inserted geometry, fundamental clock, dark-matter primitive or heuristic fitting.
