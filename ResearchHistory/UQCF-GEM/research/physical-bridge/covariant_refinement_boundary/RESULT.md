# Covariant refinement boundary: center growth needs a non-central orientation

**2026-10-16 repair notice:** This current text incorporates the corrections in `../analytical_repair/CORRECTIONS.md`. Original reviews, preregistrations and receipts remain unchanged historical evidence; their earlier verdicts do not certify these revised bytes. Fresh review and publication gates are pending.

Date: 2026-10-16 America/New_York. Parent: `b20429c2e692d3ea219ab44404366cdfa3a5b119`. Preregistration: `PREREGISTRATION.md`, commit `0243bcbbc68749c99564ea29e7a8b513bc84885e` (precedes this note).

**Bounded analytical no-go for a declared candidate class, plus an exact conditional characterization. Native milestone NOT ACHIEVED.** The author's informal sketch of Theorem 1 and the control list existed before preregistration and is disclosed there. The mathematics is elementary and standard (adjoint irreducibility, Schur's lemma, the reference-frame/superselection lesson of Bartlett–Rudolph–Spekkens, Rev. Mod. Phys. 79, 555 (2007)); no mathematical priority is claimed. Covariance is a declared hypothesis defining the tested class, NOT a claimed native law.

## 1. Question
`center_growth_law_screen` left open a source-independent law Φ selecting A_{k+1} from A_k with strict center growth. The natural formal reading of "source-independent, no inserted geometry or basis" is covariance: the law may use only data that it carries along when the whole carrier is rotated. This note asks what such laws can do.

Setting: finite-dimensional H; A = A_k ≅ ⊕_{i=1}^r M_{n_i} (each block with its multiplicity space), central atoms z_i, Z(A) = span{z_i}. U(A) = unitary group of A, G ⊆ U(A) a subgroup, acting on A by Ad g(a) = gag*. sl_{n_i} = traceless part of block i.

Class 𝓛_G: Φ(A, X) = B is a unital *-subalgebra with Z(A) ⊆ B ⊆ A (inherited center retention, P1b of `center_access_growth`), where X is any source-independent datum carried by a U(H)-action, and Φ(gAg*, g·X) = gΦ(A,X)g* for all g ∈ U(H). Let G_X = {g ∈ U(A) : g·X = X}.

Lemma 0. B is Ad(G_X)-invariant. Proof: for g ∈ U(A), gAg* = A; so B = Φ(A,X) = Φ(gAg*, g·X) = gBg* whenever g·X = X. ∎ (History dependence is covered: U(A_k) ⊆ U(A_j) for j ≤ k, so every g ∈ U(A_k) fixes the whole history A_0 ⊇ … ⊇ A_k.)

## 2. Results
**Proposition 1 (exact reduction).** For any G ⊆ U(A) the following are equivalent: (i) some Ad(G)-invariant unital *-subalgebra B with Z(A) ⊆ B ⊆ A has Z(B) ⊋ Z(A); (ii) some Ad(G)-invariant abelian *-subalgebra D with Z(A) ⊊ D ⊆ A exists.
Proof. (i)⇒(ii): D = Z(B); Ad g restricts to an automorphism of B, which maps Z(B) onto Z(B). Z(A) ⊆ B and Z(A) commutes with A ⊇ B, so Z(A) ⊆ Z(B). (ii)⇒(i): B = D, Z(D) = D. ∎

**Theorem 1 (covariant no-growth).** If for every block with n_i ≥ 2 the block projection of G acts irreducibly on sl_{n_i} by conjugation, then every B satisfying (i)'s premises has Z(B) = Z(A). In particular this holds for G = U(A).
Proof. Suppose D is as in (ii). Since z_i ∈ D, D = ⊕_i z_i D, each z_i D an Ad(G)-invariant abelian unital *-subalgebra of block i, and some z_i D ⊋ ℂ z_i (so n_i ≥ 2). For X ∈ z_i D, X − (tr X/n_i) z_i ∈ z_i D, so z_i D = ℂz_i ⊕ V_i with V_i = z_i D ∩ sl_{n_i} a nonzero Ad(G)-invariant subspace. Irreducibility forces V_i = sl_{n_i}, which is not abelian for n_i ≥ 2 (e.g. E_12, E_21 do not commute). Contradiction. For G = U(A) the block projection is U(n_i), whose adjoint representation on sl_{n_i}(ℂ) is irreducible (standard). ∎

