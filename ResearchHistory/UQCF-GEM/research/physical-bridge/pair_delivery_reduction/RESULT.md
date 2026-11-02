# T-235 — Pair-delivery premise reduction: result (draft, unreviewed until the Actions review closes)

Author: proteinfolding-grokbot (UQCF Science Agent), 2026-10-31 America/Phoenix (MST).
Authority: Aaron Spradlin's voice instruction of 2026-10-31 3:29 PM MST: shrink the set of not-derived inputs, derive what the axioms and definitions can now reach with every inference shown, and leave the rest labelled with its dependence stated precisely.
Parent: research/uqcf-overlapping-guard-exchange `0dfa5c60bd0a2838f70480035bff255428e934dd`. Preregistration: `PREREGISTRATION.md`, commit `4c8c0385831900e1f79b4f2d80776c153c3406d5` (3:35:52 PM MST), before any execution.
Status words: PROVED (general typed argument below), CHECKED (bounded exact computation), SUPPLIED, NOT_DERIVED. Nothing here is CLOSED or CERTIFIED. Native bridge NOT_DERIVED. scientific_breakthrough false.

## 0. Disclosures

- Prereg time correction. PREREGISTRATION.md §0 says the hand work ran 3:30–3:50 PM MST. It actually ended before the prereg commit at 3:35:52 PM MST. The commit is not amended (no force-push); this line is the correction.
- Exploratory local execution after the prereg commit, before the Actions run: `produce.py` was run twice on the box (Python 3.13.5, sympy 1.13.3), and `verify.py` and `test_controls.py` once each, under `/workspace/uqcf_scratch/t235/` (not in the repository). Results were GREEN and are the same predictions the Actions run tests; they are disclosed, not counted as the publication evidence. Between the two producer runs two output fields were added (`producer_sha256` for the false-provenance control, and `vertices` so the verifier can rebuild each producer tree); no checked value changed. Local digests: certificate `c3a9c672…5101`, verifier output `34da4b2a…85c0`, controls output `da0996e1…7c`.
- Prior art inside the project, so the new parts are not overstated. (a) `P1_CANONICAL_RECEIVER_ACQUISITION.md` already shows at the level of the retained grade itself (no read law) that y^(1)_a − y^(0)_a = x^(1)_u − x^(0)_u, without (Bl_D^a) or (Side_D). (b) d28 §31 already uses sibling exchange (SX_m), but at the climb's own forks and together with (PN), (POS) and (Bl_D^a); d28 §33 gives the minimal premise set (Bl_D^a)+(Side_D) for a single unit g e_{a_d}. What is new below is: for the balanced pair at a fork, in the read-law (holding) setting, (SX) at the record's own fork plus (PN) at the one step suffices, and κ plays no role; and the classification of event-invariant effects (Prop O), which says why any event witness has to be covariant.

## 1. Objects (frozen in the prereg, §1)

W a finite rooted tree (FCV L1), F^W = Q^W grades (FCV L6, relative units). p a vertex with two distinct leaf children u, v. Y = W \ {u}. P = P_{W,Y} the FCV P1 pushforward: P e_u = e_p, P e_z = e_z otherwise. I the FCV P2 zero extension, so P I = id_Y. σ the transposition of u and v; it fixes the root and preserves parents, so it is an FCV admitted relabeling and an automorphism of W. Δ = (e_u − e_v)/5 (the T-224/T-225 balanced pair; preparation SUPPLIED). Linear reads F := F̂_W on F^W, G := F̂_Y on F^Y; holding h_w(x) := F(x)_w.
(PN-step): G P = P F. (SX-fork): F σ = σ F. (Nd): h_u(e_u) ≠ h_v(e_u). c := (h_u(e_u) − h_v(e_u))/5.
Effect family anchored at p: a linear functional ℓ_X on F^X for every carrier X ⊆ W containing p. (INV): ℓ_{X\{l}} ∘ P_{X,X\{l}} = ℓ_X for every leaf l ≠ p of X. [0,p] is the chain from Genesis to p; depth(p) = |[0,p]| − 1.

## 2. Theorem P (pair delivery from sibling exchange) — PROVED

Claim. Assume only (PN-step) and (SX-fork). Then
  F(Δ) = c e_u − c e_v   and   G(PΔ) = c e_p − c e_v.
