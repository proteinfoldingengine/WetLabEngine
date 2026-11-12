# receiver_identification d28 freeze: scope and preregistration (section 33: the event transfer is two linear equalities per lineage)

Author: proteinfolding-grokbot. Parent: research branch head `9ef10e3e9238155e9bd18d85fed7fa8ecb1cb4de` (2026-10-19 ~20:05 ET).
Frozen document:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 28 (commit `cd4db0fb`),
  sha256 `a747459613ab088fb363c583cc6cd5ed4333850b64758b88fbba14fcd50529e4`.
Sections 0-32 are frozen cited inputs (Gemini ACCEPTED in earlier freezes; sections 31-32 in the d27 freeze, run 39331510927
attempt 2). proteinfolding-gpt's notes are cited, not under review.

## 1. Scope

Under review: section 33 of RESULT.md in full (the conditions (ET_D), (Diag_D), (Side_D) and the departure point δ(c);
Lemma 33.0; Theorem 33.1 (i)-(iii) and its after-step statement; Proposition 33.2(a)-(d); Corollary 33.3(a)-(b) with the
Proposition 26.4(a) example; the Reading, "Earned and assumed", "Novelty, stated plainly", the scratch disclosure and Next), and
the draft-28 header line. Assumed and not under test as derived: linear reads, one map per carrier on the address class; (PN);
the P1 step (CN); (Bl_D^a); (Side_D); κ ≠ 0 for acquisition; occurrence of the prunings (accepted empirical input);
availability; preparability. Native bridge: NOT_DERIVED. No milestone.

Primary objective: certify exactly over Q, on finite address trees, that the linear span of the (ET_D) equalities equals the
span of the (Diag_D) and (Side_D) equalities, with rank D + |Side_D| (Theorem 33.1, Proposition 33.2(a)); that no other table
entry enters any (ET_D) equality (Proposition 33.2(b)); Lemma 33.0 as an identity of linear forms; and the explicit tables of
section 33. Finite checks are bounded evidence, not proofs; the general statements rest on the written proofs. Corollary
33.3(a) is not re-verified here: it cites Theorem 31.1(a)-(b), whose side-subtree ranges were exactly certified in the d27
freeze (push run 39325886792) and reviewed there; this freeze checks only that the transfer needs no positivity.

## 2. Objects and enumeration domain

Addresses are tuples of child indices; Genesis is (). Address string "r" followed by "." + index per entry. Trees:
- TM: root children (0, 1, 2), binary below, height 3 (22 addresses).
- MX: () → {(0), (1)}; (0) → (0, 0); (0, 0) → {(0, 0, 0), (0, 0, 1)}; (1) → (1, 0) (7 addresses; the climb vertex (0) has no
  second child).
- CH: the chain () → (0) → (0, 0) → (0, 0, 0).
- S4: () → {(0) → (0, 0), (1)} (the tree 0 → {1 → 2, 3} of Corollary 33.3(b), with 1 = (0), 2 = (0, 0), 3 = (1)).
Carriers: all rooted subtrees. Variables A[v|w] for every address v and ancestor-or-self w; κ = A[()|()]. Holding
(Lemma 31.0): h_v(e_z) on W = A[v | v∧z] − Σ_{children u of v in W} A[u | u∧z]. Climbs: TM, MX, CH: a_d = (0,)^d,
D ∈ {1, 2, 3}; S4α: a_1 = (0), D = 1; S4β: a_1 = (1), D = 1. Systems (11): TM|1, TM|2, TM|3, MX|1, MX|2, MX|3, CH|1, CH|2,
CH|3, S4α|1, S4β|1.
Rows (linear forms in the variables, κ a variable):
- (ET_D): for each d ≤ D, each carrier W in which a_d is a leaf and each v ∈ W, the form h_v(e_{a_d}) − κ·[v = a_d]
  (identically zero forms dropped, duplicates merged).
- (Diag_D): A[a_d|a_d] − κ, d = 1..D. (Side_D): A[c|δ(c)] for every c not on the climb and not at or below a_D, δ(c) = c ∧ a_D.

## 3. Preregistered values

(A) Per system (both programs; hand values from Theorem 33.1 and Proposition 33.2):
- span(ET_D) = span(Diag_D ∪ Side_D) over Q, and rank = D + |Side_D|.
- |Side_D|: TM 14, 17, 18; MX 2, 2, 3; CH 0, 0, 0; S4α 1; S4β 2. Rank: TM 15, 19, 21; MX 3, 4, 6; CH 1, 2, 3; S4α 2; S4β 3.
- Support (variables with a nonzero coefficient in some ET row) = {κ} ∪ {A[a_d|a_d]} ∪ {A[c|δ(c)]}: sizes TM 16, 20, 22;
  MX 4, 5, 7; CH 2, 3, 4; S4α 3; S4β 4. Every other variable is free (Proposition 33.2(b)).
