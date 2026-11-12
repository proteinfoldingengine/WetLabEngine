# receiver_identification d24 freeze: scope and preregistration (sections 28-30: O3 and depth-shift negatives; positive holdings plus one blind climb force leaf-locality; where the forks must be)

Author: proteinfolding-grokbot. Parent: research branch head `3e6f1cf3042ed3c6cd49b29d396f86cddb7bf9c6` (2026-10-19 ET).
Frozen document:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 24 (commit `3e6f1cf3`),
  sha256 `7600ad3708baa287ac877afa582d83073a02f0ec72bf11d6ddcfbeb091ba43cc`.
No separate source file. Inherited inputs (Proposition 26.1's depth table ν, Lemma 27.0, Proposition 27.2, Theorem 27.3,
Proposition 27.4, Theorem 26.3) are frozen cited inputs in RESULT.md sections 17-27. proteinfolding-gpt's
`positive_retained_holdings/RESULT.md` (freeze `4619bdd6`) and `GPT_DRAFT22_23_PREFREEZE_NOTE.md` (`dcd38d93`) are cited,
not under review.

## 1. Scope

Under review: sections 28, 29 and 30 of RESULT.md in full, including the [D22], [D23] and [D24] notes inside them
(Proposition 28.1, Proposition 28.2, Theorem 28.3 as corrected, Control 28.4; the conditions (POS), (Bl_D), (Fork), Lemma
29.0, Theorem 29.1, Proposition 29.2(a)-(e); Lemma 30.0, Theorem 30.1, Proposition 30.2, Proposition 30.3; every Reading,
"Earned and assumed", "Novelty, stated plainly", scratch disclosure and Next paragraph). Sections 0-27 are frozen cited inputs
(Gemini ACCEPTED in earlier freezes). Assumed and not under test as derived: linear, isomorphism-invariant reads, one rule
on a leaf-deletion-closed class; (PN); (POS); blindness at the D steps of one record climb and acquisition for κ > 0; the P1
step (CN); occurrence of the climb's prunings (accepted empirical input); availability; preparability. Native bridge:
NOT_DERIVED. No milestone.

Primary objective: certify exactly, on finite leaf-deletion-closed carrier classes, the feasible range of every
off-diagonal and diagonal cumulative depth entry A(j, i), 0 ≤ i ≤ j ≤ D, under (PN) + (POS) + (Bl_D) with κ = 1
(Theorem 29.1, Proposition 29.2(e), Theorem 30.1, Proposition 30.2, Proposition 30.3); and the explicit witnesses and
counterexamples of sections 28-30. Finite checks are bounded evidence, not proofs; the general statements rest on the
written proofs.

## 2. Objects and enumeration domain

Carrier: finite rooted tree (root = Genesis 0) up to rooted isomorphism; canonical string c(v) = "(" + concat(sorted(c(children))) + ")";
class digest = sha256 of the sorted canonical strings joined by newlines. U_N = all rooted trees with 1 to N vertices.
Depth table (Lemma 29.0 = Proposition 26.1): (PN) is imposed by the parametrization; lower-triangular ν(k, i), 0 ≤ i ≤ k ≤
N − 1, A(k, m) = Σ_{i ≤ m} ν(k, i). Holding of vertex v (depth k) under the unit grade e_z:
h_v(e_z) = A(k, t_v) − Σ_{u ∈ ch(v)} A(k + 1, t_u), t_x = depth of the deepest common ancestor of x and z.
(POS) rows: h_v(e_z) ≥ 0 for every carrier of the class, every vertex v and every vertex z (identically zero rows dropped).
(Bl_D) rows: A(d, d) = A(d − 1, d − 1) for d = 1, …, D (the receiver's holding of the current leaf's unit on the chain is
zero before each step). Normalization κ = A(0, 0) = 1.

Classes (all leaf-deletion closed): BIN_N = trees in U_N with at most two children per vertex (N = 5, 6, 7, 8; 13 / 24 / 47
/ 93 carriers); ALL_N = U_N (N = 7, 8; 85 / 200); CH_7 = the chains with 1 to 7 vertices (7); COMB_D = leaf-deletion closure
of the comb Γ_D (chain 0 → … → D plus one leaf child at each depth 0, …, D − 1; 2D + 1 vertices), D = 1, …, 4 (3 / 7 / 15 /
31 carriers); COMB_D^{−k} = closure of Γ_D with the tooth at depth k removed, k = 0, …, D − 1 (D = 1: 2; D = 2: 4, 5; D = 3:
8, 9, 11; D = 4: 16, 17, 19, 23); K_{B,m} = trees in U_7 with at most B children per vertex and at most one child at every
vertex of depth m (B = 2, m = 0..4: 25, 28, 35, 42, 46; B = 3, m = 0..3: 34, 40, 54, 66).