**Corollary 1 (no accessible consequence; iteration).** Under any law in 𝓛_{U(A_k)} with G_X ⊇ U(A_k) (no datum, or any U(A_k)-invariant datum: central elements, the tracial state, elements of A_k', and any classical label such as the combinatorial laminar tree or incidence record, which are determined by the centers), Z(A_{k+1}) = Z(A_k). By `center_access_growth` Theorem (b), every pair blind at stage k stays blind at k+1 (δ_TV = 0). If every step is such a law, Z(A_m) = Z(A_0) for all m; from the trivial-center seed every pair is blind at every stage. Noncentral information may still be destroyed (block collapse, K8), but nothing becomes accessible.

**Proposition 2 (randomized laws with unretained choice).** Let G be compact, and let μ be an Ad(G)-invariant probability measure on labelled choices ω ↦ (B_ω; z_1(ω),…,z_r(ω)), each B_ω center-retaining and z_j(ω) a labelled family of atoms of Z(B_ω) (fixed finite r, measurable). If the label ω is not retained, the readout law is p_b(j) = Tr(Z̄_j ρ_b) with Z̄_j = ∫ z_j(ω) dμ(ω) ∈ A ∩ G'. If A ∩ G' = Z(A) (true for G = U(A), since unitaries span A; more generally whenever the only elements of A commuting with G are central), every pair blind at stage k has p_0 = p_1.
Proof. Tr(z E_{B_ω}(ρ)) = Tr(zρ) for z ∈ B_ω, so p_b(j) = ∫Tr(z_j(ω)ρ_b)dμ = Tr(Z̄_jρ_b). For g ∈ G, gZ̄_jg* = ∫ z_j(g·ω) dμ(ω) = Z̄_j by invariance; Z̄_j ∈ A by convexity/closure. If Z̄_j ∈ Z(A), blindness gives Tr(Z̄_jΔ) = 0. ∎
Note the weaker hypothesis: Schur irreducibility (A ∩ G' = Z(A)) suffices here but NOT for Theorem 1 (K5).

**Proposition 3 (state-relative covariant law; exact growth).** For a source-independent reference state ω on H define Φ(A, ω) = A ∩ {E_A(ω)}', E_A the inherited tracial conditional expectation. This law is U(H)-covariant (E_{gAg*}(gωg*) = gE_A(ω)g*) and center-retaining (E_A(ω) ∈ A commutes with Z(A)). Writing z_i E_A(ω) = Σ_λ λ e_{iλ} (spectral projections), Z(Φ(A,ω)) = span{e_{iλ}}. Hence Z grows iff E_A(ω) ∉ Z(A), and for a pair blind at stage k the acquired contrast is δ_TV = ½ Σ_{i,λ} |Tr(e_{iλ}Δ)| (by `center_access_growth` (b)). Proof: Φ(A,ω) = ⊕_{i,λ} e_{iλ} A e_{iλ}, whose center is spanned by the e_{iλ}. ∎
Consequence: retaining the full inner-unitary stabilizer forbids growth. Merely reducing that symmetry is NOT sufficient: K6 supplies a counterexample. Proposition 1 gives the exact criterion--the stabilizer must admit a nontrivial invariant abelian extension of Z(A). A noncentral Hermitian reference provides one sufficient construction through Proposition 3; the tracial reference is inert (K4). No such datum or selection law is derived as native here.

## 3. Controls (exact hand calculations; nothing executed)
- K1 Fixed basis (positive non-vacuity, rejected as native). A = M_2, B = diag. Grows ℂI → span{|0⟩⟨0|,|1⟩⟨1|}; pair |0⟩/|1⟩ gets δ_TV = 1. Ad(Hadamard) maps B to the Hadamard-diagonal algebra ≠ B, so the law is not U(2)-covariant. The basis is inserted geometry.
- K2 Collective tensor split (separating; reconciles `center_access_growth` C4). A = M_4 = M_2 ⊗ M_2, G = {U ⊗ U}. As a G-module M_4 ≅ (1⊕3)⊗(1⊕3) = 1⊕3⊕3⊕(1⊕3⊕5), with two-dimensional trivial part span{I, F}. D = span{I,F} is invariant and abelian, so growth is allowed; the adjoint action of G on sl_4 is reducible. Consistent with Theorem 1: the tensor factorization/common representation is the supplied orientation.
- K3 State centralizer (outside the common-chain hypothesis, not an identical-state counterexample). The COMMON function Φ(A,ρ)=A∩{ρ}' gives the SAME algebra on identical states; for ρ=|0⟩⟨0| in M_2 both outputs are the same two-dimensional diagonal algebra. For distinct states it may select different algebras, outside the common-chain hypothesis P8. A single input-state-dependent rule is distinct from externally selecting different rules by the source label: only the latter can manufacture the C3 identical-input artefact. The centralizer prescription still supplies a generally nonlinear state-to-algebra map without a derived physical implementation; this is the unresolved operational premise, not an identical-state contrast.
- K4 Tracial reference (inert, inherited). ω = I/d gives E_A(ω) ∈ Z(A), Φ(A,ω) = A: no growth. The inherited RAS tracial structure carries no orientation.
- K5 Pauli covariance (sharpness of Theorem 1). G = Pauli group on M_2 is Schur-irreducible (G' = ℂI) but Ad G on sl_2 splits into the three lines ℂX, ℂY, ℂZ. D = span{I,Z} is G-invariant and abelian: a G-covariant algebra law grows the center and separates |0⟩/|1⟩ (δ_TV = 1). The discrete Pauli frame is a supplied orientation. Under Proposition 2 any G-invariant labelled randomization has Z̄_j ∈ A ∩ G' = ℂI (on the diag orbit, X and Y exchange the two labels, giving Z̄_j = I/2), hence blindness; the deterministic labelled readout of the fixed Z axis is exactly where the frame enters.
- K6 Real-orthogonal covariance (reducibility not sufficient). A = M_3, G = SO(3). sl_3 = (antisymmetric, spin 1) ⊕ (symmetric traceless, spin 2), irreducible and inequivalent, so the invariant subspaces are 0, so(3)_ℂ, S, and their sum. None is abelian (so(3) is nonabelian; in S, diag(1,−1,0) and E_12+E_21 do not commute). No growth despite a reducible adjoint action: the converse of Theorem 1 fails, and the exact criterion is Proposition 1(ii).
- K7 Center erasure (outside class). A = M_2 ⊕ M_2, B = ℂI is U(A)-invariant but drops p = diag(1,1,0,0): retention fails (Tr pE_B(p/2) = 1/2 ≠ 1). Covariance without retention loses access instead of creating it.
- K8 Block collapse (inside class, inert). B = ⊕ ℂ z_i is U(A)-invariant and retaining; Z(B) = Z(A). Noncentral information is pruned; no access is gained.
- K9 Haar-random basis (probabilistic). A = M_2, ω a Haar-random labelled basis (u_1,u_2), B_ω its diagonal algebra. Unretained: Z̄_1 = E|u_1⟩⟨u_1| = I/2, so |0⟩ vs |1⟩ gives p = (1/2,1/2) for both: blind (Proposition 2). Retained: conditioned on ω, contrast |⟨u_1|0⟩|² − |⟨u_1|1⟩|² generically ≠ 0; the retained label is a supplied reference frame.
- K10 Ensemble-mean reference (separating). ω = ρ̄ = (ρ_0+ρ_1)/2 is b-independent but presupposes the whole source pair. Pure pairs: with phases aligned so ⟨ψ_0|ψ_1⟩ ≥ 0, the unitary R swapping ψ_0 ↔ ψ_1 on their span (identity on the complement) commutes with ρ̄, so it preserves each eigenspace; hence |⟨e|ψ_0⟩| = |⟨e|ψ_1⟩| on nondegenerate eigenvectors, and the degenerate (orthogonal) case has the span projector as atom with weight 1 for both: always blind. Mixed pair ρ_0 = |0⟩⟨0|, ρ_1 = I/2 in M_2: ρ̄ = diag(3/4,1/4), atoms |0⟩⟨0|,|1⟩⟨1|, Tr(|0⟩⟨0|Δ) = −1/2, δ_TV = 1/2. Growth with contrast is possible, but the reference is ensemble-supplied, not native.

## 4. Premise provenance
| # | Premise | Status |
|---|---|---|
| P0 | finite-dimensional H | SUPPLIED (inherited interface) |
| P1b | center retention Z(A) ⊆ B | SUPPLIED (inherited condition) |
| Q1 | covariance of Φ under U(H) (class definition) | DECLARED hypothesis, not claimed native |
| Q2 | Theorem 1, Corollary 1 | DERIVED (from Q1, P1b, standard adjoint irreducibility) |
| Q3 | Proposition 2 | DERIVED (from invariance of μ, compactness) |
| Q4 | Proposition 3 growth criterion | DERIVED; the reference ω is SUPPLIED |
| P2 | central reader Z(A) | SUPPLIED (unchanged from `center_access_growth`) |
| P8 | source independence of the chain | required hypothesis |

## 5. What this establishes and what it does not
Established (bounded): within center-retaining refinement laws, covariance under the current algebra's inner unitaries forbids strict center growth, hence forbids any new accessible central contrast, at every stage and along any chain of such laws; unretained covariant randomness is likewise blind under the weaker Schur condition. Growth requires a datum whose stabilizer in U(A) has a reducible adjoint action admitting an invariant abelian extension of Z(A) (Proposition 1(ii)); the canonical state-relative form is Proposition 3. Every control that grows the center (K1, K2, K5, K9-retained, K10-mixed) does so through a named supplied orientation or a source-dependent/ensemble-supplied reference.

Not established: that native laws must be covariant (Q1 is a class definition); that no native orientation datum exists; any physical symmetry-breaking mechanism; infinite-dimensional or non-tracial-expectation analogues; multi-step randomized iteration (Proposition 2 is single-step). No archive-wide absence claim.

## 6. Disposition
**INNER_COVARIANT_REFINEMENT_CANNOT_GROW_CENTER; CENTER_GROWTH_REQUIRES_NONCENTRAL_SOURCE_INDEPENDENT_ORIENTATION; NATIVE_MILESTONE_NOT_ACHIEVED** (frozen outcome O1, BOUNDED_NO_GO).

The open obligation sharpens again: a native datum and selection law whose stabilizer permits the invariant abelian extension in Proposition 1, plus justified central access P2. A justified noncentral Hermitian reference is sufficient for the specified centralizer construction; arbitrary symmetry reduction alone is not sufficient. Do not insert a basis, tensor split, Pauli frame or reference state to discharge it.

Analytical only: no numerics, simulation, enumeration, module import or replay; no inherited stack run. No CLOSED/CERTIFIED status, physical law, force, energy, geometry, dark-matter primitive or fundamental clock is claimed. Time remains pruning / ordered recoverability update. Path A active; broad C3/C4–C6 OPEN.

Missing AGENTS requirements (explicit): no workflow SHA; no pinned full-stack GitHub run; no execution artifacts or reproduced bytes; argument review is same-lineage (disclosed in review); no PR or merge audit.

## 7. Sources (bound in `source_packet.json` / `source_identities.json` at parent `b20429c2`)
1. `ResearchHistory/UQCF-GEM/AGENTS.md`
2. `physical-bridge/NATIVE_EVENT_MILESTONE.md`
3. `physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` (parent bytes)
4. `physical-bridge/record_compatibility_bridge/RESULT.md`
5. `physical-bridge/retained_reader_write/RESULT.md`
6. `physical-bridge/collective_covariance_candidate/RESULT.md`
7. `physical-bridge/center_access_growth/RESULT.md`
8. `physical-bridge/center_growth_law_screen/RESULT.md`