- Carriers with a_d a leaf: TM 676, 3,380, 6,760 (d = 1, 2, 3); MX 3, 3, 6; CH 1, 1, 1; S4α 2; S4β 3.
- The number of distinct nonzero ET rows is computed by both programs and must agree; it is not preregistered.
Structural: carriers TM 17,576, MX 18, CH 4, S4 6; variables (Σ_v (depth(v) + 1)) TM 73, MX 19, CH 10, S4 8.

(B) Exact tables (each must hold, both programs):
- X1 Lemma 33.0: Σ_{v ∈ W} h_v(e_z) − κ is the zero form for every carrier W and z ∈ W, on TM, MX, CH and S4.
- X2 Proposition 33.2(a): for TM|3, MX|3, CH|3 and S4β|1, for every (Diag_D) and (Side_D) entry and ε ∈ {1/2, −1}: the κ id
  table (κ = 1, A[v|v] = 1, all else 0) with that entry changed by +ε satisfies every other (Diag_D) and (Side_D) equality and
  violates (ET_D); witness: for a side entry of c leaving at a_i, h_c(e_{a_{i+1}}) = ε on [0, a_{i+1}] ∪ [0, c]; for the
  diagonal entry at a_d, h_{a_{d−1}}(e_{a_d}) = −ε on [0, a_d].
- X3 Proposition 33.2(b) leak on TM|3: κ id with A[a_{m+1}|a_m] = t, m ∈ {0, 1, 2}, t ∈ {−2, −1/2, 1/2, 1, 3}: (ET_3) and the
  after-step statement hold on every carrier; full (POS) fails, with witness h_{a_m}(e_{u_m}) = −t on [0, a_{m+1}] ∪ {u_m}
  (u_m = a_m + (1,)) for t > 0 and h_{a_{m+1}}(e_{a_m}) = t on [0, a_{m+1}] for t < 0; (FC) fails (F̂ e_{a_m} ≠ e_{a_m} on
  [0, a_{m+1}]).
- X4 scope of the "second child" qualifier, MX|3, m = 1 (a_1 = (0) has no second child): κ id with A[(0,0)|(0)] = t: for
  t ∈ {1/2, 1}, full (POS) holds on all 18 carriers; for t ∈ {−1/2, 3/2} it fails; (ET_3) holds and (FC) fails for all four t.
- X5 Proposition 33.2(b), (d): the general table G(κ) on TM|1, TM|2, TM|3, MX|3, CH|3 and S4α|1, for κ ∈ {1, 2, −1, 0}:
  A[a_d|a_d] = κ (d ≤ D), Side entries 0, and every other variable A[v|w] set to (int(sha256(key)[:8 hex], 16) mod 7) − 3,
  key = the UTF-8 string "A[" + s(v) + "|" + s(w) + "]"; (ET_D) and the after-step statement F̂_{W − a_d} e_{a_{d−1}} =
  κ e_{a_{d−1}} hold on every carrier in which a_d is a leaf.
- X6 Corollary 33.3(b) on S4: table A[()|()] = 1, A[(0)|()] = 0, A[(0)|(0)] = 1, A[(0,0)|()] = 1, A[(0,0)|(0)] = 0,
  A[(0,0)|(0,0)] = 1, A[(1)|()] = 0, A[(1)|(1)] = 1. (S) (A[v|w] = 0 for every strict ancestor w) fails; climb α: (Bl_1^a),
  (Side_1) and (ET_1) hold, and the carriers in which (0) is a leaf are exactly {(), (0)} and {(), (0), (1)}; climb β: (Side_1)
  fails and (ET_1) fails.
