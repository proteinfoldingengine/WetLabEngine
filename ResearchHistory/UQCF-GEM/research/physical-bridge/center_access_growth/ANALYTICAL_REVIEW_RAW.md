# Argument review: center access growth

**Disposition: ACCEPT_FOR_BOUNDED_ANALYTICAL_PUBLICATION after revision commit `2b49c6535f0d5941e74a9fd32514a39901f8081a`; three non-blocking objections raised and resolved; milestone NOT ACHIEVED.**

Review date: 2026-10-16 America/New_York. **Independence limitation (disclosed):** this review was produced by the same agent session that drafted the note, as a separate adversarial re-derivation pass. It is not authored by an independent party. A later independent reviewer may supersede it. This limitation is not represented as satisfying AGENTS' algorithmic-independence requirement.

## Bound objects (post-revision)
- RESULT.md SHA-256 `329ee9436730c8057496ff162205205a75bf45237ffe7e276a5072fc65669e66`
- INDEX_APPEND.md `4bdcb94f036a134149fe086639b407d6dc00ecdfffbc9cd87547fdc7f512834e`
- PREREGISTRATION.md `fdd3dc9aeff07bf1111bbcb3e99eb3ec0a549b669f4bc207a5f1728c24b19ec0`
- source_packet.json `a1a30eb2cf5b823c7e0332335b9f01180e21cf17566398c81c808f70bdd7f065`
- source_identities.json `d09aff9ff0c3ab74f396a219c8fa858d1ebffbfa89a18a1571377be5b83ad85a`
Parent `d63aea606eb9e73bab812aef2934f799f3bb281a`. Commits reviewed: preregistration `5944d8fc69080b3bcf701873d3b450b1986d0c3c`, note `aa0b68e3302bdeb44e665ce1cc92165f2ab16f6c`, revision `2b49c6535f0d5941e74a9fd32514a39901f8081a`.

## Re-derivations
(a) For nested A_j ⊇ A_m, the tower property gives E_m E_j = E_m. Z(A_j) ⊆ Z(A_{j+1}) ⊆ … ⊆ Z(A_m) ⊆ A_m, using retention at each step and the fact that a retained central element commutes with the smaller algebra. The bimodule property and trace preservation give Tr[zE_m(X)] = Tr[E_m(zX)] = Tr[zX]. Valid.

(b) Z(A_{k+1}) is a finite-dimensional commutative C*-algebra spanned by orthogonal atoms summing to I. A linear functional vanishes on it iff it vanishes on the atoms. The tracial expectation onto it is Σ Tr(z'·)/Tr(z') z', which is zero on Δ iff every Tr(z'Δ) = 0. By (a) the atom POVM law on E_{k+1}(ρ_b) equals Tr(z'ρ_b), so δ_TV = ½Σ|Tr z'Δ|. Applying (a) with j = k+1 gives persistence. Valid, given a chain common to both sources (see R1).

(c) Nested commutative algebras: each old atom z lies in Z(A_{k+1}), so z = Σ of the new atoms below it. Summing gives Tr(zΔ) = 0 by blindness. Valid.

(d) Tr(z'_l z'_i Δ z'_j) = Tr(z'_j z'_l z'_i Δ) = 0 unless i = j = l. Valid.

## Controls re-derived
- C1: Z(M_2⊗I) = ℂI since M_2 has trivial center. Retention holds trivially. σ_z⊗I has expectations +1 and −1 on |00⟩ and |10⟩, so the sources differ inside A_1 while the central reader stays blind. Correct.
- C2: B = {diag(x,y,x,y)} ⊆ M_2⊕M_2. E_B(diag(½,½,0,0)): atom q gets coefficient (½)/2 = ¼, and likewise q'. The result is I/4, with Tr(pI/4) = ½ ≠ 1. p ∉ B. Correct.
- C3: E_comp(|0⟩⟨0|) = |0⟩⟨0|, giving first-atom probability 1. E_Had(|0⟩⟨0|) = I/2, giving ⟨+|·|+⟩ = ½. Δ = 0, so the "contrast" is from the chain choice. Correctly excluded.
- C4: the commutant of {I,F} is M_3⊕M_1 on Sym⊕Anti, with center span{P_+,P_-}. ⟨10|P_-|10⟩ = ½ and ⟨00|P_-|00⟩ = 0. Z(M_4) = ℂI ⊆ A_1. Q_M is not swap-invariant. Correct. The reconciliation with the collective stage (access change, not blank acquisition) is accurate.
- C5: (i) δ = 1, sector sum 0. (ii) contrasts −½, +½, δ = ½. (iii) |+⟩⟨+| − |−⟩⟨−| = σ_x, off-diagonal, δ = 0. Correct.

## Objections
- **R1 (theorem hypothesis).** (b) did not state that the chain is common to both sources; only table row P8 did. Without it, C3 would be a counterexample to (b) as written. *Resolved in `2b49c65`:* (b) now opens "Let the same chain (independent of b, premise P8) act on both sources."
- **R2 (notation).** C1 wrote "Z⊗I", colliding with the center notation Z(·). *Resolved:* replaced with "the Pauli effect σ_z⊗I ∈ A_1".
- **R3 (scope).** §5 said the branch had been treated by "no published stage", an archive-wide absence claim beyond the 9-source packet. *Resolved:* the claim is restricted to the nine inspected sources, with an explicit no-archive-wide-novelty statement.
- **R4 (process, non-blocking, not textually resolvable).** The preregistration was committed after the full draft existed. It is disclosed in item 5 and is not claimed as prospective. It remains a recorded deviation from AGENTS' preregistration-before-execution ordering for any purpose beyond this analytical note.

## Claim boundary
The provenance table is accurate: P1a, P2, P3 and P5 are supplied; P1c, P6 and P7 are derived. The disposition O2 follows. There is no physical-law, numerics, CLOSED or CERTIFIED claim. Time is treated as stage order only. No scientific module was run.
