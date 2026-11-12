# receiver_identification d20 freeze: scope and preregistration (section 26, every vertex is a possible receiver)

Author: proteinfolding-grokbot. Parent: research branch head `3f212074ecb4c38dbedbf65738bcd7e2d7f6f04c` (2026-10-19 ET).
Frozen document:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 20 with its same-run
  addendum (commit `3f212074`), sha256 `2e10cfddb22129177e304e7a4456055d69769f42c36be811277c856cbd32883c`.
No separate source file: the inherited inputs of section 26 (FCV P1 in cone coordinates, Proposition 22.3; the FCV P2 zero
extension; Theorem 24.3(a); (25.1)) are stated in RESULT.md sections 17-25, which are frozen cited inputs.

## 1. Scope

Under review: section 26 of RESULT.md in full (Where this sits, Setting, the conditions (PN), (S), (S_leaf), (W2_F),
(C_climb), (C_recv), (Z), (G⁺), (CN_F), Proposition 26.1, Proposition 26.2(a)-(e), Theorem 26.3(a)-(f), Proposition
26.4(a)-(d), Control 26.5(a)-(c), the Reading paragraphs, "Earned and assumed", "Novelty, stated plainly", the scratch
disclosure, Next) and the draft-20 header item that summarises it. Sections 0-25 and [D16] are frozen cited inputs (Gemini
ACCEPTED in earlier freezes). Assumed and not under test as derived: linear, isomorphism-invariant read maps defined on every
finite carrier; (PN); (Z), or (S) (equivalently (W2_F)) with one of (C_climb), (C_recv), (G⁺); the P1 step (forced under CN,
CN assumed); for realization by v16.22's field, condition C, a response with every a_k ≠ 0, section 24's rule and the
Genesis total; occurrence (existential); availability (A0)-(A3') and (U); the declared pair; preparability G / N_1(l).
Native bridge: NOT_DERIVED. No milestone.

Primary objective: certify on bounded universes the solution-space dimensions of the read-map condition systems of
Propositions 26.1-26.2, Theorem 26.3 and Control 26.5 (general linear reads, one unknown matrix per carrier class), with the
finite-universe artifacts of Control 26.5(c); the identity of v16.22's field reads with the diagonal depth matrix
(Proposition 26.2, realization); the (Z) truth table of the field family (Theorem 26.3, last sentence); the witnesses of
Proposition 26.4 and Control 26.5(a); and the event behaviour of κ id. Finite checks are bounded evidence, not proofs; the
general statements rest on the written proofs.

## 2. Objects and enumeration domain

Carrier: finite rooted tree W (root = Genesis 0) up to rooted isomorphism. Canonical string
`c(v) = "(" + concat(sorted(c(children))) + ")"`, children sorted as strings; universe digest = sha256 of the sorted
canonical strings joined by newlines. Universes U_N = all rooted trees with 1 to N vertices; U3, U7, U8. A leaf is a
vertex v ≠ 0 with no children. w ≤ v means w is an ancestor of v or v itself. Cone X_a (a ≠ 0) = a and its descendants,
re-rooted at a. Cone totals c_v(x) = Σ_{t ∈ X_v} x_t, c_0 = Σ x.

Read maps. Unknowns: one matrix M_W[v][z] = F̂_W(δ_z)_v per carrier class (Σ |W|² unknowns), carried to every labelled
representative by a rooted isomorphism. Condition rows (each program builds its own):
- PN: every carrier W, leaf l with parent p, basis grade δ_z, retained v: F̂_Y(P δ_z)_v = (P F̂_W(δ_z))_v, where
  Y = W ∖ {l}, P δ_z = δ_z for z ≠ l, P δ_l = δ_p, and P adds the l-entry of a read vector to its p-entry.
- Z: every leaf a, every v ≠ a: M_W[v][a] = 0. C_recv: M_W[par(a)][a] = 0. C_climb: M_W[v][a] = 0 for every strict
  ancestor v of the leaf a.
- S: M_W[v][z] = 0 whenever v ≰ z. S_leaf: the same for leaves z only.
- CN_F: every nonroot a, z ∈ X_a, v ∈ W: M_W[v][z] = M_{X_a}[v][z] if v ∈ X_a, and 0 otherwise.
- G⁺: every W with at most N − 1 vertices, W⁺ = W below a new Genesis, z ∈ W, every v' ∈ W⁺:
  M_{W⁺}[v'][z] = M_W[v'][z] if v' ∈ W, and 0 at the new Genesis.
- W2_F: every proper prefix-closed X ⊊ W (containing 0), z ∈ X, v ∈ W: M_W[v][z] = M_X[v][z] if v ∈ X, and 0 otherwise.
Systems: PN; PN+Z; PN+CN_F; PN+G⁺; PN+C_recv; PN+C_climb; PN+S; PN+S_leaf; PN+S+C_climb; PN+S+C_recv; PN+S+G⁺;
PN+W2_F; PN+W2_F+C_recv. All 13 on U7; the first 11 on U8; PN, PN+Z, PN+CN_F on U3.
Depth-matrix reads: for a lower-triangular table ν, s_v = Σ_{w ≤ v, w ≤ z} ν(depth v, depth w) for x = δ_z and
F̂(δ_z)_v = s_v − Σ_{u ∈ ch(v)} s_u (Proposition 26.1).

Field reads (as in the d19 freeze): response tables unit a ≡ 1, three a ≡ 3, depth a_k = k, alt a_k = 1 (k odd), −2 (k
even); x° = x − (Σ x) δ_0; φ = grounded weighted-Laplacian potential (conductance 1/a_{depth v} on edge (par v, v), φ_0 = 0);
y_v = φ_v − φ_{par v}; f_v = −m_k y_v + m_{k+1} Σ_{u ∈ ch(v)} y_u (v ≠ 0, k = depth v); f_0 = m_1 Σ_{u ∈ ch(0)} y_u + θ Σ x.
Families G1 (unit, m ≡ 1), G2 (three, m ≡ 1), G3 (depth, m_k = 1/k), G4 (alt, m_k = 1/alt_k), G5 (depth, m ≡ 1), G6 (alt,
m ≡ 1); θ ∈ {−1, −3, 0, 2}; 24 settings. Composite μ_k = m_k a_k.
Witnesses: Genesis dump F̂_0 = Σ x, F̂_v = 0 otherwise; the λ = 0 field read (G1, θ = 0); the off-diagonal table
ν_off = I + E(2,0) − E(2,1) (ν(k, k) = 1 for all k).
Events: κ id with κ ∈ {1, −3, 1/2}; every labelled leaf l of every carrier, p = par(l), g ∈ {1, −2, 5/3}; pair x and
x + g δ_l with background x_v = (−1)^v (v + 2)/(1 + (v mod 3)) for v ≠ l in each program's own labels, x_l = 0.

## 3. Preregistered values

Structural counts (disclosed counting script, section 6): U3 4 carriers, 4 leaves, Σ |W| = 9, Σ |W|² = 23; U7 85
carriers, 252 leaves (69 children of Genesis), Σ |W| = 526, Σ |W|² = 3,384 unknowns, 1,621 PN cases (leaf, basis grade);
U8 200 carriers, 686 leaves (154), Σ |W| = 1,446, 10,744 unknowns, 5,093 PN cases.

Hand-derived (N = 7 / 8; formulas from Propositions 26.1-26.2, Theorem 26.3, Control 26.5 and the finite-universe count
below):
- (A) Dimensions: PN N(N+1)/2 = 28 / 36; PN+Z N = 7 / 8; PN+CN_F 2 / 2; PN+G⁺ N = 7 / 8; PN+C_recv = PN+C_climb
  N(N+1)/2 − (2N − 3) = 17 / 23; PN+S N = 7 / 8; PN+S_leaf 2N − 1 = 13 / 15; PN+S+C_climb 1 / 1; PN+S+C_recv 1 / 1;
  PN+S+G⁺ 1 / 1; PN+W2_F 7 (U7); PN+W2_F+C_recv 1 (U7). U3: PN 6, PN+Z 3, PN+CN_F 2. Count for C_recv/C_climb: the
  constraints are A(d−1, d−1) = A(d, d) for d = 1, …, N − 1 and A(d, d − 1) = 0 for d ≤ N − 2 (A(k, m) = Σ_{j ≤ m} ν(k, j)),
  2N − 3 independent rows; for S_leaf the rows A(k, m) = 0 (m < k ≤ N − 2) leave the diagonal and the N − 1 entries ν(N−1, j).
- (B) Explicit families (lower bounds; every member satisfies every row of its system exactly, and they are independent):
  PN: the N(N+1)/2 elementary tables E(k, j); PN+Z: I and E(N−1, j) − E(N−1, N−1), j < N − 1; PN+CN_F: I and
  E(N−1, 0) − E(N−1, 1); PN+G⁺: the N tables of Control 26.5(b) (free ν(0,0) and ν(r,1), r ≥ 1; ν(k, j) = ν(k − j + 1, 1)
  for j ≥ 1, ν(k, 0) = ν(k − 1, 0) − ν(k, 1)); PN+C_recv and PN+C_climb: a basis of the small ν-system above; PN+S and
  PN+W2_F: E(k, k); PN+S_leaf: E(k, k) and E(N−1, j), j < N − 1; the systems with dimension 1: I. Every PN+Z family member
  is κ id on every carrier with at most N − 1 vertices.
- (C) Field identity: in all 24 settings, field reads equal the depth-matrix reads with ν diagonal, ν(k, k) = −m_k a_k
  (k ≥ 1), ν(0, 0) = θ, at every (carrier, basis grade) (526 / 1,446 cases per setting), and PN holds at every PN case
  (1,621 / 5,093).
- (D) (Z) truth table of the field family, as the number of leaves a at which F̂(δ_a)_v = 0 for every v ≠ a (L = 252 / 686
  leaves, GL = 69 / 154 children of Genesis): G1, G3, G4 at θ = −1: L; G2 at θ = −3: L; G5, G6 at θ = −1: GL; every other
  setting: 0. (Diagonal ν: the strict ancestor v of a at depth k reads ν(k, k) − ν(k+1, k+1) = μ_{k+1} − μ_k for k ≥ 1 and
  θ + μ_1 at Genesis; non-ancestors read 0.)
- (E) Witnesses: Genesis dump and the λ = 0 field read satisfy PN at every PN case and fail (Z) at every leaf (L). ν_off
  satisfies PN at every PN case and C_climb at every leaf, fails (S); its count of leaves with a nonzero non-ancestor read is
  88 on U7 (known, section 6) and a diagnostic on U8.
- (F) Events: at every (κ, leaf, g) (2,268 / 6,174 cases) PN holds for both members, Σ x is conserved, the receiver p (Genesis
  included) is blind before (equal F̂_p) and separated by exactly κ g after.

Hand-written instances (vertex values listed as [v = 0, 1, ...]; parent arrays with par(0) = None):
- Z1 ν_off on [None, 0, 1, 0] (0 → {1 → 2, 3}), x = δ_3: ["0", "-1", "1", "1"].
- Z2 U3 dimensions: PN 6, PN+Z 3, PN+CN_F 2.
- Z3 on [None, 0], x = δ_1: Genesis dump ["1", "0"]; λ = 0 field read (G1) ["1", "-1"].
- Z4 κ id, κ = 1, chain [None, 0], l = 1, g = 1, background 0: receiver (Genesis) read before ["0", "0"] (both members),
  contrast after "1".
- Z5 G5, θ = −1, chain [None, 0, 1], x = δ_2: ["0", "1", "-2"].

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 the Genesis dump satisfies (Z) at some leaf; R2 the λ = 0 field read satisfies (Z) at some leaf; R3 ν_off satisfies (S)
on every carrier; R4 dim(PN+C_climb) = 1 on U7 or U8 (climb blindness alone forces κ id); R5 dim(PN+G⁺) = 1 on U7 or U8; R6
the table I + E(1, 0) satisfies every PN+Z row; R7 a field setting other than the four of (D) satisfies (Z) at every leaf; R8
some event case violates PN, conservation, blindness before or the κ g contrast after; R9 some PN+Z family member differs from
κ id on a carrier with at most N − 1 vertices.
Diagnostics (not predicted; must agree between programs): ν_off's non-ancestor-read leaf count on U8; the number of nonzero
rows of each condition type.
Comparator tamper controls (missing, duplicated and substituted records, wrong values and dimensions, false provenance,
wrong frozen bytes, role confusion, hidden violations, a flipped control, an extra key, a duplicated JSON key, an altered
diagnostic) must all be DETECTED.

## 5. Programs and resource rules

Producer: pure-Python exact Fractions; parent-array enumeration with AHU codes; rows in vertex coordinates; dimensions by
exact sparse Gauss-Jordan over Q (nullity = unknowns − exact rank); field by exact Gauss-Jordan solve of the grounded weighted
Laplacian; depth-matrix reads by the vertex form F̂_v = s_v − Σ s_u with s from (26.1). Checker (does not import the
producer): trees grown by leaf attachment with nested-tuple canonical forms and BFS relabelling; isomorphisms by canonical DFS
orders; dimensions certified by a sparse mod-p rank (upper bound on the nullity) and the explicit rational families of (B)
checked exactly against every row with a mod-p rank of the family (lower bound); depth-matrix reads in cone coordinates
(s_v by summing ν over common ancestors of v and z, vertex value by subtracting children); field by path sums of
a_depth · cone totals, verified against L φ = x° by neighbour sums; reads in incident-edge coordinates. GREEN requires both
programs to equal every preregistered value, equal identity digests, equal diagnostics, zero violations, all controls
REJECTED and all tamper controls DETECTED. Pinned: Python 3.12, numpy 2.3.5, sympy 1.14.0, mpmath 1.3.0. Gemini:
gemini-3.1-pro-preview, read timeout 1,500 s. Stopping rule: one verify run on push, one dispatch with review=true; a
transport failure without a verdict may be re-run once at the same SHA and both attempts are recorded; a RED is preserved
and reported, not re-run until it disappears.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the draft-20 scratch `/tmp/rid26/chk26.py` with
`/tmp/rid26/base.py` (sha256 `f243b1483eb34d513eb52f9ba4ad535a009f959139b1f20a065bff62d6b4ebbd` /
`77af574b023bcffbe34971f1c9699275ac578c4b20f0ffcc84216eca6e4a8211`; section 26's scratch paragraph): the U5, U6 and U7
dimensions of PN, PN+Z, PN+CN_F, PN+G⁺, PN+C_recv, PN+C_climb, PN+S, PN+S_leaf, PN+S+C_climb, PN+S+G⁺, PN+W2_F,
PN+W2_F+C_recv; the field = diagonal identity on U7 for θ ∈ {−1, 2}; the (Z) holds/fails pattern of the six families on U7
(holding or not at all leaves, not the per-setting leaf counts); the witnesses on U7 including ν_off's 88 of 252 and the
hand value of Z1; κ id events on U7 with random backgrounds and g ∈ {1, −2}. Structural counts above come from
`/tmp/rid27/count.py` (sha256 `c2689540813ea4c2ed0717e5903c5bf83db16b3a2be1a7fcc547a09fbbd3fabf`, not committed; carriers,
leaves, Genesis leaves, Σ |W|, Σ |W|², PN cases only). Not computed before this file was committed: every U8 value; U3;
PN+S+C_recv; the per-setting (Z) leaf counts of (D) (in particular GL for G5 and G6 at θ = −1); θ ∈ {−3, 0} in the field
identity; κ = 1/2 with g = 5/3 and the deterministic backgrounds; R6. The GitHub Actions run is the preregistered execution.