So before the event the receiver p and every vertex other than u, v hold 0 of the pair; after it the receiver p holds exactly c and every vertex other than p, v holds 0. The receiver's contrast is 0 → c, nonzero iff (Nd). Total holding is 0 before and after.

Proof.
1. σ e_u = e_v and σ e_v = e_u (definition of σ). So σΔ = −Δ.
2. By (SX-fork), F(e_v) = F(σ e_u) = σ F(e_u). Componentwise, h_w(e_v) = h_{σ(w)}(e_u) for every w ∈ W, because (σ y)_w = y_{σ(w)} for a permutation matrix of a transposition.
3. Therefore h_w(Δ) = (h_w(e_u) − h_{σ(w)}(e_u))/5 for every w (linearity of F, step 2).
4. If w ∉ {u, v}, σ(w) = w, so h_w(Δ) = 0 (step 3). In particular the receiver p holds 0.
5. If w = u: h_u(Δ) = (h_u(e_u) − h_v(e_u))/5 = c. If w = v: h_v(Δ) = (h_v(e_u) − h_u(e_u))/5 = −c. Hence F(Δ) = c e_u − c e_v.
6. By (PN-step), G(PΔ) = P F(Δ) = P(c e_u − c e_v) = c P e_u − c P e_v = c e_p − c e_v, using P e_u = e_p (u is the pruned leaf, its parent is p) and P e_v = e_v (v ∈ Y).
7. The receiver coordinate is 0 in step 4 and c in step 6, so the contrast is nonzero iff c ≠ 0 iff (Nd).
8. Totals: Σ F(Δ) = c − c = 0, and P preserves totals (FCV P1 fiber additivity), so Σ G(PΔ) = 0. The receiver's gain c is matched by the sibling's −c, which v holds before and after. QED.

Typing. (PN-step) is used only on the vector Δ. Nothing is used about (Bl_D^a), (Side_D), κ, (POS), cone-locality (S), or uniformity between carriers. The argument applies in every carrier W in which u and v are sibling leaves, with (SX-fork) imposed on that W (one automorphism of one carrier, as in d28 §31).
Remark P.1 (connection to d28). Under (PN) on the whole address class, Lemma 31.0 gives h_u(e_u) = A_u(u) and h_v(e_u) = A_v(p) (u, v leaves; v ∧ u = p), so c = (A_u(u) − A_v(p))/5. Under d28's (Diag_D) and (Side_D) along a climb through u this is κ/5, so Theorem P recovers the value of Corollary 31.3/Theorem 33.1 on the pair, while needing neither premise. Remark P.1 uses Lemma 31.0 and is not needed for Theorem P.
Remark P.2 (dimension, diagnostic). The reads allowed by Theorem P's premises on one carrier are F in the commutant of σ (dimension n² − 2n + 2: σ×σ acting on index pairs has n² − 2n + 2 orbits) with P F (e_u − e_p) = 0 (this is exactly the condition that G := P F I satisfies G P = P F, because ker P = span(e_u − e_p) and P I = id). In the commutant F e_u is an arbitrary vector (F e_v = σ F e_u is then fixed) while F e_p is σ-invariant, so P F e_u can hit any vector of F^Y and the n − 1 equations are independent: dimension n² − 3n + 3.

## 3. Proposition K (κ is not load-bearing for the pair) — PROVED

Claim. F^tot(x) = (Σ_w x_w) e_0 and F^dif = id − F^tot both satisfy (PN) for every leaf pruning of every carrier (with the same formula on the smaller carrier) and commute with every admitted relabeling. F^tot has total holding of a unit κ = 1 and c = 0. F^dif has κ = 0 and c = 1/5.
Proof.
1. P_{X,Z} preserves totals (FCV P1) and fixes e_0 (Genesis is never pruned). So F^tot_Z(P x) = (Σ P x) e_0 = (Σ x) e_0 = P((Σ x) e_0) = P F^tot_X(x). (PN) holds.
2. A relabeling π fixes the root and permutes coordinates, so Σ(πx) = Σx and π e_0 = e_0: F^tot π = π F^tot.
3. id satisfies both trivially; (PN) and relabeling-commutation are linear conditions, so F^dif = id − F^tot satisfies both.
4. κ := Σ_w F(e_p)_w: for F^tot it is 1; for F^dif it is 1 − 1 = 0.
5. c = (F(e_u)_u − F(e_u)_v)/5: F^tot(e_u) = e_0 and u, v ≠ 0, so c = 0. F^dif(e_u) = e_u − e_0, so c = (1 − 0)/5 = 1/5. QED.
Consequence. κ ≠ 0 is neither sufficient (F^tot) nor necessary (F^dif) for a nonzero pair contrast. Scaling F by λ scales both κ and c, so the size of either is a unit gauge (TYPE_LEDGER: relative units, not observer calibration).