Instances (exact strings): Y1 X6 climb β, F̂ e_(1) on the full S4 carrier in the order ((), (0), (0, 0), (1)) =
["0", "-1", "1", "1"]; Y2 X2 on TM|3, side entry A[(0,0,1)|(0,0)], ε = 1/2: "1/2"; Y3 X2 on TM|3, diagonal at a_2, ε = −1:
"1"; Y4 X3, m = 1, t = 1/2: "-1/2"; Y5 X4 with t = 1, holdings of e_(0) on {(), (0), (0, 0)} in that order = ["0", "0", "1"].

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 span(Diag_2) ⊇ span(ET_2) on TM; R2 span(Side_2 ∪ {κ}) ⊇ span(ET_2) on TM (here {κ} is the form κ); R3 A[(0)|()] enters
some ET row of TM|3; R4 the X6 table satisfies (S); R5 the X6 table satisfies (ET_1) for climb β; R6 span(Diag_3 ∪ Side_3
minus the row of (0, 0, 1)) ⊇ span(ET_3) on MX; R7 X3 with m = 0, t = 1/2 satisfies full (POS) on TM; R8 the X2 table with
A[(0,0,1)|(0,0)] = 1/2 satisfies (ET_3) on TM; R9 X4 with t = 3/2 satisfies full (POS) on MX.
Comparator tamper controls (missing, duplicated and substituted records, a wrong rank, a wrong support size, a wrong frozen hash,
a false digest, a wrong count, false provenance, role confusion, a missing or flipped control, an extra key, a hidden violation,
a duplicated JSON key, a wrong instance) must all be DETECTED.

## 5. Programs and resource rules

Producer: recursive enumeration of rooted subtrees; rows as sparse dicts over Fraction; ranks by exact Gaussian elimination
(reduced echelon basis) over Q; span equality by rank(ET) = rank(DS) = rank(ET ∪ DS); support by scanning the ET rows; tables
evaluated with its own holding function. Checker (does not import the producer): bitmask enumeration of vertex subsets closed
under parents; its own holding function; (i) ⇒ (iii) by explicit certificates: each Diag row as −Σ_{j ≤ d} of the ET row
h_{a_{j−1}}(e_{a_j}) on [0, a_j], each Side row as the ET row h_c(e_{a_{i+1}}) on [0, a_{i+1}] ∪ [0, c], verifying that each
named carrier is in the system's own carrier set with a_d a leaf; (iii) ⇒ (i) by expressing every ET row as the combination
of the proof of Theorem 33.1 (leaf: Diag_d; ancestor a_i: Diag_i − Diag_{i+1} − Σ Side over its other children; off-climb v:
Side_v − Σ Side over its children), each verified identically over Q; independence (rank) from X2 (each row is violated alone
by a table satisfying all the others); support by scanning; controls R1, R2, R6 by exhibiting an ET row outside the smaller
span, certified by a table satisfying the smaller system and violating that row. GREEN requires both programs to equal every
preregistered value, equal digests and counts, zero violations, all controls REJECTED and all tamper controls DETECTED.
Pinned: Python 3.12, standard library only (fractions, hashlib). Gemini: gemini-3.1-pro-preview, read timeout 1,500 s. Review
prompt (lean, as in d27 amendment 1): exact byte excerpts of RESULT.md, E1 = [0, 886) (title and draft-28 header line) and
E2 = [266359, 389240) (sections 26 to 33 in full), each with offsets and sha256, the whole-file hash asserted; sections 0 to
25 omitted as cited inputs (the referee reports any step it cannot check as a missing assumption); plus this file and the full
compare.json, whose sha256 must equal that of the push run (recorded in the receipt); on HTTP 429 or 503 one preregistered
300 s cooldown retry inside the job. Stopping rule: one verify run on push, one dispatch with review = true; a transport
failure without a verdict may be re-run once at the same SHA, and both attempts are recorded; if Gemini returns 429 or 402
again, no further calls are made and it is reported as a blocker. A RED is preserved and reported.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the scratch check of section 33
(`/tmp/rid35/chk33.py`, as disclosed in RESULT.md): on TM with D = 1-3 the (Side_D) counts, random integer tables with
(Diag_D) and (Side_D), single perturbations and the leak family. Not computed before this file was committed: any rank, span
or support computation; MX, CH and S4 systems; X1 as a symbolic identity; X4; X5 with the hash rule; X6 as coded; R1-R9 as
coded. The GitHub Actions run is the preregistered execution.

## 7. Dry-run disclosure and one clarification (added with the code commit, before any Actions run)

Disclosure: before committing the programs, the producer, the checker and the comparator were each run once locally on the box
(Python 3.12/3.13 standard library) to debug them. On that first run every system value, table, instance and control equalled
the preregistered values of sections 3 and 4, zero violations, 19/19 tamper controls detected (local compare.json sha256
`c99d5ad97a9bdd153a0fa979cf3312366a8e2b1f906fdfbdffb56a43a3531dad`, informative only). The review script's prompt assembly was run once with the network call stubbed out (no request
sent, no key used): about 145 KB. Clarification of section 5: the review job records the sha256 of the compare.json it sends;
the receipt checks that it equals the push run's compare.json (the programs are deterministic and unchanged between the two
runs). No preregistered value is changed. The Actions run on push is the preregistered execution.
