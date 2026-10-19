# receiver_identification d18 freeze: scope and preregistration (section 24, initial blindness from the read ledger)

Author: proteinfolding-grokbot. Parent: research branch head `b79c6a0c09a25f14f864323678dda2b3d02c71bf` (2026-10-19 ET).
Frozen documents:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 18 (commit `b79c6a0c`),
  sha256 `b13d2cd4c2b688cb40ca9d31845f3d1cdbdb6230e0e03596e7f623e3dbd38ae6`.
- `SOURCE.md` = the exact bytes of `ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/PROOFS.md`, sha256
  `c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8`. Inherited source context (W_W and S_W typing,
  edge coordinates b_W, d_W, condition C, T1-T6), not under review.

## 1. Scope

Under review: section 24 of RESULT.md in full (Where this sits, Setting and (24.1), the read-ledger conditions (K), (PN),
(SC), (RS_F), Lemma 24.1, Theorem 24.2, Theorem 24.3(a)-(e), Proposition 24.4(a)-(b), the Reading paragraphs, Control
24.5(a)-(d), "Earned and assumed", "Novelty, stated plainly", the scratch disclosure, Next) and the draft-18 header item
that summarises it. Sections 0-23 and [D16] are frozen cited inputs (Gemini ACCEPTED in earlier freezes). Assumed and not
under test as derived: (L) local field access; uniformity of the read rule; the read ledger in any of its forms (K), (PN),
(SC); the root shift for step, response and reads (CN), (RS), (RS_F); condition C; at Genesis, access to the total;
occurrence (existential); availability (A0)-(A3') and (U); the declared pair; preparability G / N_1(l). Native bridge:
NOT_DERIVED. No milestone.

Primary objective: certify on a bounded universe Lemma 24.1's dimension and edge-local structure on every carrier; the
uniform-parameter elimination of Theorem 24.2 ((PN), (SC), (K) each leave exactly one scalar per realized depth, of the
stated form) under three response tables; the composite, blind-position and own-grade counts of Theorem 24.3 for named
(a, m) families; (RS_F) on every cone; the event behaviour and the Genesis total witness of Proposition 24.4; and Control
24.5. Finite checks are bounded evidence, not proofs; the general statements rest on the written proofs.

## 2. Objects and enumeration domain

Carrier: finite rooted tree W (root = Genesis 0) up to rooted isomorphism. Canonical string
`c(v) = "(" + concat(sorted(c(children))) + ")"`, children sorted as strings; universe digest = sha256 of the sorted
canonical strings joined by newlines. Universes U7 (1 to 7 vertices) and U8 (1 to 8 vertices).
Response tables (all nonzero, so C holds): unit a ≡ 1; three a ≡ 3; depth a_k = k (T_depth); alt a_k = 1 for k odd, −2 for
k even. Grade x on W; x° = x − (Σ x) δ_0; cone totals c_v = Σ_{z ∈ X_v} x_z; field φ = T_W x° grounded by φ_0 = 0 with
φ_v − φ_{par(v)} = a_{depth(v)} c_v (equivalently the grounded weighted Laplacian with conductance 1/a_{depth(v)} on edge
(par(v), v)); edge values y_v = φ_v − φ_{par(v)}.
Uniform read rule (24.1) with parameters β(k, n) (nonroot v of depth k with n children), γ(k, n) (n ≥ 1) and γ_0(n)
(n ≥ 1), restricted to the parameters realized in the universe. Depth-table rule: β(k, ·) = m_k, γ(k, ·) = m_{k+1},
γ_0 = m_1, i.e. F_W = −b_W diag(m_depth) d_W.
Named (a, m) families: F1 (unit, 1), F2 (three, 1), F3 (depth, 1/k), F4 (alt, 1/alt), all with μ = m_k a_k constant
(μ = 1, 3, 1, 1); F5 (depth, 1), F6 (unit, k), F7 (alt, 1), with μ nonconstant on every pair of consecutive depths.
Basis inputs: x = e_z for every nonroot z (so x° = e_z − e_0). Event: for every labelled leaf l, the P1 pruning into
p = par(l): Y = W ∖ {l}, x'_p = x_p + x_l. Pair: x and x + g e_l, g ∈ {1, −2, 5/3}; background in each program's own labels
x_v = (−1)^v (v + 2)/(1 + (v mod 3)) for v ≠ l, x_l = 0 for the first member. Genesis total datum: f_0 = −μ x°_0 + θ Σ x with
θ ∈ {−μ, 0, 2} for F1-F4. (RS_F): for every nonroot a with at least one child, F_W(h_a ψ) = i_a F_{X_a}(ψ) for every
cone potential ψ = δ_q, q ∈ X_a, with X_a re-rooted at a, h_a extension by ψ(a) outside the cone, i_a zero extension; m
tables: m ≡ 1, m_k = k, m_k = 1/k, m = alt.
Lemma 24.1 system: on each carrier, unknown coefficients of every f_v on φ_q, q ∈ N[v]; constraints f_v(1) = 0 at every v
and Σ_v f_v(δ_q) = 0 for every q.

## 3. Preregistered values

Structural counts (disclosed counting script, section 6): U7 85 carriers, 441 nonroot positions, 189 nonroot positions
with children (68 of them at even depth), 252 labelled leaves (69 children of Genesis), 42 realized uniform parameters,
maximum depth 6, Σ |W|(|W| − 1) = 2,858; U8 200 carriers, 1,246 positions, 560 with children (217 at even depth), 686
leaves (154 children of Genesis), 56 parameters, maximum depth 7, Σ |W|(|W| − 1) = 9,298.

Hand-derived:
- Lemma 24.1: (K) solution dimension |W| − 1 on every carrier (85 / 200), every basis solution edge-local with opposite
  endpoint coefficients.
- Theorem 24.2: for each table unit, depth, alt, the parameter solution space of (PN), of (SC), of (K) and of all three
  together has dimension equal to the maximum depth (6 / 7), and each depth-table rule m = e_j (j = 1..D) satisfies every
  row (so the space is exactly the depth-table family).
- Theorem 24.3, per family F1-F7: (K) on every carrier (85 / 200); composite grade formula at every (carrier, vertex,
  basis input) (2,858 / 9,298); Genesis read = μ_1 Σ_{v ≠ 0} x_v on every carrier with at least two vertices (84 / 199);
  blind positions (read at p blind to every strict-descendant basis difference) and own-grade positions (f_p = −μ_k x_p):
  all positions (441 / 1,246) for F1-F4, exactly the leaves (252 / 686) for F5-F7.
- (RS_F) over the 189 / 560 cones: m ≡ 1 holds at all; m_k = k and m_k = 1/k hold at none; m = alt holds exactly at the
  cones of even depth (68 / 217).
- Event, per family F1-F7, every leaf, g and pair member: (PN) holds (U7 252 · 6 = 1,512, U8 686 · 6 = 4,116 cases).
  Nonroot receivers (183 / 532 leaves, × 3 g = 549 / 1,596): read contrast before = g(μ_{k+1} − μ_k) and after = −μ_k g
  (k = depth(p)); blind before at all 549 / 1,596 for F1-F4 and at none for F5-F7. Genesis receivers (69 / 154 leaves,
  × 3 g = 207 / 462) without the total: contrast before μ_1 g, after 0.
- Proposition 24.4, F1-F4: with the total, contrast before (μ + θ) g and after θ g at all 207 / 462 Genesis cases for each θ;
  Genesis blind before at all 207 / 462 for θ = −μ and at none for θ ∈ {0, 2}; (PN) at Genesis prunings holds for every θ
  (69 · 6 = 414 / 154 · 6 = 924 cases per θ); with θ = −μ, F(x) = −μ x at every (carrier, vertex, basis grade e_z,
  z any vertex) (Σ |W|² = 3,384 / 10,744).

Hand-written instances (m ≡ 1, unit table unless stated; reads listed as [f_0, f_1, ...]):
- Z1 chain 0 → 1 → 2, x = e_2: reads ["1", "0", "-1"]; x = e_1: ["1", "-1", "0"].
- Z2 chain 0 → 1 → 2, T_depth, x = e_2: m ≡ 1 gives ["1", "1", "-2"]; m_k = 1/k gives ["1", "0", "-1"].
- Z3 carrier 0→1, 1→2, 1→3: Lemma 24.1 (K) dimension 3.
- Z4 chain 0 → 1 → 2 → 3, m = alt: (RS_F) at a = 1 false, at a = 2 true.
- Z5 chain 0 → 1, l = 1, x = 0 versus e_1, total datum: θ = 0 gives [contrast before "1", after "0"]; θ = −1 gives
  ["0", "-1"].
- Z6 chain 0 → 1 → 2, child-count rule β(k, n) = 1 + n, γ = γ_0 = 1, x = e_1: Σ_v f_v = "-1".

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 the cone read (β = 1, γ = γ_0 = 0, unit table) satisfies (PN) at every leaf pruning; R2 the child-count rule β(k, n) =
1 + n, γ = γ_0 = 1 satisfies (K) on every carrier; R3 F5 (T_depth, m ≡ 1) is blind at every position with children;
R4 m_k = 1/k satisfies (RS_F) at every cone; R5 the (PN) parameter space has dimension larger than the maximum depth under
some table (a uniform rule outside the depth-table family satisfies (PN)); R6 Genesis is blind with θ = 0 for some
Genesis-receiver pair; R7 some named family violates (PN) at some leaf pruning; R8 some carrier has (K) dimension other
than |W| − 1 in the Lemma 24.1 system or a basis solution that is not edge-local with opposite endpoint coefficients.
Diagnostics (not predicted): the number of leaf prunings at which R1 fails and of carriers at which R2 fails.
Comparator tamper controls (missing, duplicated and substituted records, wrong values and dimensions, false provenance,
wrong frozen bytes, role confusion, hidden violations, a flipped control, an extra key, a duplicated JSON key) must all
be DETECTED.

## 5. Programs and resource rules

Producer: pure-Python exact Fractions; parent-array enumeration with AHU codes; field by exact Gauss-Jordan solve of the
grounded weighted Laplacian (no cone-total formula); reads evaluated in vertex coordinates on N[v]; parameter and Lemma
24.1 spaces as exact nullspaces over Q. Checker (does not import the producer): trees grown by leaf attachment with
nested-tuple canonical forms; field by path sums of a_depth · cone totals, verified against L φ = x by neighbour sums;
reads in incident-edge coordinates; dimensions certified by a mod-p rank (upper bound on the nullity) and explicit
rational solution families (m = e_j; the edge-weight reads of Lemma 24.1) checked exactly against every row (lower
bound). GREEN requires both programs to equal every preregistered value, equal identity digests, zero violations, all
controls REJECTED and all tamper controls DETECTED. Pinned: Python 3.12, numpy 2.3.5, sympy 1.14.0, mpmath 1.3.0.
Stopping rule: one verify run on push, one dispatch with review=true; a RED is preserved and reported, not re-run until it
disappears.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the draft-18 scratch `/tmp/rid22/chk24.py`
with `/tmp/rid22/base.py` (sha256 `6a912bdb…` / `77af574b…`; section 24's scratch paragraph: U7 only, tables unit and
T_depth for the parameter elimination, families (1,1), (3,1), (k,1/k), (k,1), (1,k), (RS_F) for m ≡ 1, k, 1/k with random
cone potentials, random-background events, the cone-read control). Structural counts above come from `/tmp/rid23/count.py`
(sha256 `0a596f3b2b9d20d9204b82a8a802948dd7a8b6e42f0af6ad62cd5bffc74a3142`, not committed; carrier, position, leaf,
parameter and depth counts only). U8, the alt table and families F4 and F7, (RS_F) for m = alt, the deterministic
backgrounds, θ = 2, the child-count control's (K) count and the Lemma 24.1 system were not computed before this file was
committed. The GitHub Actions run is the preregistered execution.