## 4. Proposition N (each premise of Theorem P is needed) — PROVED

(a) Drop (SX-fork). F^pre(x) := (x_p + x_u − x_v) e_p on W and G^pre(y) := (y_p − y_v) e_p on Y. Check (PN-step): (P x)_p = x_p + x_u and (P x)_v = x_v, so G^pre(P x) = (x_p + x_u − x_v) e_p = P F^pre(x) (P fixes e_p). But F^pre(Δ) = (1/5 + 1/5) e_p = (2/5) e_p: the receiver is informed before the event. (SX) fails: F^pre(e_v) = −e_p ≠ e_p = σ F^pre(e_u).
(b) Drop (PN-step). F = id, G = 0. (SX) holds, F(Δ) = Δ so c = 1/5, but G(PΔ)_p = 0 ≠ c. (PN) fails: G P = 0 ≠ P.
(c) (Nd) is not automatic. c is a linear functional on the admissible space, nonzero (id gives 1/5), so (Nd) fails exactly on a hyperplane, which contains F^tot and the zero read.

## 5. Proposition O (event-invariant effects factor through the lineage chain) — PROVED

Claim. An effect family anchored at p satisfies (INV) iff there is α ∈ (F^{[0,p]})* with ℓ_X = α ∘ P_{X,[0,p]} for every carrier X ∋ p. The solution space has dimension depth(p) + 1.
Proof.
1. (⇐) Let l ≠ p be a leaf of X. Every vertex of [0,p] other than p has the descendant p in X, so it is not a leaf of X; hence l ∉ [0,p]. X \ {l} is a carrier containing [0,p]. By FCV P1 composition, P_{X\{l},[0,p]} ∘ P_{X,X\{l}} = P_{X,[0,p]}. Apply α: ℓ_{X\{l}} ∘ P_{X,X\{l}} = ℓ_X.
2. (⇒) Induction on m(X) := |X \ [0,p]|. If m = 0, X = [0,p], P_{X,[0,p]} = id; put α := ℓ_{[0,p]}.
3. If m > 0, pick w ∈ X \ [0,p] of maximal depth. A child c of w in X is deeper than w, and c ∉ [0,p] (otherwise its parent w would be in the ancestor-closed chain [0,p]); this contradicts maximality. So w is a leaf of X, and w ≠ p.
4. By (INV), ℓ_X = ℓ_{X\{w}} ∘ P_{X,X\{w}}. X \ {w} is a carrier containing p with m one smaller; by induction ℓ_{X\{w}} = α ∘ P_{X\{w},[0,p]}, with the same α = ℓ_{[0,p]}.
5. By FCV P1 composition, ℓ_X = α ∘ P_{X\{w},[0,p]} ∘ P_{X,X\{w}} = α ∘ P_{X,[0,p]}.
6. The map α ↦ (α ∘ P_{X,[0,p]})_X is linear and injective (its [0,p] component is α), and by steps 1–5 its image is the whole solution space. dim = dim F^{[0,p]} = depth(p) + 1. QED.
Corollary O.1. P_{W,[0,p]} sends e_u and e_v both to e_p, so Δ ∈ ker P_{W,[0,p]}, and every (INV) effect has ℓ_W(Δ) = 0 and ℓ_Y(PΔ) = ℓ_W(Δ) = 0. More generally ℓ_Y ∘ P = ℓ_W, so no (INV) effect distinguishes before from after. The cone totals C_0, C_p of T-225/T-233 are (INV) effects, which explains why that control fails.
Corollary O.2 (what N1 has to be). The T-217 criterion E_A(τ_u) ≠ E_A(τ_0) needs an effect that is not (INV). The receiver coordinate x ↦ x_p is one such effect: e_u has p-coordinate 0 on W and P e_u = e_p has p-coordinate 1. Any read that can deliver the event is therefore event-covariant, like F in Theorem P. This generalizes T-225 and d28 Prop 25.1 from the cone totals to every invariant effect.

