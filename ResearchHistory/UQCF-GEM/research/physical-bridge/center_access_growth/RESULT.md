# Center access growth under record-retaining pruning

Date: 2026-10-16 America/New_York. Parent: `d63aea606eb9e73bab812aef2934f799f3bb281a`. Preregistration: `PREREGISTRATION.md` (must be committed first).

**Conditional analytical assessment. Native milestone NOT ACHIEVED.** The findings in §§1–2 were already known before preregistration and are disclosed there; they are not preregistered predictions. The theorem is an elementary consequence of standard finite-dimensional conditional-expectation facts; no mathematical priority is claimed.

## 1. Setting
Finite-dimensional H. A GIVEN chain of unital *-subalgebras A_0 ⊇ A_1 ⊇ … ⊇ A_n with center retention Z(A_k) ⊆ A_{k+1}. Then Z(A_k) ⊆ Z(A_{k+1}) (`record_compatibility_bridge` §2) and the central atoms form a laminar tree: each atom of Z(A_k) is the sum of the atoms of Z(A_{k+1}) beneath it. E_k is the tracial conditional expectation onto A_k; for nested algebras E_m E_j = E_m (j ≤ m), so the nonselective output at stage m is E_m(ρ). The stage index orders pruning updates; it is not a duration.

Reader premise (P2, SUPPLIED): the stage-m accessible reader is R_m = Z(A_m), read out by its central-atom POVM {z_j^{(m)}}.

## 2. Theorem
Let ρ_0, ρ_1 be states, Δ = ρ_1 − ρ_0.

(a) Retention. For j ≤ m and every z ∈ Z(A_j): Tr[z E_m(ρ)] = Tr[zρ].

(b) Acquisition criterion. Suppose Tr(zΔ) = 0 for all z ∈ Z(A_k) (blind at stage k). Then the stage-(k+1) readout laws differ iff E_{Z(A_{k+1})}(Δ) ≠ 0, iff some atom z' of Z(A_{k+1}) has Tr(z'Δ) ≠ 0. Their total-variation distance is
  δ_TV = ½ Σ_{z' atom of Z(A_{k+1})} |Tr(z'Δ)|,
and by (a) this law, hence δ_TV, is unchanged at every later stage m ≥ k+1.

(c) Sector constraint. For every atom z of Z(A_k), Σ_{z' ≤ z} Tr(z'Δ) = Tr(zΔ) = 0. The acquired contrast is a redistribution within old sectors; it never changes an old sector's weight.

(d) Coherence blindness. If Δ = Σ_{i≠j} z'_i Δ z'_j (purely off-diagonal across new atoms), the contrast is zero.

