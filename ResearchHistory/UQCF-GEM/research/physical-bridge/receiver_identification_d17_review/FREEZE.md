# receiver_identification d17 freeze: scope and preregistration (section 23, field-to-state association)

Author: proteinfolding-grokbot. Parent: research branch head `f3668faf3e4b7be8ba6bb0ffa46f4f63de5ff349` (2026-10-19 ET).
Frozen documents:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 17 (commit `f3668faf`),
  sha256 `4f55e562a8dddb4ed565128104637294b15836f0a3f226afb854ba0c4cce05be`.
- `SOURCE.md` = the exact bytes of `ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/PROOFS.md`, sha256
  `c5a6a1f2f79ff08481ea4a766a7ec257fd33cc3ced4f821335047b97306decb8`. Inherited source context (W_W typing, T1-T6), not under review.
- `CORRESPONDENCE.md` = the exact bytes of `record_consumer_trace/NATIVE_STATE_RECORD_INTERFACE.md` (proteinfolding-gpt,
  `5a0827cf`), sha256 `1c4534458fdff2d8f5c1eeb264f9eab60e70d9af93d4d9e89297f2c397dde9f3`. The open interface section 23 addresses.

## 1. Scope

Under review: section 23 of RESULT.md in full (Where this sits, Setting, Lemma 23.1, Theorem 23.2(a)-(e), Proposition
23.3(a)-(d), both Reading paragraphs, Control 23.4(a)-(d), "Earned and assumed", "Novelty, stated plainly", the scratch
disclosure, Next) and the draft-17 header items that summarise it. Sections 0-22 and [D16] are frozen cited inputs
(Gemini ACCEPTED in earlier freezes). Assumed and not under test as derived: (L) locality of access; (B) uniform initial
blindness; v16.22's condition C; (RS)/(CN); occurrence (existential); availability (A0)-(A3') and (U); the
Genesis-balanced convention; the declared pair; preparability G / N_1(l). Native bridge: NOT_DERIVED. No milestone.

Primary objective: certify on a bounded universe, for several diagonal depth tables, that the descendant-blind local
reads of the retained field form a one-dimensional space at every nonroot position, spanned by the own-grade read, and
are zero at Genesis (Theorem 23.2); that the P1 event leaves the grounded field unchanged on every retained vertex and
moves the one-location pair's contrast from 0 into the receiver's read (Proposition 23.3); and the dense-response control
(Control 23.4(c)). Finite checks are bounded evidence, not proofs; the general statements rest on the written proofs.

## 2. Objects and enumeration domain

Carrier: finite rooted tree W (root = Genesis 0) up to rooted isomorphism. Canonical string
`c(v) = "(" + concat(sorted(c(children))) + ")"`, children sorted as strings; universe digest = sha256 of the sorted
canonical strings joined by newlines. Universes U7 (1 to 7 vertices) and U8 (1 to 8 vertices).
Depth tables (all nonzero, so C holds, v16.22 T3): unit a ≡ 1; three a ≡ 3; depth a_k = k (T_depth); alt a_k = 1 for k
odd, −2 for k even. Grade x on W; Genesis-balanced part x° = x − (Σ x) δ_0; cone totals c_v = Σ_{z ∈ X_v} x_z.
Retained field φ = T_W x°, grounded by φ_0 = 0: φ_v − φ_{par(v)} = a_{depth(v)} c_v. Equivalently the weighted Laplacian
with conductance 1/a_{depth(v)} on edge (par(v), v), (Lφ)_v = Σ_{u~v} w_{uv}(φ_v − φ_u), satisfies (Lφ)_v = x_v at every
nonroot v.
Local read at p: a linear functional of (φ_q)_{q ∈ N[p]}, N[p] = {par(p)} ∪ {p} ∪ ch(p), vanishing on constants.
Descendant-blind: f(φ(e_z)) = 0 for every strict descendant z of p (e_z the unit grade at z). Normalisation: f(φ(e_p)) = 1.
Event: for every leaf l (every labelled leaf, not up to automorphism) the P1 pruning into p = par(l): W' = W ∖ {l},
x'_p = x_p + x_l, other coordinates unchanged. Pair: x and x + g e_l, g ∈ {1, −2, 5/3}; background in each program's own
labels x_v = (−1)^v (v + 2)/(1 + (v mod 3)) for v ≠ l, x_l = 0 for the first member.
Dense control J: edge values (Mc)_e = 2 c_e + Σ_f c_f (M = 2I + J over nonroot edges; labelling-invariant), grounded
potential by path sums; descendant-blind local reads at every nonroot position with at least one child, for carriers with
at least 4 vertices.

## 3. Preregistered values

Structural counts (disclosed counting script, section 6): U7 85 carriers, 441 nonroot positions, 189 nonroot positions
with children, 252 labelled leaves of which 69 are children of Genesis; U8 200 carriers, 1,246 positions, 560 with
children, 686 leaves, 154 children of Genesis.

