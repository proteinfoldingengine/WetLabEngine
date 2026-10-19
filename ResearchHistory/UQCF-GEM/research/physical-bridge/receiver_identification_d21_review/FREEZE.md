# receiver_identification d21 freeze: scope and preregistration (section 27, a leaf reads only what it holds, and one record climb fixes the reads up to its depth)

Author: proteinfolding-grokbot. Parent: research branch head `bf82797f58b31453bcf6fed5014bebb681683464` (2026-10-19 ET).
Frozen document:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 21 (commit `bf82797f`),
  sha256 `7c0eb6f830e6ca167ec62839e760d092c88fb1084ce72c91877b7c314414b229`.
No separate source file: the inherited inputs of section 27 (the P1 step and zero extension, Proposition 26.1's depth
matrix ν, (26.2), Lemma 17.0, Theorem 17.3, Corollary 17.6) are stated in RESULT.md sections 17-26, which are frozen cited
inputs.

## 1. Scope

Under review: section 27 of RESULT.md in full (Where this sits, Setting, the conditions (S_L), (E0), (W2_1), (CL_D), Lemma
27.0, Lemma 27.1, Proposition 27.2, Theorem 27.3, Proposition 27.4(a)-(d), the Reading paragraphs, "Earned and assumed",
"Novelty, stated plainly", the scratch disclosure, Next) and the [D21] revision note. Sections 0-26 and [D16] are frozen
cited inputs (Gemini ACCEPTED in earlier freezes). Assumed and not under test as derived: linear, isomorphism-invariant read
maps on every finite carrier; (PN); (S_L), equivalently (E0); acquisition on the one-location pair at the D steps of one
record climb (or climbs of every depth for the whole class); the P1 step (CN assumed); the occurrence of the climb's
prunings (accepted empirical input); availability (A0)-(A3') and (U); the declared pair; preparability G / N_1(l). Native
bridge: NOT_DERIVED. No milestone.

Primary objective: certify on bounded universes the solution-space dimensions of the read-map condition systems of
Proposition 27.2, Theorem 27.3 and Proposition 27.4 (general linear reads, one unknown matrix per carrier class); the depth
horizon and its sharpness (Theorem 27.3(iii), Proposition 27.4(a)); the ledger identities of Lemma 27.0; the kernel
description of Lemma 27.1 with its witness; the carrier-independent before/after values of Theorem 27.3; the correlated-pair
construction of Proposition 27.4(b); the witness of Proposition 27.4(c); and the κ id climb events. Finite checks are
bounded evidence, not proofs; the general statements rest on the written proofs.

## 2. Objects and enumeration domain

Carrier: finite rooted tree W (root = Genesis 0) up to rooted isomorphism. Canonical string
`c(v) = "(" + concat(sorted(c(children))) + ")"`, children sorted as strings; universe digest = sha256 of the sorted
canonical strings joined by newlines. Universes U_N = all rooted trees with 1 to N vertices; U3, U7, U8. A leaf is a vertex
v ≠ 0 with no children. w ≤ v means w is an ancestor of v or v itself. Chain C_d = the path 0 → 1 → … → d. Cherry K_d
(d ≥ 1) = C_d plus one more leaf d + 1 with parent d − 1 (d + 2 vertices).

Read maps. Unknowns: one matrix M_W[v][z] = F̂_W(δ_z)_v per carrier class (Σ |W|² unknowns), carried to every labelled
representative by a rooted isomorphism. Condition rows (each program builds its own; empty rows dropped):
- PN: every carrier W, leaf l with parent p, basis grade δ_z, retained v: F̂_Y(P δ_z)_v = (P F̂_W(δ_z))_v, where
  Y = W ∖ {l}, P δ_z = δ_z for z ≠ l, P δ_l = δ_p, and P adds the l-entry of a read vector to its p-entry.
- S_L: every carrier W, leaf l, z ≠ l: M_W[l][z] = 0.
- W2_1: every carrier X' and leaf l of X', X = X' ∖ {l}, z ∈ X, v ∈ X': M_{X'}[v][z] = M_X[v][z] if v ≠ l, and 0 if v = l.
- C_recv: every carrier, every leaf a: M_W[par(a)][a] = 0.
- CL_D (blindness half of one chain climb from depth D, D ≥ 1): for d = 1, …, D, M_{C_d}[d − 1][d] = 0 (D rows).
- BU_D (the same climb with each step's leaf on a non-chain carrier where the universe allows it): for d = 1, …, D, the row
  M_{K_d}[d − 1][d + 1] = 0 if d + 2 ≤ N, and the CL row M_{C_d}[d − 1][d] = 0 otherwise.
Acquisition (κ ≠ 0) is an open condition, not a linear row; it is certified by the family member with κ = 1 (section 3 (B))
and by the events (section 3 (F)).
Systems: PN; PN+S_L; PN+W2_1; PN+S_L+C_recv; PN+S_L+CL_D, PN+S_L+BU_D and PN+CL_D for every D = 1, …, N − 1; on U3, U7
and U8 (4 + 3(N − 1) systems: 10 / 22 / 25).
Depth-matrix reads: for a lower-triangular table ν, s_v = Σ_{w ≤ v, w ≤ z} ν(depth v, depth w) for x = δ_z, extended
linearly, and F̂(x)_v = s_v − Σ_{u ∈ ch(v)} s_u (Proposition 26.1).
Named tables: ν_off = I + E(2, 0) − E(2, 1); ν_gen(k, j) = (k + 1)(−1)^j / (j + 2) + [j = k]; T1 diagonal ν(k, k) = k² + 1;
T2 diagonal ν(k, k) = (−1)^k (k + 2)/(k + 1); horizon tables H_D (D = 1, …, N − 1): diagonal, ν(k, k) = −2 for k ≤ D and
ν(k, k) = −2 + 7(k − D) for k > D.

## 3. Preregistered values

Structural counts (disclosed counting script, section 6): U3 4 carriers, 4 leaves, Σ |W| = 9, 23 unknowns, 11 PN cases
(leaf, basis grade); U7 85 carriers, 252 leaves, Σ |W| = 526, 3,384 unknowns, 1,621 PN cases, 1,369 one-vertex extension
cases (carrier, leaf, z ∈ X) = S_L rows; U8 200 carriers, 686 leaves, Σ |W| = 1,446, 10,744 unknowns, 5,093 PN cases, 4,407
one-vertex extension cases = S_L rows.

Hand-derived (formulas from Proposition 27.2, Theorem 27.3, Proposition 27.4; N = 3 / 7 / 8):
- (A) Dimensions: PN N(N+1)/2 = 6 / 28 / 36; PN+S_L = PN+W2_1 = N = 3 / 7 / 8; PN+S_L+C_recv 1; PN+S_L+CL_D =
  PN+S_L+BU_D = N − D for every D = 1, …, N − 1; PN+CL_D = N(N+1)/2 − D for every D.
- (B) Explicit families (lower bounds; every member satisfies every row of its system exactly, independent):
  PN: E(k, j), j ≤ k; PN+S_L and PN+W2_1: E(k, k); PN+S_L+C_recv: I; PN+S_L+CL_D and PN+S_L+BU_D: Σ_{k ≤ D} E(k, k) and
  E(k, k) for D < k ≤ N − 1; PN+CL_D: E(k, j) − E(k, k) (1 ≤ k, j < k), Σ_{k ≤ D} E(k, k), and E(k, k) for D < k ≤ N − 1.
  The member Σ_{k ≤ D} E(k, k) (κ = 1) gains 1 at the receiver after each of the D chain steps.
- (C) Horizon (Theorem 27.3(iii), Proposition 27.4(a)), for every D = 1, …, N − 1 with H_D: (i) F̂_W = −2 id on every carrier
  of depth at most D (carriers per D: U7 7, 30, 60, 78, 84, 85; U8 8, 45, 113, 167, 192, 199, 200; U3 3, 4); (ii) at every
  vertex v of depth less than D on every carrier, F̂(δ_z)_v = −2 [v = z] for every z ((carrier, vertex) pairs per D: U7 85,
  248, 398, 484, 517, 525; U8 200, 595, 997, 1,267, 1,394, 1,436, 1,445; U3 4, 8); (iii) sharpness: at every vertex v of
  depth D with a child u, F̂(δ_u)_v = −7 ((carrier, vertex, child) cases per D: U7 150, 86, 33, 8, 1, 0; U8 402, 270, 127,
  42, 9, 1, 0; U3 1, 0).
- (D) Ledger and kernel, with ν_gen: Lemma 27.0 at every PN case (receiver p's read gains exactly the leaf's read, every
  other retained read unchanged, total read conserved): 11 / 1,621 / 5,093. Lemma 27.1 at every one-vertex extension case
  (7 / 1,369 / 4,407): the defect F̂_{X'}(I δ_z) − I F̂_X(δ_z) vanishes off {l, p}, its p-entry is minus its l-entry, its
  l-entry equals F̂_{X'}(I δ_z)_l (the (E0) value), and P of the defect is 0. With T1 the defect is 0 in every case.
  Diagnostic (not predicted, must agree): the number of cases with nonzero defect for ν_gen and for ν_off.
- (E) Before/after (Theorem 27.3, any carrier) for T1 and T2 at every leaf l of depth d with receiver p (4 / 252 / 686
  leaves): F̂(e_l)_p = ν(d−1, d−1) − ν(d, d), F̂(e_l)_l = ν(d, d), and F̂_Y(P e_l)_p = ν(d−1, d−1). Correlated pair
  (Proposition 27.4(b)) with T1 and T2 (every diagonal entry nonzero, so no case is skipped) at every leaf:
  r = −(ν(d−1, d−1) − ν(d, d))/ν(d−1, d−1), F̂_W(e_l + r e_p)_p = 0 and F̂_Y(P(e_l + r e_p))_p = ν(d, d).
- (F) Witness ν_off (Proposition 27.4(c)): PN at every PN case; every CL_D row for D = 1, …, N − 1 holds; S_L rows violated:
  1 / 227 / 660. κ id events (κ ∈ {1, −3, 1/2}, every labelled leaf l, p = par(l), g ∈ {1, −2, 5/3}; pair x and
  x + g δ_l with background x_v = (−1)^v (v + 2)/(1 + (v mod 3)) for v ≠ l in each program's own labels, x_l = 0):
  36 / 2,268 / 6,174 cases, PN for both members, Σ x conserved, receiver blind before, contrast exactly κ g after.

Hand-written instances (vertex values listed as [v = 0, 1, ...]; parent arrays with par(0) = None):
- Y1 ν_off, X = {0} ⊂ X' = chain [None, 0, 1]: F̂_{X'}(I δ_0) = ["1", "-1", "1"]; defect ["0", "-1", "1"].
- Y2 U3 dimensions: PN 6; PN+S_L 3; PN+W2_1 3; PN+S_L+C_recv 1; PN+S_L+CL_1 2; PN+S_L+CL_2 1; PN+S_L+BU_1 2;
  PN+S_L+BU_2 1; PN+CL_1 5; PN+CL_2 4.
- Y3 H_1 with κ written as 1 instead (ν(0,0) = ν(1,1) = 1, ν(2,2) = 8), chain [None, 0, 1], x = δ_2: ["0", "-7", "8"].
- Y4 T1 (1, 2, 5), chain [None, 0, 1], leaf 2, p = 1: r = "3/2", before "0", after "5".
- Y5 T1, carrier [None, 0, 1, 1] (0 → 1 → {2, 3}), leaf 3, p = 1: before F̂(e_3)_1 = "-3", after F̂_Y(P e_3)_1 = "2".

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 ν_off satisfies every S_L row on U7 or U8; R2 dim(PN+CL_{N−1}) = 1 on U7 or U8 (a climb without leaf-locality forces κ
id); R3 dim(PN+S_L+CL_D) = 1 for some D < N − 1 on U7 or U8 (no horizon); R4 some sharpness case of (C)(iii) reads 0 (H_D is
κ id one level below the horizon); R5 dim(PN+W2_1) = dim(PN) (the ledger alone forces the zero-extension square); R6 the
ν_gen defect vanishes at every one-vertex extension case on U7 or U8; R7 the table I + E(1, 0) satisfies every PN+S_L row on
U7 or U8; R8 some case of (D), (E) or (F) fails.
Diagnostics (not predicted; must agree between programs): the nonzero-defect counts of (D); the number of nonzero rows of
each condition type.
Comparator tamper controls (missing, duplicated and substituted records, wrong values and dimensions, false provenance,
wrong frozen bytes, role confusion, hidden violations, a flipped control, an extra key, a duplicated JSON key, an altered
diagnostic) must all be DETECTED.

## 5. Programs and resource rules

Producer: pure-Python exact Fractions; parent-array enumeration with AHU codes; rows in vertex coordinates; dimensions by
exact sparse Gauss-Jordan over Q (nullity = unknowns − exact rank; the PN echelon basis is computed once and extended per
system); depth-matrix reads by the vertex form F̂_v = s_v − Σ s_u with s from (26.1) in cone coordinates. Checker (does not
import the producer): trees grown by leaf attachment with nested-tuple canonical forms and BFS relabelling; isomorphisms by
canonical DFS orders; dimensions certified by a sparse mod-p rank (upper bound on the nullity) and the explicit rational
families of (B) checked exactly against every row with a mod-p rank of the family (lower bound); depth-matrix reads by
summing ν over common ancestors of v and z, vertex value by subtracting children. GREEN requires both programs to equal
every preregistered value, equal identity digests, equal diagnostics, zero violations, all controls REJECTED and all tamper
controls DETECTED. Pinned: Python 3.12, numpy 2.3.5, sympy 1.14.0, mpmath 1.3.0. Gemini: gemini-3.1-pro-preview, read
timeout 1,500 s. Stopping rule: one verify run on push, one dispatch with review=true; a transport failure without a verdict
may be re-run once at the same SHA and both attempts are recorded; a RED is preserved and reported, not re-run until it
disappears.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the draft-21 scratch `/tmp/rid28/chk27.py` with
`/tmp/rid28/base.py` and `/tmp/rid28/common.py` (sha256 `51ba381b…` / `77af574b…` / `1aed4c80…`; section 27's scratch
paragraph): the U5, U6 and U7 dimensions of PN, PN+S_L, PN+W2_1, PN+S_L+C_recv, PN+S_L+CL_D, PN+S_L+(bushy climb) and
PN+CL_D; the explicit families; the horizon and sharpness on U5-U7 for random κ; ν_off's 227 S_L violations on U7 and the
Lemma 27.1 witness values (Y1); Lemma 27.0, Lemma 27.1, the climb equivalences, the before/after values and the correlated
pair with random tables on U7. Structural counts above (including the horizon counts of (C), the one-vertex extension
counts and ν_off's S_L violations 1 / 227 / 660) come from `/tmp/rid29/count.py` (sha256
`c9221363423414c14b61871d4764fc732dbc1808acaa874a457215c872e6b6cd`, not committed; it imports the d20 producer's
enumeration helpers). Not computed before this file was committed: every U8 dimension; U3 dimensions; the named tables
ν_gen, T1, T2, H_D in any check; the deterministic event backgrounds; R6 and R7; the nonzero-defect diagnostics. The GitHub
Actions run is the preregistered execution.
