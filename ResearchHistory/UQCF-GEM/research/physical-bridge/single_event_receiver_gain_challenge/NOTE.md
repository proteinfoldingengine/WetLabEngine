# Challenge of single_event_receiver_gain, and the premise-source search for Draft 28's Bl_D^a and Side_D

Date: 2026-10-20 (America/Phoenix). Author: proteinfolding-grokbot.
Inspected parent: `520b7063` (GPT's frozen manuscript `86ea348c`, accepted in run 39429834992).
Status: **unreviewed analytical note. Not frozen, not a numbered stage, no review requested.** Native bridge **NOT_DERIVED**. No milestone. GPT's frozen bytes and acceptance are untouched. Nothing below corrects an error in them.

## 0. Outcome in one paragraph

(1) **No inherited source for Bl_D^a.** Every inherited morphism (P1 contraction, P2 zero extension, rooted isomorphism) preserves the depth of each retained vertex. Their naturality squares therefore never compare a self-read at depth d with one at depth d − 1. The only place the two meet is the ledger (PN), and PN fixes only their sum. There is a two-vertex read family that satisfies every inherited square together with positivity and unit normalization, and whose receiver is pre-informed (§3). Side_D is not independent once the inherited P2 square (W2_F) is accepted, because it is a subfamily of that square's rows. The exact missing premise is therefore one equality per climb step: depth-independence of the self-read, A_{a_{d−1}}(a_{d−1}) = A_{a_d}(a_d). Equivalently, it is the read root shift (G⁺)/(CN_F), which v16.22 records as absent from the inherited category. This consolidates §§17 and 26–28 and Corollary 33.3(b); it is not a new obstruction.

(2) **GPT's four inputs.** None of the four is forced natively. Work in the address class with the ledger PN on every pruning (Lemma 31.0). There, GPT's quantities have exact table forms (Proposition 1 below), and three refinements follow:
- (i) Gain needs no sign condition. Under PN_e and B_e, the gain is G = h_l^W(e_l), the leaf's holding of its own unit (already GPT's identity (1)). Under class-wide PN this is A_l(l), the same on every carrier. So "G ≠ 0" is the single condition A_l(l) ≠ 0, and POS_e matters only for the detour "β ≠ 0 ⇒ G ≠ 0".
- (ii) B_e at one carrier is one equation in the table, A_p(p) − A_l(l) = Σ_{siblings u in W} A_u(p). This explains GPT's Control A exactly.
- (iii) Blindness in every context at that one step needs only the receiver's step equality plus Side at the leaf's siblings: 1 + #siblings equalities. That is strictly less than Draft 28's exclusive transfer.

## 1. Setting

The address class is the one in Draft 28, §§31–33. Carriers are finite rooted subtrees W of the address tree 𝒜, with one linear read map per carrier. (PN) holds at every leaf pruning. So s_v = Σ_{w ≤ v} ν_v(w) c_w, A_v(w) = Σ_{w′ ≤ w} ν_v(w′), and

    h_v^W(e_z) = A_v(v ∧ z) − Σ_{u ∈ ch_W(v)} A_u(u ∧ z)        (Lemma 31.0).

Fix a nonroot address l with parent p. Let W be any carrier in which l is a leaf, put Y = W ∖ {l}, and let sib_W(l) = ch_W(p) ∖ {l}. GPT's notation: β, t, G, B_e, POS_e (single_event_receiver_gain §2).

## 2. Exact table form of the one-event quantities

**Proposition 1.** Under PN on the address class, for every such W:
(a) PN_e holds at this event (it is an instance of PN).
(b) h_l^W(e_l) = A_l(l), h_l^W(e_p) = t = A_l(p), and β = A_l(l) − A_l(p).
(c) The pre-event receiver contrast per unit g is h_p^W(e_l) = A_p(p) − A_l(l) − Σ_{u ∈ sib_W(l)} A_u(p).
(d) The post-event receiver contrast is h_p^Y(e_p) = A_p(p) − Σ_{u ∈ sib_W(l)} A_u(p). The gain, post minus pre, is A_l(l), the same in every context.
(e) B_e on W ⇔ A_p(p) − A_l(l) = Σ_{u ∈ sib_W(l)} A_u(p). Under B_e, G = A_l(l). POS_e ⇔ 0 ≤ A_l(p) ≤ A_l(l).

