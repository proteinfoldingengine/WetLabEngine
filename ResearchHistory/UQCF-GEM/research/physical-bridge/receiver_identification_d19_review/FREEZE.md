# receiver_identification d19 freeze: scope and preregistration (section 25, the Genesis datum is forced)

Author: proteinfolding-grokbot. Parent: research branch head `8fb06970b802f3a1c011124b9bf5d351f02290d8` (2026-10-19 ET).
Frozen documents:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 19 (commit `8fb06970`),
  sha256 `9f307412224e835f4fccedccdabc408ab0e48c06b74ace9dbc3795a1b7a2c615`.
- `SOURCE.md` = the exact bytes of `ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/PROOFS.md`, sha256
  `c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8`. Inherited source context (W_W and S_W typing,
  edge coordinates b_W, d_W, condition C, T1-T6), not under review.

## 1. Scope

Under review: section 25 of RESULT.md in full (Where this sits, Setting and (25.1), the conditions (PN) for F̂ and (CN_F),
Proposition 25.1, Theorem 25.2(a)-(d), Corollary 25.3(i)-(iv), Proposition 25.4(a)-(c), the Reading paragraphs, "Earned and
assumed", "Novelty, stated plainly", the scratch disclosure, Next) and the draft-19 header item that summarises it.
Sections 0-24 and [D16] are frozen cited inputs (Gemini ACCEPTED in earlier freezes). Assumed and not under test as
derived: (CN_F), the CN root shift applied to reads; CN itself; (L) local field access; uniformity of the read rule; the
read ledger (K)/(PN)/(SC); condition C; for (B) via section 24, (RS) and (RS_F); that Genesis's read is a field read plus
some linear datum of the grade; occurrence (existential); availability (A0)-(A3') and (U); the declared pair;
preparability G / N_1(l). Native bridge: NOT_DERIVED. No milestone.

Primary objective: certify on a bounded universe the (CN_F) truth table of Theorem 25.2 for named (a, m) families and
total data θ Σ x; the elimination of an arbitrary Genesis datum under (CN_F) (Theorem 25.2(b), with the finite-universe
caveat that the root coefficients of the largest carriers are never tested by a cone); the elimination of the composite
depth table and θ (Theorem 25.2(a)-(b)); the λ ≡ 0 control (Theorem 25.2(d)); the P1-invariant functionals
(Proposition 25.1); and the event behaviour of Corollary 25.3(ii). Finite checks are bounded evidence, not proofs; the
general statements rest on the written proofs.

## 2. Objects and enumeration domain

Carrier: finite rooted tree W (root = Genesis 0) up to rooted isomorphism. Canonical string
`c(v) = "(" + concat(sorted(c(children))) + ")"`, children sorted as strings; universe digest = sha256 of the sorted
canonical strings joined by newlines. Universes U7 (1 to 7 vertices) and U8 (1 to 8 vertices); U3 (1 to 3 vertices) for
hand instances only.
Response tables (all nonzero, so C holds): unit a ≡ 1; three a ≡ 3; depth a_k = k (T_depth); alt a_k = 1 for k odd, −2 for
k even. Grade x ∈ F^W (not necessarily balanced); x° = x − (Σ x) δ_0; cone totals c_v = Σ_{z ∈ X_v} x_z; field φ = T_W x°
grounded by φ_0 = 0, equivalently the grounded weighted Laplacian with conductance 1/a_{depth(v)} on edge (par(v), v);
edge values y_v = φ_v − φ_{par(v)}. Read rule: the depth-table rule of Theorem 24.2(iv), F_W = −b_W diag(m_depth) d_W,
i.e. f_v = −m_k y_v + m_{k+1} Σ_{u ∈ ch(v)} y_u (v ≠ 0, k = depth(v)) and f_0 = m_1 Σ_{u ∈ ch(0)} y_u.
Full read map (25.1): F̂_W(x) = F_W(T_W x°) + λ_W(x) δ_0.
Named (a, m) families: G1 (unit, m ≡ 1), G2 (three, m ≡ 1), G3 (depth, m_k = 1/k), G4 (alt, m_k = 1/alt_k), with
μ_k = m_k a_k constant (μ = 1, 3, 1, 1); G5 (depth, m ≡ 1, μ_k = k) and G6 (alt, m ≡ 1, μ = alt), with μ nonconstant on
every pair of consecutive depths.
Total data: λ_W = θ Σ x with θ ∈ {−1, −3, 0, 2} (so −μ is in the set for every G1-G4).
(CN_F) case: (carrier W, nonroot a, basis grade e_q of the cone X_a re-rooted at a, q ∈ X_a); the case holds iff
F̂_W(j_a e_q) = j_a F̂_{X_a}(e_q) at every vertex of W, with j_a zero extension of vertex values from X_a to W.
Arbitrary Genesis datum: one unknown coefficient λ_W[v] for every vertex v of every carrier representative; equations from
every (CN_F) case (components that do not involve λ are constant equations and enter as consistency rows).
Composite-table elimination: unknowns μ_1, …, μ_D (D = maximum depth) and θ, with a ≡ 1, m = μ and λ = θ Σ x; equations
from every (CN_F) case.
P1-invariance: unknowns as for the arbitrary datum; for every leaf l of every carrier and every basis grade e_z,
λ_Y(P e_z) = λ_W(e_z), with Y = W ∖ {l} identified with its canonical representative by a rooted isomorphism.
Event: for every labelled leaf l, the P1 pruning into p = par(l): Y = W ∖ {l}, x'_p = x_p + x_l. Pair: x and x + g e_l,
g ∈ {1, −2, 5/3}; background in each program's own labels x_v = (−1)^v (v + 2)/(1 + (v mod 3)) for v ≠ l, x_l = 0 for the
first member; λ = −μ Σ x for G1-G4.

## 3. Preregistered values

Structural counts (disclosed counting script, section 6): U7 85 carriers, 441 nonroot positions, 252 labelled leaves (69
children of Genesis), 899 (CN_F) cases (Σ over nonroot a of |X_a|), Σ |W| = 526 unknowns, 48 carriers with 7 vertices,
maximum depth 6, Σ |W|² = 3,384; U8 200 carriers, 1,246 positions, 686 leaves (154 children of Genesis), 2,788 cases,
1,446 unknowns, 115 carriers with 8 vertices, maximum depth 7, Σ |W|² = 10,744.

Hand-derived:
- (A) Truth table. G1, G3, G4 with θ = −1 and G2 with θ = −3: (CN_F) holds at every case (899 / 2,788). G1-G4 with any
  other θ in the set: holds at no case (0), because Genesis of W reads μ + θ ≠ 0 at every case. G5 and G6: holds at fewer
  than all cases for every θ (exact numbers are diagnostics).
- (B) Arbitrary datum under (CN_F), for G1 and for G3: the system is consistent; λ = −Σ x satisfies every row; the solution
  space has dimension 48 / 115, spanned by the root coefficients of the carriers with the maximum number of vertices; every
  other coefficient (478 / 1,331) is forced to −1. For G5 the system is inconsistent.
- (C) Composite-table elimination: solution space dimension 1, spanned by μ_1 = … = μ_D = 1, θ = −1.
- (D) λ ≡ 0 with G1-G4: (CN_F) fails at x = δ_a (q = a) for every (carrier, nonroot a) (441 / 1,246).
- (E) Events, G1-G4 with λ = −μ Σ x: (PN) for F̂ holds and Σ x is conserved at every (leaf, g, member) (1,512 / 4,116); the
  receiver p, Genesis included, is blind before (zero F̂_p contrast) and separated by exactly −μ g after at every (leaf, g)
  (756 / 2,058); F̂ = −μ id at every (carrier, vertex, basis grade e_z, z any vertex) (3,384 / 10,744).
- (F) P1-invariant functionals: solution space dimension 1, spanned by λ = Σ x.

Hand-written instances (G1 unless stated; vertex values listed as [v = 0, 1, ...]):
- Z1 chain 0 → 1, a = 1, q = a: θ = −1 gives F̂_W(j_a e_q) = ["0", "-1"] and j_a F̂_X(e_q) = ["0", "-1"]; θ = 0 gives
  ["1", "-1"] and ["0", "0"].
- Z2 chain 0 → 1 → 2, x = e_2: λ = −Σ x gives ["0", "0", "-1"]; λ ≡ 0 gives ["1", "0", "-1"].
- Z3 chain 0 → 1 → 2, G5, θ = −1, a = 1, q = 2: F̂_W(j_a e_q) = ["0", "1", "-2"], j_a F̂_X(e_q) = ["0", "0", "-1"].
- Z4 P1-invariant functionals on U3 (4 carriers, 9 unknowns): dimension 1.
- Z5 chain 0 → 1, λ = −Σ x, l = 1, x = 0 versus e_1: Genesis F̂ contrast before "0", after "-1".
- Z6 arbitrary-datum elimination on U3, G1: dimension 2.
- Z7 composite-table elimination on U3 (μ_1, μ_2, θ): dimension 1.

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 λ ≡ 0 satisfies (CN_F) at the apex basis δ_a for some (carrier, nonroot a) under some G1-G4; R2 G5 or G6 satisfies
(CN_F) at every case for some θ; R3 some G1-G4 with θ ≠ −μ satisfies (CN_F) at some case; R4 the arbitrary-datum solution
space for G1 or G3 has dimension other than the number of maximum-size carriers, or λ = −Σ x fails a row; R5 the G5
arbitrary-datum system is consistent; R6 the P1-invariant space has dimension other than 1 or omits Σ x; R7 the
composite-table space has dimension other than 1 or omits (1, …, 1, −1); R8 some G1-G4 event case violates (PN), blindness
before, the −μ g contrast after or conservation of Σ x.
Diagnostics (not predicted; must agree between programs): the number of (CN_F) cases holding for G5 and G6 at each θ.
Comparator tamper controls (missing, duplicated and substituted records, wrong values and dimensions, false provenance,
wrong frozen bytes, role confusion, hidden violations, a flipped control, an extra key, a duplicated JSON key) must all
be DETECTED.

## 5. Programs and resource rules

Producer: pure-Python exact Fractions; parent-array enumeration with AHU codes; field by exact Gauss-Jordan solve of the
grounded weighted Laplacian (no cone-total formula); reads as vertex-coordinate matrices on N[v]; cones re-rooted by
relabelling; eliminations as exact sparse Gauss-Jordan over Q with an augmented constant column. Checker (does not import
the producer): trees grown by leaf attachment with nested-tuple canonical forms and BFS relabelling; field by path sums of
a_depth · cone totals, verified against L φ = x° by neighbour sums; reads in incident-edge coordinates; dimensions
certified by a sparse mod-p rank (upper bound on the nullity) and explicit rational solutions checked exactly against
every row (lower bound); consistency by comparing coefficient and augmented mod-p ranks. GREEN requires both programs to
equal every preregistered value, equal identity digests, equal diagnostics, zero violations, all controls REJECTED and all
tamper controls DETECTED. Pinned: Python 3.12, numpy 2.3.5, sympy 1.14.0, mpmath 1.3.0. Gemini: gemini-3.1-pro-preview,
read timeout 1,500 s (the d18 attempt 1 timed out at 900 s on an ~82k-token prompt). Stopping rule: one verify run on push,
one dispatch with review=true; a transport failure without a verdict may be re-run once at the same SHA and both attempts
are recorded; a RED is preserved and reported, not re-run until it disappears.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the draft-19 scratch `/tmp/rid24/chk25.py` with
`/tmp/rid24/base.py` (sha256 `d16d0997…` / `77af574b…`; section 25's scratch paragraph: U7 only; (CN_F) for six families
with θ ∈ {−1, −3, 0, 2}; arbitrary-datum elimination for (1, 1) with 48 free directions; a composite-table elimination with
an extra unrealized μ_7 unknown; the λ ≡ 0 control; random-background events with two g values; P1-invariant functionals).
Structural counts above come from `/tmp/rid25/count.py` (sha256
`d1edfe13062b84317ead1f2b2974c3adf8c94c5ecdf7d3504640127af3470c3e`, not committed; carrier, position, leaf, case, unknown,
top-carrier and depth counts only). U8, the G3 and G5 arbitrary-datum systems, the composite elimination without the
unrealized top-depth unknown, the deterministic backgrounds, g = 5/3 and the G5/G6 diagnostic counts were not computed
before this file was committed. The GitHub Actions run is the preregistered execution.