## 6. Exact checks (bounded evidence; CHECKED, not a proof)

Universes (prereg §4): U_P = rooted unlabeled trees with 3 ≤ n ≤ 7 and sibling-leaf pairs up to automorphism; U_O = trees with 1 ≤ n ≤ 6 and every anchor p up to automorphism. Producer `produce.py` (recursive forest enumeration, sympy nullspaces). Verifier `verify.py` (stdlib only: parent-array enumeration deduplicated by an AHU string, σ-orbit parameterization, own Fraction Gaussian elimination, PN for the K witnesses checked at every leaf pruning of each carrier, provenance by producer sha256). Controls `test_controls.py` (16 tampered certificates that must be rejected).
Local disclosed values (the Actions values are in EVIDENCE.md once published): tree counts 1, 1, 2, 4, 9, 20, 48; U_P 56 cases (1, 2, 5, 13, 35 for n = 3..7; the hand predictions 1 and 2 for n = 3, 4 matched), 1440 basis reads checked, dim = n² − 3n + 3 in every case; K witnesses as stated in every case; N(a), N(b) witnesses in every case; T-233 cone-total control 0 before and 0 after in every case (fails to separate, as preregistered); U_O 151 cases over 1073 carriers, dim = depth + 1 and factorization in every case. 16/16 tampers rejected, honest certificate accepted.

## 7. Ledger of not-derived inputs after this stage (ranked by how much of the N1 target rests on each)

| # | Input | Status after T-235 | Exact dependence |
|---|---|---|---|
| 1 | Access/record law (N1 core): that a holding is an available record of the receiver, that p performs a read | NOT_DERIVED | Needs an inherited law naming the receiver's effect. Prop O now types it: it must be event-covariant (not INV). Theorem P: if it is a linear holding read with (PN-step), (SX-fork), (Nd), the pair is delivered to p with contrast c. Not reached: holding ⇒ record. |
| 2 | (Bl_D^a), (Side_D), κ ≠ 0 | Removed from the premise set of the pair contrast (Theorem P, Prop K). Still NOT_DERIVED as statements | Still needed for d28's single-unit transfer (ET_D) of g e_{a_d}; not needed for Δ. |
| 3 | (PN) read ledger | NOT_DERIVED | Theorem P needs it only at the event step and only on Δ. FCV proves naturality of P, I, R, H, not of an arbitrary read. |
| 4 | (SX-fork) | NOT_DERIVED | Would follow if reads were required to be natural under FCV admitted relabelings (TYPE_LEDGER proves this for P, I, R, H only). No source makes a read law natural; T-235 does not assume one. |
| 5 | (Nd) | NOT_DERIVED | Generic (complement of a hyperplane) but not forced; F^tot and the zero read violate it while satisfying (PN) and (SX). |
| 6 | N2 complementary receiver (R2) | NOT_DERIVED | Typing remark: after the P1 step every F^Y object reaches u only through P (Prop O, (PN)), and u has no coordinate in Y. A complementary receiver would need a retained pre-event carrier; P1 does not keep one (FCV P2's projectors live on the pre-event carrier). Not a no-go. |
| 7 | N3 own-command/own-view record; N4 physical counterpart of #118's q memory and coupling | NOT_DERIVED | Unchanged from T-233 items 1 and 5. |
| 8 | Preparation of Δ; enactment; occurrence (an accepted empirical input) | SUPPLIED | Unchanged. |
| 9 | Palette order; controller memory/coupling; shifted interface G_Y(s); UNRESOLVED_PHYSICAL_REALIZATION; CPTP leg; a unique response law | SUPPLIED / NOT_DERIVED | Unchanged from T-233 items 1–5 and TYPE_LEDGER "still not supplied". |

No supplied input was promoted to derived.

## 8. Scope fence

No geometry, no fundamental clock, no dark-matter primitive, no fitting. Time is pruning / ordered recoverability update; depth is lineage-address length. The finite checks are bounded evidence; the general claims rest on §§2–5. Nothing here establishes receiver access, that any vertex performs a read, preparation, occurrence or the native bridge. Native bridge NOT_DERIVED. scientific_breakthrough false. Not CLOSED, not CERTIFIED (AGENTS.md: only after a post-merge audit).
