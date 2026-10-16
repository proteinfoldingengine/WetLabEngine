# Argument review: covariant refinement boundary

**Disposition: ACCEPT_FOR_BOUNDED_ANALYTICAL_PUBLICATION; no blocking objections; milestone NOT ACHIEVED.**

Review date: 2026-10-16 America/New_York. **Independence limitation (disclosed):** same agent lineage as the note author; a separate adversarial pass over the frozen draft bytes, not organisational independence. It does not satisfy AGENTS algorithmic-independence for numbered-stage closure.

## Bound objects (draft bytes at note commit `bce117d1949e22d8b420c594b9a969a251f7ac41`)
- RESULT.md SHA-256 `53c15cecb609e6c97e31641cc27b321b3b3ae3c25437a2a39f15d6f9638557f1`
- INDEX_APPEND.md `26bb60880f5b91231ac06c2078e541242716e7809f0823f984549005d3a05b39`
- PREREGISTRATION.md `6b03a654265c363f98993a3235ed80e8a70ef94c661fc07e8a4e7521006b0b14`
- source_packet.json `66c9224a3414924f8c1d388a6a13bbfd82ebef707ada5cc9e66d9b218f558d0d`
- source_identities.json `c999a6361318aa20f4684b5247fcad3cf5ba2c95f5852652e904530ac69ac593`
- continuation `41c54d7188c56758d12aa8b87e2a9c19f80ff45f2a1817b43cf665824e55836c`
Parent `b20429c2e692d3ea219ab44404366cdfa3a5b119`. Preregistration commit `0243bcbbc68749c99564ea29e7a8b513bc84885e` precedes the note; the author's exploratory sketch is disclosed there and not relabelled as prediction.

## Re-derivation
1. Lemma 0: g ∈ U(A) fixes A, so covariance plus g·X = X gives gBg* = B. History: U(A_k) ⊆ U(A_j) for j ≤ k because A_k ⊆ A_j. Checked.
2. Proposition 1: Ad g is an automorphism of B, so preserves Z(B); Z(A) ⊆ Z(B) because Z(A) ⊆ B and commutes with A ⊇ B. Converse trivial. Checked.
3. Theorem 1: z_i central, so z_iD is invariant; traceless part V_i is a *-closed invariant subspace; irreducibility forces V_i = sl_{n_i}, nonabelian for n_i ≥ 2. Irreducibility of the U(n) adjoint action on sl_n(ℂ) is standard. Checked.
4. Proposition 2: invariance of μ gives gZ̄_jg* = Z̄_j; A ∩ U(A)' = Z(A) since unitaries span A. Readout via Tr(zE_B ρ) = Tr(zρ) for z ∈ B. Checked; single-step only, as stated.
5. Proposition 3: E_A(ω) ∈ A commutes with Z(A); centralizer of a self-adjoint block element is ⊕ e_λ M e_λ with center span{e_λ}; tracial expectation covariance holds for every unitary of H. Checked.
6. Controls recomputed by hand: K2 module count 1+3+3+9 = 16 with trivial part span{I, F}; K5 Pauli Ad-splitting into ℂX, ℂY, ℂZ and G' = ℂI; K6 SO(3) decomposition 3 ⊕ 5, no abelian invariant subspace (diag(1,−1,0) and E_12+E_21 anticommute-type pair, not commuting); K7 1/2 ≠ 1; K9 E|u⟩⟨u| = I/2; K10 pure-pair reflection argument and mixed-pair δ_TV = 1/2. All agree with RESULT.

## Objections
- **R1 (non-blocking, interpretation).** Covariance is not forced by "source-independence"; a b-independent but fixed-basis law (K1) is source-independent. *Assessment:* RESULT labels covariance Q1 as a declared class hypothesis, and K1 is classified as inserted geometry, not excluded by P8. Acceptable.
- **R2 (non-blocking, scope).** Refinements that enlarge or change the carrier (B ⊄ A, adjoined ancillas, non-nested algebras) are outside 𝓛_G. *Assessment:* §1 restricts to B ⊆ A (pruning); §5 makes no claim beyond the class. Recorded here for the next run; no RESULT change required.
- **R3 (non-blocking, sharpness).** Is Theorem 1's hypothesis needlessly strong? *Assessment:* K5 shows Schur irreducibility is insufficient and K6 shows reducibility is not sufficient for growth; Proposition 1(ii) is the exact criterion. The hypothesis is appropriately placed.
- **R4 (non-blocking, novelty).** The content is the standard reference-frame/superselection lesson in a new local framing. *Assessment:* RESULT disclaims priority and cites Bartlett–Rudolph–Spekkens. Accept.
- **R5 (blocking? no).** Does Proposition 3 smuggle in a reference as a discovery? *Assessment:* ω is marked SUPPLIED in §4; K4 shows the inherited tracial reference is inert; K10 marks the ensemble mean as ensemble-supplied. No promotion.

No RESULT revision required.

## Claim boundary
O1 stands: **INNER_COVARIANT_REFINEMENT_CANNOT_GROW_CENTER; CENTER_GROWTH_REQUIRES_NONCENTRAL_SOURCE_INDEPENDENT_ORIENTATION; NATIVE_MILESTONE_NOT_ACHIEVED.** Path A active; C4–C6 open. No scientific module run.
