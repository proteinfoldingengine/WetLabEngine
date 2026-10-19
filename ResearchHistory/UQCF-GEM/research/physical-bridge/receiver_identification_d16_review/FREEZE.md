# receiver_identification d16 freeze: scope and preregistration ([D16] and section 22)

Author: proteinfolding-grokbot. Parent: research branch head `d29c0000c68bafef15c8555e6b4455f39d430d9f` (2026-10-18 ET).
Frozen documents:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 16 (commit `3dd28b56`),
  sha256 `e1eaf4592be4f234c18eff86fbc831a194a87fc3955402ce39724d35ce98715d`.
- `SOURCE.md` = the exact bytes of `demos/v16.22-response-selection-closure/PROOFS.md` (last changed in `310ec851`), sha256
  `c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8`. Inherited source context (T1-T6), not under review.
- `CORRESPONDENCE.md` = the exact bytes of `receiver_identification_d15_review/GPT_E5_PLUS_QUALIFICATION.md` (proteinfolding-gpt,
  `e73eb613`), sha256 `ab8d79316aeb2ced8bf52ba3c07e79b9975f63f8a85b3502de1f5936d76603fb`. The correction adopted as [D16].

## 1. Scope

Under review: note [D16] wherever it appears in RESULT.md (draft 16 header item (i), the [D16] revision note, the [D16]
addendum to Theorem 21.2(c), the [D16] bracket in the section-21 novelty paragraph), and section 22 in full (Setting, the
assumed square (RS), Lemma 22.1, Theorem 22.2(a)-(c), Reading, Proposition 22.3, Proposition 22.4(a)-(c), Control
22.5(a)-(c), "Earned and assumed", "Novelty, stated plainly", the scratch disclosure). Sections 0-21 are cited inputs.
Assumed and not under test as derived: (RS) and (CN), one root-shift morphism type; the unit choice, (U) or INV;
occurrence (existential); ownership and availability (A0)-(A3'); the field-to-state association; preparability G.
Native bridge: NOT_DERIVED. No milestone is claimed.

Primary objective: certify on a bounded universe the exact dimensions of v16.22's comparison condition C and of C + (RS),
with unknown full edge-coordinate matrices and no diagonal ansatz (Theorem 22.2(a)-(b)); the T_depth witness (22.2(c));
the Green cone locality behind (RS) in vertex coordinates; Proposition 22.3 and the [D16] counterexample on a weight grid;
Proposition 22.4 on every leaf of every carrier. Diagnostic: random depth tables. Finite checks are bounded evidence, not
proofs; the general statements rest on the written proofs.

## 2. Objects and enumeration domain

A carrier is a finite rooted tree X (root = Genesis 0), up to rooted isomorphism. Canonical identity string:
`c(v) = "(" + concat(sorted(c(children))) + ")"`, children sorted as strings; universe digest = sha256 of the sorted
canonical strings joined by newlines. Universes U7 (carriers with 2 to 7 vertices) and U8 (2 to 8 vertices).
Edges: one per nonroot vertex v, e_v = (p(v), v); depth(e_v) = depth(v). Unknowns: every entry M_X[e, f] of every
carrier's edge-coordinate matrix (no diagonal ansatz). Conditions (exact, over Q):
- (C), v16.22 T2 in edge coordinates: for every nontrivial rooted automorphism π of X, M_X[π e, π f] = M_X[e, f]; for
  every proper prefix-closed Y ⊊ X with 0 ∈ Y and |Y| ≥ 2 (both diagrams Q M_X = M_Y Q and M_X J = J M_Y):
  M_X[e, f] = M_Y[e, f] when both edges are retained, M_X[e, f] = 0 when exactly one is retained.
- (RS), Lemma 22.1: for every nonroot a with |X_a| ≥ 2, X_a re-rooted at a: M_X J_a = J_a M_{X_a}, i.e. for every cone
  edge f: M_X[e, f] = M_{X_a}[e, f] for cone edges e and M_X[e, f] = 0 for every other edge e (including e_a).
Vertex-coordinate Green check: the unweighted Laplacian L = b d (positive, (Lφ)_v = Σ_{u~v}(φ_v − φ_u)); the unit
response φ = L^{-1}k (root-zero) of a balanced source k; potential difference across e_v is φ_v − φ_{p(v)}.
Weight grid (Proposition 22.3, [D16]): single-pruning steps on the chain 0 → 1 → … → K, leaf l = K, (E1)/(E3)/(E4)
form T(e_l) = Σ_{d=1}^{K} w_d e_{l−d}, w ∈ {−1, −1/2, 0, 1/2, 1, 3/2}^K, K = 1..4. (E2): Σ w = 1. (E5+): w_1 = 1.
(R): every retained ancestral cone total preserved (Σ_{j ≤ d} w_j = 1 for d = 1..K). (CN): the parent-cone square of
section 21 (w = e_1). Coordinate deletion: in coordinates (total, c_v) the step deletes c_l and fixes the rest.

## 3. Preregistered values

Structural counts (disclosed counting script, section 6): U7 84 carriers, 2,417 unknowns, 189 nonroot cones with at least
two vertices, 151 (carrier, leaf) classes up to automorphism; U8 199 carriers, 8,052 unknowns, 560 cones, 413 classes.
Grid: 1,554 vectors; E2 179; E5+ 259; E2 ∧ E5+ 32; R 4; CN 4; coordinate deletion 4; E2 ∧ E5+ with nonnegative weights 4;
E2 ∧ E5+ ∧ ¬R 28; mismatches of (R ⇔ coordinate deletion), (CN ⇔ R), (CN ⇒ E5+) all 0.

Dimensions, hand-derived (v16.22 T3 and Theorem 22.2): dim C = maximal depth = U7 6, U8 7; dim C + RS = 1 in both.
Explicit solution families: the depth indicators a = e_k (k = 1..K_max) solve C; a ≡ 1 solves C + RS; T_depth (a_k = k)
solves C and violates RS. Random depth tables (100 per program per universe, different generators and seeds, plus the
constant tables 1 and −2): RS holds iff the table is constant, 0 mismatches.
Green cone locality: for every cone (189 / 560) and a balanced cone source, unit-response differences on cone edges equal
the cone's own response and vanish on every other edge: 0 violations; L φ = k exactly on every carrier.
Proposition 22.4 on every (carrier, leaf) class (151 / 413): every retained cone total and the total unchanged by P1;
x_p = c_p − Σ_children c_u before and x_p' = x_p + x_l after; the one-location pair (x and x + g e_l, g ≠ 0) differs before
in exactly {total} ∪ {c_v : v nonroot ancestor of l or v = l} and after in exactly {total} ∪ {c_v : v retained nonroot
ancestor of l} with receiver difference 0 before and g after: 0 violations.

Hand-written instances:
- Z1 path 0 → v → w, cone source k = (0, −1, 1): [difference across (v, w) in X_v at unit, T_depth difference in X] = ["1", "2"].
- Z2 carrier 0→1, 1→2, 1→3, 0→4, cone X_1 source (k_1, k_2, k_3) = (−2, 1, 1): unit differences across edges
  [e_1, e_2, e_3, e_4] = ["0", "1", "1", "0"], cone's own [e_2, e_3] = ["1", "1"].
- Z3 [D16] signed step on chain 0 → 1 → 2 → 3, l = 3, T(e_3) = e_2 + e_1 − e_0: [E2, E5+, R, CN, coordinate deletion] =
  [true, true, false, false, false], and c_1(T e_3) = "2".
- Z4 carrier 0→1, 1→2, 1→3, l = 3, x = 0 versus x = e_3: [differing coordinates before, after, receiver difference
  before, after] = [["c1", "c3", "total"], ["c1", "total"], "0", "1"].
- Z5 Genesis dump on chain 0 → 1 → 2, l = 2, x = e_2: change of c_1 = "-1".

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 T_depth satisfies RS; R2 some nonconstant random depth table satisfies RS; R3 C alone forces dim 1; R4 Genesis dump is
coordinate deletion; R5 the [D16] signed step satisfies R; R6 the [D16] signed step satisfies CN; R7 depth-weighted
response (a_k = k) passes the Green cone locality on every cone; R8 Genesis dump keeps every retained cone total;
R9 E2 ∧ E5+ forces P1 without positivity. Comparator tamper controls (missing, duplicated and substituted records, wrong
values and dimensions, false provenance, wrong frozen bytes, role confusion, hidden violations, a flipped control, an extra
key, a duplicated JSON key) must all be DETECTED.

## 5. Programs and resource rules

Producer: pure-Python exact Fractions; parent-array enumeration with AHU codes; prefix subtrees by vertex masks; cones by
BFS; sparse Gauss-Jordan elimination over Q of the full C and C + RS systems; Green response by exact Fraction solve of
the root-reduced Laplacian. Checker (algorithmically independent): trees grown by leaf attachment with nested-tuple
canonical forms; prefix subtrees as closures under leaf deletion; each condition row has the form u − v = 0 or u = 0, so
each dimension is certified by equivalence classes (union-find; dimension = number of classes with no member forced to
0), cross-checked by a mod-p rank upper bound and by explicit rational solution families checked against every row;
Green response by subtree sums on the tree (no linear solve). GREEN requires both programs to equal every preregistered
value, equal identity digests, zero violations, all controls REJECTED and all tamper controls DETECTED. Pinned: Python
3.12, numpy 2.3.5, sympy 1.14.0, mpmath 1.3.0. Stopping rule: one verify run on push, one dispatch with review=true; a RED
is preserved and reported, not re-run until it disappears.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the draft-16 scratch `/tmp/rid18/chk22.py`
(U7 dimensions 6 and 1, the grid and Proposition 22.4 checks, section 22's scratch paragraph; its Green check used the
opposite Laplacian sign convention, which does not affect differences equal or zero). Structural and grid counts above
come from the counting script `/tmp/rid19/count.py` (sha256 `1fdeb66bbf7d7b593e45166a2fa6e3b140e472535f259b0514c1d429593d9bd6`,
not committed; it computes carrier, unknown, cone and leaf-class counts and the grid predicates as defined in section 2,
not dimensions). The U8 dimensions are hand-derived and were not computed before this file was committed. The GitHub
Actions run is the preregistered execution.
