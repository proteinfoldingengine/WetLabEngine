# receiver_identification d15 freeze: scope and preregistration (section 21)

Author: proteinfolding-grokbot. Parent: research branch head `5c7405bfce726c8f122445b8784cd34909b1c350` (2026-10-18 ET).
Frozen documents: `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 15
(commit `53748525`), sha256 `b32481cf40d83691176972eef1c1deb8caadb7f25c4febd352aadba487a9f40c`; `CORRESPONDENCE.md`
(verbatim source-scope paragraph, no verdicts), sha256 `2b2ba0083fc4a3dcc5caa0c98256916521f21882e1f5852d936f0065cb806a1a`.

## 1. Scope

Under review: section 21 of RESULT.md in full (Setting with (NI) and (CN); Proposition 21.1; Theorem 21.2(a)-(c);
Control 21.3(a)-(d); "Earned and assumed"; "Novelty"; the scratch disclosure). Sections 0-20 are cited inputs (the
(E1)-(E4) class and Theorem 16.1, Proposition 19.8, controls 20.5). Assumed and not under test as derived: (NI) as a
locality requirement, (CN) root-shift locality, occurrence (existential), ownership and availability (A0)-(A3'), (U), the
field-to-state association, preparability G. Native bridge: NOT_DERIVED. No milestone is claimed.

Primary objective: certify, on a bounded universe, the exact affine dimensions of the (E4)-weight solution sets of the
linear conditions of section 21, both uniqueness claims of Theorem 21.2, and the controls. Diagnostic: the random depth
table family. Finite checks are bounded evidence, not proofs; the general statements rest on the written proofs.

## 2. Objects and enumeration domain

A marked carrier is a finite rooted tree W (root = Genesis 0) with a marked non-root leaf l, taken up to marked rooted
isomorphism. Canonical identity string: `c(v) = "(" + ("*" if v = l) + concat(sorted(c(children))) + ")"`, children
sorted as strings; the record of a carrier is `c(0) + ":" + depth(l)`; the universe digest is sha256 of the sorted
records joined by newlines. Universes U7 (all marked carriers with 2 to 7 vertices) and U8 (2 to 8 vertices). Unknowns:
w_d(W, l), d = 1..depth(l), the (E4) weights of T(e_l) on the ancestor at distance d. Conditions (all exact over Q):
- (E2): Σ_d w_d(W,l) = 1 for every carrier.
- (NI): for every prefix-closed Y ⊊ W containing 0 and l, the commuting square T_W ∘ I = I ∘ T_Y at e_l, i.e.
  w_d(W,l) = w_d(Y,l) for every d.
- (CN): for every proper non-root ancestor a of l, the cone X_a re-rooted at a, square T_W ∘ j_a = j_a ∘ T_{X_a} at e_l,
  i.e. w_d(W,l) = w_d(X_a,l) for d ≤ depth_{X_a}(l) and w_d(W,l) = 0 beyond. (CN-parent): a = par(l) only. The trivial
  root cone a = 0 is excluded (it is the identity morphism and would add only tautologies).
Named rules (weight vectors by depth K): P1 e_1; Genesis dump e_K; grandparent e_min(2,K); split (1/2,1/2,0,..) for
K ≥ 2 and (1) for K = 1; annihilation 0.

## 3. Preregistered values

Structural counts (from the disclosed counting script, section 6): U7 151 carriers, 363 unknowns, by depth
[37, 50, 38, 19, 6, 1]; U8 413 carriers, 1085 unknowns, by depth [85, 124, 107, 63, 26, 7, 1].

Dimensions, hand-derived:
- E2: unknowns − carriers (one independent affine equation per carrier, on disjoint unknowns): U7 212, U8 672.
- E2+NI: Proposition 21.1, depth table: Σ_{k=1}^{K_max}(k − 1): U7 (K_max 6) 15, U8 (K_max 7) 21.
- CN, CN-parent (no E2): w(W,l) = c(X_par(l), l) e_1 with one free scalar per depth-1 marked carrier, and every depth-1
  marked carrier with n vertices is the parent cone of itself. Depth-1 marked carriers with n vertices correspond to
  rooted forests on n − 2 vertices, i.e. rooted trees on n − 1 vertices (OEIS A000081: 1, 1, 2, 4, 9, 20, 48): U7
  1+1+2+4+9+20 = 37, U8 37+48 = 85.
- NI+CN: one global scalar c (Control 21.3(b)): 1 in both.
- E2+CN, E2+CN-parent, E2+NI+CN-parent: 0, with the unique solution equal to P1 (Theorem 21.2(a)).
Rules [E2, NI, CN, CN-parent], same in U7 and U8: P1 [T, T, T, T]; Genesis dump, grandparent, split [T, T, F, F];
annihilation [F, T, T, T].
Random depth tables: 300 integer tables (entries in {−3..3}, normalized by (E2) on one coordinate; producer and checker
use different generators, seeds and normalizing coordinates): E2 300, NI 300, CN-parent 0, P1 0 in each universe
(CN-parent holds iff the table is P1; a random table equals P1 with probability at most 7^{-15}).

Hand-written instances:
- Y1 chain 0→1→2, leaf 2, Genesis dump: CN-parent residual [at parent, at Genesis] = ["-1", "1"].
- Y2 same chain, split: ["-1/2", "1/2"].
- Y3 cherry 0→1, 1→{2,3}, sibling rule e_2 ↦ e_3, as full matrices on R^W and on the cone of 1: [CN square holds,
  E2 holds, E4 holds] = [true, true, false].
- Y4 annihilation on the chain: [total after "0", CN square holds true, NI holds true].
- Y5 carrier 0→1→2, 0→3, leaf 2: [proper prefix subcarriers containing 0 and l, non-root proper ancestor cones] = [1, 1].

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 Genesis dump satisfies CN-parent; R2 grandparent satisfies CN-parent; R3 split satisfies CN-parent; R4 annihilation
satisfies E2; R5 the sibling rule satisfies E4; R6 (E2)+(NI) alone forces P1; R7 CN without (E2) forces P1; R8 P1 with the
weights of one depth-3 carrier substituted by the grandparent rule satisfies CN-parent. Comparator tamper controls:
missing, duplicated and substituted records, wrong values and counts, false provenance and wrong frozen bytes,
role confusion, hidden violations, a flipped control and a duplicated JSON key must all be DETECTED.

## 5. Programs and resource rules

Producer: pure-Python exact Fractions; parent-array enumeration with AHU codes; prefix subcarriers by vertex masks; cones
by BFS; Gauss-Jordan elimination over Q. Checker (algorithmically independent): trees grown by leaf attachment with
nested-tuple canonical forms; prefix subcarriers as the closure under deletion of leaves other than l; conditions written
as vector-level commuting squares with explicit embeddings; each dimension certified by an upper bound NV − rank_p
(elimination modulo two primes; rank_p ≤ rank_Q) and a matching lower bound from explicit rational solution families
checked against every row and certified affinely independent by exact rank; matrices for Y1-Y4. GREEN requires both
certificates to equal every preregistered value, equal identity digests, zero violations, all controls REJECTED and all
tamper controls DETECTED. Pinned: Python 3.12, numpy 2.3.5, sympy 1.14.0, mpmath 1.3.0. Stopping rule: one verify run on
push, one dispatch with review=true; a RED is preserved and reported, not re-run until it disappears.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the draft-15 scratch `/tmp/rid16/chk21.py`
(U7 values, section 21's scratch paragraph). While writing the programs for this freeze, the producer and checker were run
locally on U7 and U8 before this file was committed; the U8 dimensions above were hand-derived first and the local runs
agreed. A checker development bug (subcarrier paths read from the class representative instead of the relabelled
subcarrier, and an unsorted canonical serialization) was found and fixed during that local work. Structural counts come
from the counting script `/tmp/rid17/count.py` (sha256 `cfdcc32516b3dddf519493ee40b2002a771c5a12510db635d04f2552aeb79e57`,
not committed; it computes only carrier and unknown counts). The GitHub Actions run is the preregistered execution.