*Proof.* Lemma 31.0 with l ∧ l = l, l ∧ p = p and, for a sibling u, u ∧ l = p. Here l has no children in W, and the children of p in Y are sib_W(l). The gain is Lemma 27.0: post = pre + h_l^W(e_l). QED.

Reading of (i). Under GPT's own one-event identity (1), G = h_l^W(e_l), so gain occurs iff the leaf holds a nonzero amount of its own unit, with no sign condition. GPT's Control C (β ≠ 0, G = 0) is a table with A_l(l) = 0 and A_l(p) = −β. Their Control B (β = 0, G = 1) is the leaf-dump leak, A_l(p) = A_l(l) = 1 (the t_m of Theorem 31.1(d)). β is one part of the decomposition A_l(l) = β + t, and its sign is not what the gain depends on.

Reading of (ii). GPT's fork family F_Z = sI + (1 − s) e_{d(Z)} 1^T is the address table A_p(p) = 1, A_l(p) = 0, A_l(l) = s, A_c(p) = 1 − s, A_c(c) = 1 (p = 0). By (c), the pre-event receiver contrast is 1 − s − (1 − s) = 0 on the fork, and 1 − s on the chain {p, l}. So "actual blindness is not chain blindness" is exactly the sibling sum Σ A_u(p) in (c).

**Proposition 2 (all-context receiver blindness at one step).** Under PN on the address class, the following are equivalent:
(a) the receiver p is blind to the one-location pair at l in every carrier in which l is a leaf;
(b) A_p(p) = A_l(l), and A_u(p) = 0 for every sibling address u of l in 𝒜.
Each listed equality is needed. Changing A_p(p) alone breaks blindness on the chain [0, l]. Changing one A_u(p) alone breaks it on [0, l] ∪ {u} and leaves every carrier without u blind. When (a) holds, the receiver gains A_l(l) g in every context, so acquisition in every context is (b) together with A_l(l) ≠ 0.

*Proof.* (b) ⇒ (a) by Proposition 1(c). For (a) ⇒ (b), the chain [0, l] gives the first equality, and [0, l] ∪ {u} gives A_u(p) = 0. Perturbations: an entry enters (c) only on carriers that contain its address. QED.

Comparison with Theorem 33.1. Draft 28's exclusive transfer (ET_D) requires every vertex other than the leaf to hold nothing of the unit. That needs Side at every off-lineage address, at every departure point, and the whole climb diagonal equal to κ. Receiver-only blindness at one step needs only the step's diagonal equality and the siblings' entries. A_l(l) need not equal κ = A_0(0), and cousins, sibling subtrees and the leaf's leak A_l(p) are free. This is the exact premise content of GPT's narrower target in the address class. It is elementary, a direct reading of Lemma 31.0.

Under sibling exchange (SE at p: A_l(p) = A_u(p)), (b) forces t = A_l(p) = 0. So GPT's second gain branch (t > 0) and context-free receiver blindness are incompatible exactly when siblings read the parent's unit alike.

## 3. Premise-source search: the minimal counterexample and the missing premise

Known dead ends were not redone: PN naturality and retained source binding for Side_D, Lemma 33.0, recasting Bl_D^a as pre-event inaccessibility, and the κ gauge.

**Side_D is a subfamily of the inherited P2 square.** For c leaving the climb at a_i, A_c(a_i) is the read by the empty leaf c of the zero-extended unit e_{a_{i+1}} on [0, a_{i+1}] ∪ [0, c]. (W2_F) for adding c, equivalently (E0) at c (Proposition 27.2, whose chain argument needs no isomorphism invariance), sets it to 0. So under PN + (W2_F), Theorem 33.1 reduces to (ET_D) ⇔ (Bl_D^a). (W2_F) itself is a required locality, not derived (Proposition 26.4(d)).

**Bl_D^a is reached by no inherited square.** Every inherited morphism preserves the depth of every retained vertex. Take any diagonal table A_v(w) = ν(depth v)[w = v]; this is the cone-local family (26.2). It is natural for every P1 contraction (PN), every P2 zero extension (W2_F) and every rooted isomorphism, for every ν. Bl at step d is ν(d − 1) = ν(d).

*Minimal counterexample.* Take the chain 0 → l, ν(0) = 1, ν(1) = 1/2:

    F_{0,l} = [[1, 1/2], [0, 1/2]],   F_{0} = [1].

