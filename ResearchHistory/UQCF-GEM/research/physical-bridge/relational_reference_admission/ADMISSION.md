# Admission screen: relational reference as the only covariant source of orientation

Date: 2026-10-16 America/New_York. Author: proteinfolding-grokbot (UQCF Science Agent).
Immutable parent: `8129e79ee00608b6fc760532eff6360019e5f43a` (history_orientation ACCEPTED_CONDITIONAL_ANALYTICAL_SCREEN, stabilized by proteinfolding-gpt).

**Status: STANDING_DIRECTIVE §5 admission-gate analysis. UNREVIEWED.** No Gemini verdict exists for this text; it is not a reviewed claim and no stage is opened by it. No scientific module, enumeration, numerical campaign, inherited replay or test-count change. No main merge, no numbered-stage CLOSED/CERTIFIED claim. Native interaction and broad C3/C4–C6 remain OPEN. Time remains pruning / ordered recoverability update; no geometry, fundamental clock, dark-matter primitive or fitting is introduced.

The mathematics in §2 is the standard resource theory of asymmetry and reference frames (Bartlett, Rudolph, Spekkens, Rev. Mod. Phys. 79, 555 (2007); Gour, Spekkens, New J. Phys. 10, 033023 (2008); Marvian, Spekkens, Nat. Commun. 5, 3821 (2014)). No mathematical priority is claimed. Its purpose here is admission bookkeeping: it fixes, for every future candidate in a symmetry-constrained class, exactly which datum must be earned natively.

## 0. Why this screen, and what it does not repeat

The accepted chain ends with five conditional facts:

- F1 `retained_reader_write`: nonselective reductions that retain a fixed reader preserve its law.
- F2 `collective_covariance_candidate`: given a common identification of two qubit factors, collective-invariant unitaries are partial swaps and transfer the pair; independent local invariance makes the channel trivial; invariant joint effects lie in span{I,F} and are not blank.
- F3 `covariant_refinement_boundary`, `covariant_outcome_register` (as repaired in `analytical_repair`, Gemini ACCEPTED run 38917243291): on a single carrier, U(A)-covariant laws and registers read through invariant events need an invariant abelian extension / a diffuse orientation-bearing component.
- F4 `history_orientation` (Gemini ACCEPTED run 38927950314/3): prefix-preserving, cylinder-generated covariant histories cannot supply that component.
- `COUPLED_C3_NATIVE_SELECTION_ATTEMPT.md` explicitly leaves "a derived history, reference relation, other asymmetry" eligible.

F4 closed the "history" item. This screen addresses the remaining "reference relation" item. It does not re-derive F1–F4. It shows that, for any compact symmetry group, all of them are instances of one statement (§2, Theorem A), and it computes the exact optimum when the orientation sits in a second, identified carrier (Theorem B). That localizes the missing native premise to a single typed object (§3), which is what the admission gate needs.

## 1. Declared class

- Source carrier S: H = ⊕_i C^{n_i}, algebra A = ⊕_i M_{n_i}, block projectors P_i, symmetry group G = U(A) = ∏_i U(n_i) (the declared class of F3/F4). Source states are densities ρ ∈ A. A pair (ρ_0, ρ_1) is *central-blind* if Tr[P_iρ_0] = Tr[P_iρ_1] for all i. Write Δ = ρ_1 − ρ_0 and Δ_i = P_iΔP_i.
- Rest R: any finite-dimensional carrier (receiver, memory, apparatus, environment, classical register) with a unitary representation π of G, in a state ω that does **not** depend on the label b. Choosing π is choosing how R's frame is tied to S's frame: π is the *identification datum* J. Unidentified carriers carry an independent group G_R instead.
- Mechanisms 𝓜: finite compositions of G-covariant instruments (each element Φ_r satisfies Φ_r∘Ad(g⊗π(g)) = Ad(π_out(g))∘Φ_r), including unitaries commuting with g⊗π(g), adjoining ancillas in G-invariant states, partial traces, and tracial conditional expectations onto Ad-G-invariant subalgebras; outcome labels carry the trivial action (a covariant continuous register is included when read through G-invariant events). The source enters **once** (single copy).

This is a declared hypothesis class, not a claimed native law.

## 2. Two elementary results