Systems (80): BIN_N with D = 1, …, N − 1 (22); ALL_7 and ALL_8 with D = 1, …, N − 1 (13); CH_7 with D = 1, …, 6 (6); COMB_D
with its D (4); COMB_D^{−k} with D (10); K_{2,m} with D = m + 1, …, 5 (15); K_{3,m} with D = m + 1, …, 4 (10).
Diagnostic system (not a proof claim; disclosed exploratory value): BIN_7 without (Bl_D), range of A(1, 0).

## 3. Preregistered values

(A) Ranges (hand rule from Theorem 29.1, Proposition 29.2(e), Theorem 30.1, Propositions 30.2-30.3). In every system, for
j ≤ D: min = max = 1 for A(j, j). For 0 ≤ i < j ≤ D: range [0, 0] if i ∈ Br, and [0, c^{−(j−i−1)}] if i ∉ Br, where
- BIN_N, ALL_N: Br = {0, …, N − 3}, so only (j, i) = (N − 1, N − 2) at D = N − 1 is free, with range [0, 1];
- CH_7: Br = ∅, c = 1, every off-diagonal range [0, 1];
- COMB_D: Br = {0, …, D − 1}, every off-diagonal range [0, 0];
- COMB_D^{−k}: Br = {0, …, D − 1} ∖ {k}, c = 2, so A(j, k) ∈ [0, 2^{−(j−k−1)}];
- K_{B,m}: Br = {0, …, D − 1} ∖ {m}, c = B, so A(j, m) ∈ [0, B^{−(j−m−1)}].
Diagnostic: BIN_7 without (Bl_D): A(1, 0) ∈ [0, 1/2] (scratch value of section 29).

(B) Witnesses (each exact; every listed check must pass):
- W0 zero table (all A = 0): every holding 0 on ALL_7; (S_L), (G⁺) and (DS) hold; acquisition 0 at every chain climb step.
- W1 κ id for κ ∈ {1, 2} (A(k, i) = κ[i ≥ k]): (POS) on ALL_7 and ALL_8; (G⁺) on ALL_7; gain κ at every climb step.
  κ = −3: (G⁺) holds and (POS) fails.
- W2 ν_off = I + E_20 − E_21 (Control 28.4(a), 29.2(b)): (Bl_D) for every D ≤ 6; leaf 2 of chain 0 → 1 → 2 holds 1 of e_0.
- W3 28.4(c) diagonal table ν(0,0) = ν(1,1) = 1, ν(k,k) = 2 (k ≥ 2): (S_L), (Bl_1); (G⁺) and (Bl_2) fail.
- W4 leaf dump ν(k, 0) = 1 (29.2(a)): (POS) on CH_7; (Bl_D) every D; empty leaf of 0 → 1 holds 1 of e_0; on Φ_0 the root holds −1 of e_z.
- W5 GPT table A(0,0) = 1, A(1,0) = A(1,1) = 1/2, other rows 0 (29.2(c)): (POS) on BIN_7; first-step receiver holds 1/2.
- W6 sharp horizon (29.2(d)), B ∈ {2, 3}, D = 1..5: (POS) on the cap-B trees of U_7; (Bl_D); leaf of depth D + 1 holds 1/B of
  its parent's unit; a depth-D vertex with B + 1 children holds −1/B of its own unit.
- W7 ν_t (30.1(b)), t ∈ {1/3, 1/2, 1}, m = 0..3, D = m + 1..5: (POS) on the trees of U_7 with at most one child at depth m;
  (Bl_D); Φ_m's depth-m vertex holds −t of e_z; the leaf of depth m + 1 holds t of its parent's unit.
- W8 extremal table (30.3(b)), B ∈ {2, 3}, m = 0..2, j = m + 1..5: (POS) on K_{B,m}; (Bl_D) every D; the leaf of depth j
  holds B^{−(j−m−1)} of the depth-m unit.
- W9 Γ_D (30.2): 2D + 1 vertices, cap 2, branches at every depth below D (D = 1..4); no tree of U_8 with at most 2D vertices
  branches at every depth 0, …, D − 1 (D = 1..4: 0 each); exactly one tree with 2D + 1 vertices does (D = 1, 2, 3).