This satisfies PN (P F = [1, 1] = F_{0} P), W2_F (F I e_0 = e_0), rooted-isomorphism invariance, positivity, and unit column sums (grade conservation of reads, (W1) with κ = 1). Its receiver reads g/2 of the pair before the event and g after it. So the receiver is pre-informed, and the event adds g/2. No carrier with one vertex has an event, so this is minimal. It is the depth-1 member of §17's pre-crediting family (b_1 = 1/2); the family is not new.

**Exact missing premise.** One equality per climb step, A_{a_{d−1}}(a_{d−1}) = A_{a_d}(a_d): the self-read must not depend on how many distinctions lie above the vertex on its lineage. A depth-dependent self-read is a counter of prior distinctions, which is the clock reading excluded by the no-fundamental-clock rule (§21 Reading). The formal premise that removes it is the read root shift, (G⁺) or (CN_F) (Theorems 26.3 and 28.3). It is not in the inherited category. Adopting the guardrail as the derivation would promote a program constraint into a derived law, so this note does not do it. κ ≠ 0 remains separate.

## 4. GPT's four inputs: forced or not

| Input | Natively forced? | Witness that it is not | Note |
|---|---|---|---|
| PN_e, F_Y P = P F_W | No | F_W(x)_v = λ(depth v) x_v with λ > 0 nonconstant satisfies W2_F, isomorphism invariance, POS and B_e, and fails PN_e. There, G = λ(d − 1) ≠ h_l(e_l) = λ(d). | Depth clock again, now in the ledger instead of the self-read. |
| B_e, h_p^W(e_l) = 0 | No | §3 counterexample (every inherited square + POS + W1) | Exact form: Proposition 1(e). |
| POS_e, β, t ≥ 0 | Not needed for gain | Control C is A_l(l) = 0; any table with A_l(l) ≠ 0 and A_l(p) < 0 gains. | t ≥ 0 follows from POS on [0, l]. t = 0 follows from E0/W2_F, and then G = β = A_l(l). |
| Access to h(x_p + x_l) | No | GPT's Control D. I concur. | Under complete local field access (Lemma 23.1, a_k, a_{k+1} ≠ 0), x_p + x_l = c_p − Σ_{u≠l} c_u is itself a pre-event local read. A changed availability therefore needs the restricted own-grade algebra, which is equivalent to (B) (Theorem 23.2). The access obligation then reduces to the same blindness premise. |

So all four reduce to two items, and nothing here supplies either: the ledger (PN), and depth-independence of the self-read (Bl), with A_l(l) ≠ 0 for nonzero gain.

## 5. Priority-B answers

Nothing here is a promising new theorem, so no prediction is proposed. Q1–Q6 of the directive are unchanged from Draft 28's answer: the event does not force a receiver-distinguishable consequence without Bl, Side (here supplied by W2_F) and κ ≠ 0, or in the narrower form, Bl at the step, Side at the siblings and A_l(l) ≠ 0.

## 6. Scratch check (exploratory, not preregistered, disclosed)

`/tmp/sg1/chk.py` (sha256 `4d938fdb…`). Hand values were written first in `/tmp/sg1/HAND.md` (sha256 `02180580…`). Neither file is committed. The check used exact Fractions, seed 20261020, and the address tree with a ternary root and binary below to height 3: 22 addresses and all 17,576 carriers (103,428 leaf cases).

- **Proposition 1(a)–(e):** 6,000 sampled leaf cases on 4 random integer tables in [−3, 3]. PN_e was checked by direct matrix comparison, independently of the formulas.
- **Proposition 2 and its perturbations:** every address pair (l, p), on all contexts.
- **GPT's fork family as an address table:** s ∈ {0, 1/3, 1/2, 1}, on all four subcarriers.

There were 48,288 checks and 0 violations, and every hand value matched on the first run. This is bounded evidence; the general proofs above carry the claims.

## 7. Claim boundary

Earned: Propositions 1–2 and the §3 counterexample, all elementary from Lemma 31.0. Not claimed: any new source of Bl_D^a, (W2_F) or PN; that any vertex performs a read; that a holding is an available record; physical access; occurrence (an accepted empirical input); which outcome is actual. Depth is lineage-address length, not time or distance. Draft 28 and single_event_receiver_gain remain independently accepted conditional results. Native bridge NOT_DERIVED. Broad C3/C4–C6 and physical origin remain OPEN.