Proof. (a) Z(A_j) ⊆ Z(A_m) ⊆ A_m, and Tr[aE_m(X)] = Tr[aX] for a ∈ A_m (inherited identity, `retained_reader_write` eq. 1). (b) Z(A_{k+1}) is spanned by its atoms, so Tr(·Δ) vanishes on it iff it vanishes on each atom; E_Z(Δ) = Σ Tr(z'Δ)/Tr(z') z' is zero iff every coefficient is zero. The readout laws are p_b(z') = Tr(z' E_{k+1}(ρ_b)) = Tr(z'ρ_b) by (a); δ_TV follows. (c) Laminarity gives z = Σ_{z'≤z} z'. (d) Tr(z'_l z'_i Δ z'_j) = 0 unless l=i=j. ∎

Interpretation boundary: the distinction already lies in ρ_b; (b) is a change of ACCESS, not creation of information. It needs no coupling U and no copy gate, and it does not contradict the fixed-reader result, since the reader R_k ⊊ R_{k+1} is not fixed. Relative to criterion (4) of `retained_reader_write`: there is no U; the contrast arises because the reader set grows, not because Q moves.

## 3. Premise provenance
| # | Premise | Status | Source |
|---|---|---|---|
| P0 | Finite-dimensional quantum carrier H | SUPPLIED | inherited conditional interface (v15.11/v15.15); no native ontology derived |
| P1a | Existence and choice of the chain A_0 ⊇ … ⊇ A_n, in particular each center-growth step | SUPPLIED | RAS; not selected by any inherited law |
| P1b | Center retention Z(A_k) ⊆ A_{k+1} | SUPPLIED (inherited condition) | v15.11 sufficient record-preservation condition |
| P1c | Nested centers and laminar atom tree | DERIVED | `record_compatibility_bridge` §2, from P1b |
| P2 | Accessible reader = Z(A_m), central-atom POVM | SUPPLIED | standard superselection reading; no receiver, factorization or reference association constructed |
| P3 | Source pair ρ_0, ρ_1 and its binding to native events | SUPPLIED | no native source identification |
| P4 | Blindness at stage k | Hypothesis; automatic if Z(A_k) = ℂI (trivial-center seed, itself SUPPLIED per `compatible_history_seed` §1) |
| P5 | Nonselective operation E_m | SUPPLIED (inherited) | RAS reduction |
| P6 | Retention of the acquired law | DERIVED | Theorem (a) from P1b, P5 and the inherited identity |
| P7 | Acquisition iff criterion, δ_TV, sector constraint | DERIVED | Theorem (b)–(d) |
| P8 | Chain independent of the source | Required hypothesis | violating it gives C3 |

## 4. Controls (exact hand calculations; nothing executed)
C1 Non-growing center (rejecting). H = ℂ²⊗ℂ², A_0 = M_4, A_1 = M_2⊗I. Both centers are ℂI. With ρ_0 = |00⟩⟨00| and ρ_1 = |10⟩⟨10|, the sources differ on A_0 and on A_1 (via Z⊗I), but the central readers stay blind: δ_TV = 0. Distinguishability within the retained algebra is not accessibility under P2.

C2 Center erasure (rejecting). A_0 = M_2⊕M_2 with atoms p = diag(1,1,0,0) and s = diag(0,0,1,1); A_1 = B = {diag(x,y,x,y)}, so B ⊆ A_0 but p ∉ B. For ρ = p/2, E_B(ρ) = I/4, so Tr[pE_B(ρ)] = 1/2 ≠ Tr[pρ] = 1. Retention (a) fails, and the new atom q = diag(1,0,1,0) is not laminar with p, s. Premise P1b is essential.

C3 Source-chosen chain (rejecting). ρ_0 = ρ_1 = |0⟩⟨0| (Δ = 0). Reduce source 0 to the computational diagonal and source 1 to the Hadamard-basis diagonal. A "first-atom" readout gives 1 versus 1/2: an apparent contrast of 1/2 with identical sources. That contrast comes from the chain choice, so the criterion is not applicable. Choosing the chain by source is a selective/labelled instrument (`retained_reader_write` §2) and is excluded by P8.

C4 Swap outside reader (separating; reconciled with `collective_covariance_candidate` §4). A_0 = M_4, A_1 = {X : XF = FX}. Z(A_1) = span{P_sym, P_anti} with P_anti = (I−F)/2, so the center grows from ℂI. For |00⟩ versus |10⟩: Tr(P_anti ρ) = 0 versus 1/2, giving δ_TV = 1/2. This is admissible under (b), with a joint, central reader. The local Q_M (0 → 1/2) is in neither A_1 nor Z(A_1) and is rejected as a reader. This reconciles the earlier swap control with the theorem without crediting a local marginal. Consistency with `collective_covariance_candidate` §4: that stage observes that P_- already has probabilities 0 and 1/2 at input, so it is not an initially blank acquired record. Both statements hold. The 1/2 contrast is present in ρ_b throughout; it becomes *accessible under P2* only because the central reader grows from ℂI to span{P_+,P_-}. C4 is therefore an access change, never an acquisition by a blank memory, and it inherits P1a and P2 as supplied premises.

C5 Trivial-seed positive case. A_0 = M_2 (Z = ℂI, so every pair is blind), A_1 = diagonal algebra (atoms |0⟩⟨0|, |1⟩⟨1|).
- (i) |0⟩⟨0| versus |1⟩⟨1|: δ_TV = 1, and the sector sum −1 + 1 = 0 = Tr(IΔ) ✓.
- (ii) Partial: |0⟩⟨0| versus |+⟩⟨+|: contrasts −1/2, +1/2, δ_TV = 1/2.
- (iii) Coherence-blind: |+⟩⟨+| versus |−⟩⟨−|: Δ is off-diagonal, so δ_TV = 0 by (d).
The step M_2 → diagonal is itself supplied (P1a).

## 5. Relation to `collective_covariance_candidate` (overlap and novelty)
- Different mechanism. That stage moves a fixed local reader Q by a supplied symmetric unitary, via criterion (4) of `retained_reader_write`. This note holds the dynamics nonselective and moves the reader set. Neither result implies the other. The partial-swap theorem says nothing about which readers are accessible, and the center-growth theorem contains no unitary.
- Shared object. Both examine P_- on the |00>/|10> pair with the same 0 versus 1/2 numbers (C4 here, §4 there). Their verdicts agree once access change is distinguished from blank-memory acquisition.
- Not subsumed in either direction. The new stage's invariant-reader statement is a special case of theorem (a): span{I,F} = Z(swap commutant) is retained. The general iff criterion (b), the sector constraint (c), coherence blindness (d) and controls C1–C3 and C5 do not appear there.
- Shared gap. Both reduce to supplied structure: there, the common representation, nonidentity occurrence and local access; here, the center-growth step and the central reader. Neither achieves the milestone.
- Novelty is modest: an elementary standard fact applied to the changed-reader branch that `retained_reader_write` §2 left explicitly eligible and no published stage has treated.

## 6. Objection 1: is the growth step native?
The acquisition happens exactly at a center-growth step Z(A_k) ⊊ Z(A_{k+1}), and the theorem's whole content sits there. The inspected inherited sources do not derive that step:
- v15.11 supplies the chain and the retention condition as inputs.
- `record_compatibility_bridge` builds its tree from a GIVEN chain.
- `compatible_history_seed` treats the trivial center as a possible supplied case.
- The V906/V930 ancestry supplies mode-selected updates. `collective_covariance_candidate` supplies its symmetry and occurrence premises and does not select an algebra chain.
No inspected result selects A_{k+1} from A_k, the state or an event. The reader premise P2 is likewise interpretive. Therefore the theorem converts the open question "native coupling U?" into the sharper open question "native law for center growth plus justified central access?" It does not answer it. A source-independent law fixing A_{k+1} would make P1a derived without violating P8. Such a law is not supplied here and must not be invented under the no-new-primitive mandate.

## 7. Disposition
**CONDITIONAL_CENTER_ACCESS_GROWTH_PROVED; GROWTH_STEP_AND_CENTRAL_READER_SUPPLIED; NATIVE_MILESTONE_NOT_ACHIEVED** (frozen outcome O2).

The work is analytical only: no numerics, simulation, enumeration, module import or replay was performed, and no inherited stack was run. No CLOSED/CERTIFIED status, physical law, force, energy, geometry, dark-matter primitive or fundamental clock is claimed. Time remains pruning / ordered recoverability update. Path A remains active, Path B closed, broad C3/C4–C6 OPEN.

Missing AGENTS requirements (reported explicitly): no workflow SHA; no pinned full-stack GitHub run; no execution artifacts or reproduced bytes (none applicable to a pure-analysis note, but this means it is not stage closure); no independent review; no publication audit; no PR/merge audit.

## 8. Source list (to be bound in `source_packet.json` / `source_identities.json` at parent `d63aea6`)
1. `ResearchHistory/UQCF-GEM/AGENTS.md`
2. `physical-bridge/NATIVE_EVENT_MILESTONE.md`
3. `physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` (80,735-byte parent)
4. `physical-bridge/record_compatibility_bridge/RESULT.md`
5. `physical-bridge/compatible_history_seed/RESULT.md`
6. `physical-bridge/retained_reader_write/RESULT.md`
7. `physical-bridge/collective_covariance_candidate/RESULT.md`
8. `physical-bridge/collective_covariance_candidate/ANALYTICAL_REVIEW_RAW.md`
9. `physical-bridge/collective_covariance_candidate/PUBLICATION_RECEIPT.md`
The inspection is bounded to these sources; no archive-wide novelty or absence claim is made.