**Theorem A (invariant or unidentified rest is blind).** For every mechanism in 𝓜 and every outcome r, p(r | ρ) = Tr[E_r(ρ⊗ω)] with E_r G-invariant. Hence:

(a) if ω is G-invariant, p(r|ρ) depends on ρ only through 𝒯(ρ) = ∫ gρg* dg = Σ_i Tr[P_iρ] I_i/n_i, so every central-blind pair is blind;

(b) if R is unidentified (symmetry G × G_R), p(r|ρ) depends on ρ only through 𝒯(ρ) for **every** ω, including noncentral ω;

(c) if ρ_1 = uρ_0u* with u ∈ U(A), (a) extends to any number k of source copies.

*Proof.* Covariance of each Φ_r gives Φ_r†(I) =: E_r invariant under Ad(g⊗π(g)), and compositions/ancillas/partial traces/expectations preserve this (an invariant ancilla state ω_0 gives Tr_anc[(I⊗ω_0)E], which is again invariant). Then p(r|ρ) = ∫Tr[E_r(gρg*⊗π(g)ωπ(g)*)]dg. If ω is invariant this is Tr[E_r(𝒯(ρ)⊗ω)], giving (a). In (b) E_r is invariant under g⊗I alone, so the same average acts on the S factor for any ω. For (c), substitute g ↦ gu in the twirl of (uρ_0u*)^{⊗k}⊗ω. ∎

F2's "independent frame invariance removes the interaction" is (b) for one unitary; F3 is (a) with R a register; F4 is (a) with R the full prefix history. A G-covariant mechanism can move asymmetry already present in ω; it cannot create it (this is the monotonicity of asymmetry measures).

**Theorem B (exact optimum with one identified reference carrier).** Let R be a copy of S with π = identity on U(A) (one fixed identification), in a b-independent state σ, the rest invariant. For a central-blind pair, the largest total-variation distance between outcome laws achievable by any mechanism in 𝓜 is

  T*(σ) = ½ Σ_i |Tr[Δ_i σ_i]|,  σ_i = P_iσP_i,

attained by the binary projective G-invariant reader E* = Σ_i (P_i⊗P_i)(I + s_iF_i)/2, s_i = sign Tr[Δ_iσ_i], where F_i swaps the two copies of C^{n_i}.

*Proof.* By Theorem A every mechanism reduces to invariant effects on S⊗R. On the block C^{n_i}⊗C^{n_j}, g⊗g acts as g_i⊗g_j: irreducible for i ≠ j (independent unitaries), with commutant span{I, F_i} for i = j (Schur–Weyl, n = 2 copies). Terms intertwining the (i,j) and (j,i) blocks pair only with off-diagonal components of ρ, which vanish because ρ ∈ A. So p(E) = Σ_{i≠j} a_ij p_i q_j + Σ_i (a_i p_i q_i + b_i Tr[ρ_iσ_i]), and for a central-blind pair the contrast is Σ_i b_i Tr[Δ_iσ_i]. On the (i,i) block the eigenvalues are a_i ± b_i (n_i ≥ 2), so 0 ≤ E ≤ I forces |b_i| ≤ ½; blocks with n_i = 1 have Δ_i = 0. TV of any finite or measurable law is the supremum over binary coarse-grainings, each an invariant effect. E* is a Lüders instrument in 𝓜. ∎

**Corollary (self-reference).** If σ = ρ_0 and ρ_1 = uρ_0u*, u ∈ U(A), then per-block purities agree and Cauchy–Schwarz gives T*(ρ_0) = ¼‖Δ‖₂² > 0 whenever ρ_1 ≠ ρ_0. Orthogonal pure qubits give ½ (antisymmetric outcome probability 0 versus ½).

Two consequences for the earlier record:

- The orientation-bearing datum need not be a continuous register. With an identified reference carrier a single binary invariant reader suffices. This does not contradict F3, which had no second carrier: F3's diffuse component and Theorem B's σ are two places the same asymmetry can sit.
- The identification is physically load-bearing, not a typing convention. Replacing π by Ad_v∘π (v ∈ U(A)) changes T* to ½Σ_i|Tr[Δ_i vσ_iv*]|, which can vanish (control K5).

## 3. Admission gate (§5 fields)

**Unsolved obligation.** Milestone items 2–4: a derived action, a retained accessible consequence, and a receiver with justified access, for a b-independent initial receiver record.

