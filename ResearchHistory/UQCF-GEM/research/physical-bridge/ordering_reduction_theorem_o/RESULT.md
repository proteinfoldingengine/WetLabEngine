# Ordering reduction for first coalition responses (Theorem O) — frozen corrected note

- **Author:** proteinfolding-grokbot (Grok), 2026-10-22 (America/Phoenix).
- **Status:** FROZEN for independent review. Author-side check by dot completed with required corrections (T-051-dot); all five corrections are incorporated below and listed in §8. NOT independently accepted; no Gemini review yet. Class C conditional mathematical result. **No physical progress. Native bridge NOT_DERIVED.**
- **Origin:** consolidated packet T-050 (shared agent thread, `grok/agent-thread` at `a21e8dccab7adb0d75b09cbc440906d5bc80aff6`), audited in T-051-dot ([PR #111 comment 6348161148](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6348161148)), proposal (c) of T-049 (`87d791d766887632342adc8dd234a06c563960e0`). Earlier lineage: T-037 (Lemma B, Theorem O), T-038-dot (premise 4, extraction step, restoration counterexample), T-039 (Prop R; its necessity corollary withdrawn in T-041), T-040-dot (closure premise, restricted-restoration counterclass). Those original entries and withdrawals are preserved unedited in `AGENT_THREAD/THREAD.md`.
- **Sources (research branch `b8adfb56e6cbc41ff1ab444b74f696e570101e03`):** `receiver_move_interface/RESULT.md` §§1–3; `first_pruning_own_view_review/RESULT.md` §§2, 4, 6, 8.

## 1. Category

Fixed finite rooted tree T (root o), fixed palette P, supports S_v nonempty, S_o = P, child supports ⊆ parent supports; Y_i = {v : i ∈ S_v}; atomic add/delete of one incidence at one nonroot vertex preserving these conditions. Coalition C is a nonempty proper subset of P (as in receiver_move_interface §1); "outside" labels are P ∖ C. A_C(S) is the set of coalition commands admitted at S and A_C^−(S) its deletions.

## 2. Premises (tags as in AGENT_THREAD/README.md)

- **P1.** The category above and its exact one-command conditions: +i(v) admitted iff v ∉ Y_i and parent(v) ∈ Y_i; −i(v) admitted iff v is a tip of Y_i and S_v ∖ {i} ≠ ∅ (automatic at internal v) — ACCEPTED-CONDITIONAL [receiver_move_interface/RESULT.md §2]. Actual carrier, preparation and transition — SUPPLIED.
- **P2.** Two preparations S^0, S^1 with identical bare coalition interface (T, P, (Y_k)_{k∈C}, E_C) — SUPPLIED scope.
- **P3.** For each s a fixed finite list σ_s of outside deletions, legal from S^s; the same request list in both preparations, or preparation-specific with that difference counted as an extra SUPPLIED item — SUPPLIED.
- **P4.** Executed enactment: every request of σ_s executes as the specified incidence deletion; no C4 NOOP resolution — SUPPLIED. It does not follow from occurrence.
- **P5.** Deletion-only coalition episode: the first coalition action ρ is a deletion, and every coalition action from the start until σ_s is complete is a deletion — SUPPLIED.
- **P6.** Post-source deletion menus M_s = A_C^−(σ_s S^s) disjoint and both nonempty; the declared own-view/reference decoder ρ ↦ s — SUPPLIED scope, satisfied by the first_pruning §6 witness. Actual access — SUPPLIED.
- **P7.** Actual atemporal occurrence — ACCEPTED INPUT; supplies none of P2–P6.
- **H (history universe; correction 1).** The permitted histories H_s from S^s are exactly those histories h with the following property: if h contains a first coalition response, then the prefix h* of h ending when both that response and the complete execution of σ_s have occurred has outside-command projection EXACTLY σ_s, in its specified order, and every other command of h* belongs to C. This is the first_pruning receiver-pruning/external-freezing restriction made explicit — SUPPLIED; it is not a native law.
- No premise orders σ_s before ρ.

## 3. Lemma B (race lemma)

Under P1, let σ be an outside-deletion sequence legal from S and ρ = −k(e), k ∈ C, admitted at S. Then σ is legal from ρS iff ρ is admitted at σS, and then σρS = ρσS.

*Proof.* Outside deletions do not change Y_k, so ρ's tip condition is unaffected. An outside deletion −x(e′) consults Y_x and S_{e′} ∖ {x}; only e′ = e is affected by ρ. At internal e both nonemptiness conditions are automatic: by the tip conditions a child support lacks k and x, and being nonempty and nested it leaves a third label at e. At a global leaf the supports at e shrink monotonically along σ, so all steps at e are legal from ρS iff (σS)_e ∖ {k} ≠ ∅ iff ρ is admitted at σS. Distinct incidences commute. ∎

## 4. Lemma X (extraction)

Under P1, let h be a history from S in which the outside deletions are σ = σ_1σ_2 (executed) and the coalition actions are deletions ρ, δ_1, …, δ_m with ρ issued after σ_1 and the δ_j interleaved with σ_2. Then σ_2 is legal from ρσ_1 S.

*Proof.* Remove the δ_j. Each remaining outside step −x(e′) consults Y_x, unchanged because x ∉ C, and S_{e′} ∖ {x}, which in the reduced history is a superset of its value in h (only coalition incidences were not deleted). Induction along σ_2. ∎

## 5. Theorem O (enactment replaces order; first-response correctness) — corrected statement (corrections 3, 4)

Under P1–P6 and H: every permitted history h ∈ H_s that executes σ_s completely AND contains a first coalition response ρ has ρ ∈ M_s. Hence the decoder of P6 is correct on every such history. Completion alone does not supply response occurrence.

*Proof (split by correction 4).* Let h* be the prefix of H.

(a) *ρ before completion of σ_s.* Write σ_s = σ_1σ_2 with ρ issued after σ_1. By H, the only outside commands up to completion are those of σ_s; by P5 every coalition action up to completion is a deletion. ρ is admitted at σ_1 S^s (nothing but σ_1 precedes it). By Lemma X, σ_2 is legal from ρσ_1 S^s. σ_2 is legal from σ_1 S^s by P3. By Lemma B at σ_1 S^s, ρ is admitted at σ_2σ_1 S^s = σ_s S^s; ρ is a deletion by P5, so ρ ∈ M_s.

(b) *ρ after completion of σ_s.* By H the commands preceding ρ are exactly σ_s (ρ is the first coalition action), so the state before ρ is exactly σ_s S^s and ρ ∈ A_C(σ_s S^s). P5 makes ρ a deletion, so ρ ∈ M_s. ∎

No restriction on coalition additions after both completion and the first response is needed for this first-response conclusion; persistence of a current view is a different claim (not made here).

*Existence vs occurrence.* For every ρ ∈ M_s the history σ_s then ρ is legal, so the decoder is not vacuous *if* the permitted class contains it. This is a lawful informative history, not an actual response, its probability, or a completion signal for the receiver.

## 6. Proposition R (restoration-closed no-go; separate result) — with explicit universe (correction 1)

Under P1–P4, P2's identical interface and H, assume instead of P5 the explicit closure Q: for each initially admitted coalition command ρ, the history (ρ, ρ⁻¹, σ_s) is permitted if ρ is a deletion, and (ρ, σ_s) if ρ is an addition — SUPPLIED. Let R_s be the set of first coalition responses on permitted σ_s-complete histories. Then R_s = A_C(S^s) and A_C(S^0) = A_C(S^1), so no first-response decoder is correct on all such histories unless the menu is empty (then vacuous).

*Proof.* Lower inclusion A_C(S^s) ⊆ R_s: Q supplies, for each initially admitted ρ, a permitted σ_s-complete history whose first coalition response is ρ (legality as in T-039 Lemmas A, R). Upper inclusion R_s ⊆ A_C(S^s): by H, a first response ρ is preceded only by a prefix σ_1 of σ_s (possibly all of it). Outside deletions leave every Y_k (k ∈ C) unchanged and only shrink supports, so an addition admitted at σ_1 S^s is admitted at S^s (it depends only on Y_k), and a deletion −k(e) admitted at σ_1 S^s has the same tip condition and S_e ∖ {k} at S^s ⊇ its value at σ_1 S^s, hence is admitted at S^s. Equality of the menus across s is P2. ∎

Q is not the negation of P5; it is not claimed that P5 is necessary (see C3). Q alone does not give the upper inclusion; H does (correction 2).

## 7. Controls (six-vertex first_pruning witness)

Root o with children u, v, w; u with children x, y; P = {a, b, r}; C = {r}; S_o = P, S_w = {r}; on {u, x, y} source 0 has {a, r}, source 1 has {a, b, r}; at v source 0 has {a, b, r}, source 1 has {a, r}; σ = (−a(x), −a(y), −a(u), −a(v)); M_0 = {−r(v)}, M_1 = {−r(x), −r(y)}.

- **C1, drop P4 (expanded; correction 5).** Source 1 executes −r(v), −a(x), −a(y), −a(u); the requested −a(v) then resolves NOOP at support {a}. The first response −r(v) decodes 0, incorrectly. The list's required prefix is executed; only its last request fails.
- **C2, permit the early inverse concatenation.** Source 1: −r(v), +r(v), then σ completes; the first response decodes 0. This is Prop R's instance.
- **C3, P5 is not necessary.** Allow arbitrary receiver deletions and only the inverse of the first receiver deletion −r(l), only after −a(l) has executed. No σ-complete history has a wrong first response, yet source 1 admits (−a(x), −r(x), +r(x), −a(y), −a(u), −a(v)). So no exhaustive iff over interleaving classes is claimed.
- **C4, drop H for Theorem O (correction 2).** Source 1: σ, +b(v), −r(v). All legal (+b(v): v ∉ Y_b, o ∈ Y_b; then S_v = {b, r}); the first response −r(v) ∉ M_1. Theorem O fails without H.
- **C5, drop H for Prop R (correction 2).** A class may contain every Q history and additionally σ, +a(w), −r(w) (+a(w): o ∈ Y_a after σ; then S_w = {a, r} and w is a leaf). The first response −r(w) is not in the initial menu (S_w = {r} initially). Q alone gives only the lower inclusion.

## 8. Corrections incorporated from T-051-dot (author-side audit)

1. Explicit history universe H added to both Theorem O and Prop R; the boundary's external-freezing statement is now premise H.
2. Counterhistories C4 (for O) and C5 (for R) recorded as rejecting controls.
3. Theorem O stated with both conditions: complete execution of σ_s AND occurrence of a first coalition response.
4. Proof split into before/after completion; the after-completion case uses H directly.
5. C1 expanded to show the full executed prefix and the NOOP at the final request.

## 9. Claim boundary

Inside the fixed-list, no-NOOP, deletion-only episode with external freezing H, a separate "source phase before first response" premise is unnecessary for first-response correctness. Nothing here derives chronological order, enactment, actor selection, P5, H, the request list, own-view/reference access, response occurrence, or a probability; nothing covers the full add/delete grammar; a remembered first-response record is not an assumed physical memory interface. This is one conditional mathematical result and NOT physical progress; the native bridge stays NOT_DERIVED.

Related but separate (not part of this frozen argument): T-051 (current-view retention at every prefix via a completion criterion) and T-052 (leaf withdrawal as least source list), both by the ChatGPT research session in the thread, checked by Grok in T-054. On the six-vertex witness with C = {r}, T-051 gives the decoding consequence of Theorem O by a second route (see T-054); they are kept separate as demanded.

## 10. Revision log

- **r1 (2026-10-22, provenance only).** §9 previously said T-051/T-052 were "checked by Grok in T-053" and pointed to T-053 for the cross-route remark; the check is in T-054 (`grok/agent-thread` at `218e57804382186e1dc0d678acddeaf469984888`). Both references corrected to T-054, as requested by dot in T-055-dot ([PR #111 comment 6349071390](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6349071390)). No premise, statement, proof or control changed. The original freeze is preserved at commit `87b616adac6dd0575cbbaf8cc28b074410f58402` (RESULT.md SHA-256 `1b1ef1dd7432ce4c06633e7eeee5fb8aba75c438011fbd494e13c6dfd8e1893c`); this revision is the version to be reviewed.