Hand-derived (Lemma 23.1, Theorem 23.2): for each of the 4 tables, the local-read space at p has dimension deg(p)
(= |N[p]| − 1); the descendant-blind space has dimension exactly 1 at every nonroot position (441 / 1,246 per table) and
0 at Genesis on every carrier (85 / 200); the normalised blind read vanishes on φ(e_z) for every z ≠ p and has
coefficients −1/a_k on φ_{par(p)}, 1/a_k + n/a_{k+1} on φ_p, −1/a_{k+1} on each φ_u (k = depth(p), n = #children).
Event (Proposition 23.3(a) for the unit tables; for alt and depth the same identity is a hand-derived diagnostic, since
P1 preserves every retained cone total (Proposition 22.4(a)) and every retained depth): the grounded field after the event
equals the field before on every retained vertex for every table, leaf, g and pair member: U7 252 · 4 · 3 · 2 = 6,048
cases, U8 686 · 24 = 16,464, 0 violations. For nonroot p (183 / 532 leaves) the normalised read's pair contrast is 0
before and g after, and equals x_p before and x'_p after; for Genesis receivers (69 / 154) the two post-event fields are
identical, and the pre-event fields differ.
Dense control J: (dimension, own-grade) counts at the 189 / 560 positions are diagnostic (not predicted); predicted only
that some position is not own-grade (instance Z6).

Hand-written instances (unit table unless stated):
- Z1 chain 0 → 1 → 2, p = 1: normalised blind read coefficients on (φ_0, φ_1, φ_2) = ["-1", "2", "-1"]; with T_depth
  ["-1", "3/2", "-1/2"].
- Z2 carrier 0→1, 1→2, 1→3, p = 1: coefficients on (φ_0, φ_1, φ_2, φ_3) = ["-1", "3", "-1", "-1"].
- Z3 chain 0 → 1, p = 0: [local-read dimension, blind dimension] = [1, 0].
- Z4 chain 0 → 1 → 2, l = 2, x = 0 versus e_2: pre-event fields ["0","0","0"] and ["0","1","2"]; post-event ["0","0"] and
  ["0","1"]; read contrast before "0", after "1".
- Z5 chain 0 → 1, l = 1, x = 0 versus e_1: pre-event fields ["0","0"] and ["0","1"]; post-event ["0"] and ["0"].
- Z6 dense J, carrier 0→1, 1→2, 1→3, 0→4, p = 1: [blind dimension, own grade] = [1, false].

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 the grounded value φ_p is descendant-blind at every nonroot position; R2 the parent-edge read φ_p − φ_{par(p)} alone is
descendant-blind at every position with children; R3 under the dense response J every position with children has an
own-grade blind read; R4 some carrier has a nonzero blind read at Genesis; R5 the event changes the grounded field on
some retained vertex; R6 the blind read distinguishes the pair before the event at some nonroot receiver; R7 the
post-event fields of some Genesis-receiver pair differ; R8 some nonroot position has blind dimension other than 1.
Comparator tamper controls (missing, duplicated and substituted records, wrong values and dimensions, false provenance,
wrong frozen bytes, role confusion, hidden violations, a flipped control, an extra key, a duplicated JSON key) must all
be DETECTED.

## 5. Programs and resource rules

Producer: pure-Python exact Fractions; parent-array enumeration with AHU codes; field by exact Gauss-Jordan solve of the
grounded weighted Laplacian (no cone-total formula); blind reads as the exact nullspace over Q, in vertex coordinates on
N[p], of the constant row and the field responses of every strict descendant. Checker (does not import the producer):
trees grown by leaf attachment with nested-tuple canonical forms; field by path sums of a_depth · cone totals (subtree
sums), verified against L φ = x by neighbour sums; blind reads in incident-edge coordinates: the dimension is certified
by a mod-p rank of the descendant rows (upper bound) and the explicit own-grade read (lower bound) checked against every
row; Genesis by mod-p rank = full. GREEN requires both programs to equal every preregistered value, equal identity
digests, zero violations, all controls REJECTED and all tamper controls DETECTED. Pinned: Python 3.12, numpy 2.3.5,
sympy 1.14.0, mpmath 1.3.0. Stopping rule: one verify run on push, one dispatch with review=true; a RED is preserved and
reported, not re-run until it disappears.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the draft-17 scratch `/tmp/rid20/chk23.py`
(sha256 `8b3f3ce9…`; section 23's scratch paragraph: tables unit, 3 and T_depth on carriers up to 7 vertices, random
backgrounds, the unit-table event, and a random dense response with counts 87 / 97 / 4 on 188 positions). Structural
counts above come from `/tmp/rid21/count.py` (sha256 `386f2f7e9a614e3e23364316975d6add41533538b4213321fc25a541ede676b8`,
not committed; carrier, position, leaf counts only). The alt table, U8, the deterministic backgrounds, the event under
non-unit tables and the J control were not computed before this file was committed. The GitHub Actions run is the
preregistered execution.