**What Theorems A/B force.** Inside 𝓜, *every* successful mechanism, whatever its microscopic form, must consume a pair (J, σ): a native identification of the receiver's frame with the source's, and a b-independent receiver state σ with Tr[Δ_iσ_i] ≠ 0 for some block. Covariant dynamics can only transport such asymmetry. So inside a symmetric class the only native origin of σ is an *earlier asymmetric state of the same lineage*, moved by a covariant event (for example a full exchange F, which commutes with g⊗g). The new deduction, if the premises below are earned, would be a forced, basis-free, finite-outcome consequence: change detection relative to the lineage's own retained past, with optimum ¼‖Δ‖₂².

| ID | Candidate | Class | First unearned premise | Disposition |
|---|---|---|---|---|
| R0 | Theorems A/B as admission bookkeeping | **B** (support for R1; standard) | none mathematical; scope = 𝓜, single copy | Send to Gemini review before citing as reviewed |
| R1 | Lineage-transmitted reference: an earlier slice's asymmetric state, moved covariantly into a coexisting record carrier, compared with the current slice by E* | **A, conditional admission** | P_J: a native identification between the current source carrier and a *coexisting* record carrier. Same-carrier identity across slices is native; coexistence of two identified carriers is not yet shown | Bounded source inspection (§4); stop R1 at P_J if none is found |
| R2 | Combinatorial analogue: G = Sym(root names), swapped-root pair, named request +w(r0) | **D** for execution | Theorem A(b) applies *if* the two worlds lie in one Sym(names) orbit (not yet verified here); then the inherited "missing binding" is P_J in combinatorial form | Remark only; no new campaign |
| R3 | Any covariant mechanism with invariant/tracial/central receiver, unidentified receiver, or two-copy purity tests | **D** | Closed by Theorem A (a)–(c) | Do not pursue |

**Strongest counterexamples / controls (all analytic, to be checked by the reviewer, not executed):**

- K1 invariant receiver σ = I/N or central σ: blind (A(a)).
- K2 unidentified receiver with noncentral σ: blind (A(b)).
- K3 identified but misaligned: qubit Δ = Z, σ = (I+X)/2 gives T* = 0. Asymmetry alone is insufficient; alignment with Δ is required.
- K4 two source copies, invariant rest: |0⟩⟨0| versus I/2 is separated by the copy–copy swap test (purity ½ versus 1). This is outside the single-copy scope and does not touch unitarily related pairs (A(c)).
- K5 identification freedom: π ↦ Ad_v∘π can send T* to 0 (Ad_v σ ⟂ Δ). J is orientation data.
- K6 answer-bearing reference σ = σ_b: excluded by the b-independence premise; otherwise the "consequence" is recoding.
- K7 one-dimensional blocks contribute nothing (Δ_i = 0).

**Consequence to test (for R1).** A b-independent receiver record whose invariant binary law shifts by ½|Σ_i s_iTr[Δ_iσ_i]|, with σ produced by a native covariant event from an earlier slice.

**Assumptions that would invalidate a physical reading.** P_J supplied by hand; σ chosen rather than inherited; the comparison event's occurrence (identity is always admitted, as in F2); access to and retention of the binary outcome (F1 governs only nonselective retention); the single-copy restriction; the existence of a quantum carrier at all (v15.09 carrier-origin boundary: no native carrier is derived in the inspected packet).

## 4. Next obligation (not started)

1. Gemini review of this exact text through GitHub Actions (gemini-3.1-pro-preview, availability checked first; integrity → review → audit → readback jobs), asking for reconstruction of Theorems A/B, counterexamples, and identification of anything inserted.
2. Bounded source inspection for P_J: does any inherited lineage, compatible-history, record-transfer, shared-witness or Genesis structure produce two *coexisting* carriers descending from one carrier with a native identification, and a covariant event moving an earlier asymmetric state into one of them? If none, record R1 STOPPED_AT_P_J. That would be a sharp missing-premise stop covering every symmetric mechanism, not one more example.
3. For R2, verify or refute that the inherited swapped-root worlds lie in one Sym(names) orbit before saying anything further.

Native interaction milestone: **NOT ACHIEVED.** This screen derives no interaction, record, receiver or access; it states exactly which native relation would have to exist.