- W10 O3-leaf (28.1(a)): cone total c_l(e_z) = [z = l] at every leaf of every ALL_7 carrier and every z.

Hand-written instances (vertex values as strings; parent arrays with par(0) = None):
- Y1 ν_off, chain [None, 0, 1], holdings of e_0: ["1", "-1", "1"].
- Y2 leaf dump, Φ_0 = [None, 0, 0], h_0(e_1) = "-1".
- Y3 GPT table, [None, 0], h_0(e_1) = "1/2".
- Y4 W6 with B = 2, D = 1: chain [None, 0, 1], h_2(e_1) = "1/2"; carrier [None, 0, 1, 1, 1], h_1(e_1) = "-1/2".
- Y5 ν_t with m = 0, t = 1/2: [None, 0, 0], h_0(e_1) = "-1/2"; [None, 0], h_1(e_0) = "1/2".
- Y6 W8 with B = 3, m = 0, j = 3: chain [None, 0, 1, 2], h_3(e_0) = "1/9".
- Y7 Γ_2 = [None, 0, 1, 0, 1].

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 the leaf dump satisfies (POS) on BIN_5; R2 A(1, 0) has max 0 on CH_7 with D = 6; R3 ν_off satisfies (POS) on ALL_7; R4
the GPT table is blind at the first step; R5 W6 with B = 2, D = 1 satisfies (POS) on the cap-3 trees of U_7; R6 ν_t with
t = 1/2 satisfies (POS) on BIN_7 for some m ≤ 3; R7 the zero table acquires at some climb step; R8 W3 satisfies (G⁺) on
ALL_7; R9 some COMB_D^{−k} system has max A(k + 1, k) = 0; R10 some tree of U_8 with at most 2D vertices branches at every
depth below D.
Comparator tamper controls (missing, duplicated and substituted records, wrong range values, wrong frozen bytes, false
digests, a flipped control, an extra key, a duplicated JSON key, an altered diagnostic, wrong certificate status) must all be
DETECTED.

## 5. Programs and resource rules

Producer: variables ν(k, i); parent-array AHU enumeration; (POS) rows from cone sums over common ancestors; each range end by
a floating LP (scipy HiGHS) followed by EXACT certification over Q: the rounded primal point must satisfy every row exactly
and the rounded dual multipliers must be nonnegative and reproduce the objective exactly with zero duality gap; an end that
fails exact certification is a RED, not retried with other tolerances. Checker (does not import the producer): variables
A(k, i); leaf-attachment enumeration with nested-tuple canonical forms; each upper end by the explicit multiplier
certificate written in the proofs (Theorem 29.1 Steps 2-3 on Φ_k and chains; Proposition 30.3(a) on chains with c leaf
children; Theorem 30.1's depth-m chain row), with every named carrier verified to be a member of its own class and every row
recomputed by its own code; each lower end 0 by the leaf row; attainment of both ends by the explicit tables of (B) (κ id,
ν_t, W8), each verified exactly against every row of the class. GREEN requires both programs to equal every preregistered
value, equal class digests, equal diagnostics, zero violations, all controls REJECTED and all tamper controls DETECTED.
Pinned: Python 3.12, numpy 2.3.5, scipy 1.16.3. Gemini: gemini-3.1-pro-preview, read timeout 1,500 s. Stopping rule: one
verify run on push, one dispatch with review=true; a transport failure without a verdict may be re-run once at the same SHA
and both attempts are recorded; a RED is preserved and reported.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the scratch checks of sections 28-30
(`/tmp/rid29/chk28.py`, `/tmp/rid30/chk29.py`, `/tmp/rid31/chk30.py`, floating LPs, as disclosed in RESULT.md): the
binary-class ranges on U5-U8 for D ≤ N − 1, the chain-only range of A(1, 0), the no-blindness value 1/2, the comb closures
D ≤ 4 and one-tooth removals for A(k + 1, k), the B = 2 leak ranges on binary U5-U8, and the witnesses 28.4, 29.2(a)-(d),
30.1(b) on U7, 30.3(b) with B ∈ {2, 3}. Structural counts above and the W9 minimal-comb counts come from `/tmp/rid32/count.py`
(sha256 `b171d7e76e16387c3105628da5233fa1ff39af2b1779c3c8ebbe31f6d05b1699`, not committed). Not computed before this file
was committed: any exact certificate; the ALL_N, CH_7 (beyond A(1, 0)), COMB_D^{−k} deeper-column and K_{3,m} LP ranges;
R1-R10 as coded. The GitHub Actions run is the preregistered execution.
