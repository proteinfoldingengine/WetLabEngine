# PREREG Q536(b): multi-step recovery paths from each first actor (GEOMETRY_DELAY fixture)

- Ref: uqcf-sci-q536b-prereg
- Written: 2026-11-22 13:54 MST (UTC-07:00), BEFORE any Q536(b) execution.
- Authorization: Aaron Spradlin, 2026-11-22 13:51 MST, own words: "Yes, preregister and run" (answer to "Do you want a preregistered local run for (b), the multi-step recovery paths?").
- Scientific parent: research branch `research/uqcf-overlapping-guard-exchange` head `e7e01bab68ba5171dacd91333f98d208d810dac3` (verified 13:52 MST). Fixture source: `ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py` @ PR153 head `4538a663258f169ad60c252daef11fe1a1447e13`, sha256 `4d9c4a2c9392acf02fb62fd07dadb996ecedfcb03c1a2aa95885e5777e195cfe`. Inherited legality source: `ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py` @ 4538a663, git blob `c10ac57f988a439144e21898bd2b33ece0838a9b` (= the pin in check_geometry_repair.py).
- Workflow SHA: none. This is a LOCAL box run, not a GitHub workflow run (see "AGENTS.md compliance" below).
- Nature of result: a finite exact enumeration on one supplied preparation. It is a SIMULATION, not a discovery, and no finite no-counterexample result will be stated as a universal theorem.

## 0. Already-known findings (disclosed, NOT preregistered predictions)
From Q536 (scratch artifact `independent_2026-11-22_1243_q536_geometry_actor_uniqueness/RESULT.md`), which relied on the committed script's own assertions and hand derivation (no new run):
1. After the source event (A=0 deletes T=1), the script asserts exactly 32,575 inherited-legal next deletions, and per-view counts equal the column-count derivation.
2. Depth 1: exactly one legal deletion passes G, namely (B=12, ULEAF=2) (script assertion `candidates == [(B, ULEAF)]`).
3. Lemma 536.1: every one of the 25 views has at least one legal move under inherited legality alone.
4. The post-source state fails G (script `must_reject(work1)`).
No exploratory multi-step computation of any kind has been run. No feature counts beyond those above have been computed.

## 1. Frozen mathematical objects
- Fixture: `fixture()` of check_geometry_repair.py @4538a663, reproduced byte-for-byte (the local run will import the fetched file, whose sha256 is checked against the value above). Features f = (parent, grade, initial support). Views LABELS = 0..24. A=0, B=12, T=1, ULEAF=2, R=3, CHILD=4, B_PRIVATE=5. MU = 1984.
- subtotal / squares: exactly as in `run()` (subtotal[parent] += subtotal[child], descending index; sq_v = subtotal_v^2).
- State: S = (row_0, ..., row_24), row_i = set of feature indices held by view i. Initial S0 = `initial_state(features)`. Start state S1 = S0 with T removed from row_A (the source event; it is verified with engine.atomic as in the script).
- Work: W(S)_ij = sum_{v in row_i XOR row_j} sq_v (inherited v15.40 two-row functional; same as `work_for`).
- INHERITED legality (the ONLY move rule): (i, v) is legal at S iff, exactly as engine.atomic accepts it:
  (L1) v in row_i and v != 0; (L2) no w in row_i with parent(w) = v ("non-leaf"); (L3) the union of all rows is unchanged by removing v from row_i, i.e. some j != i has v in row_j ("same union" = last-copy guard).
  NOT part of legality: any schedule, any actor order, enumerator order, the degree-four gate, MU, or G. Any actor may move at any step.
- Move: (i, v) maps S to S' with row_i' = row_i \ {v}, other rows unchanged.
- SUPPLIED recovery predicate G (used ONLY as the recovery test, never as a move filter): G(S) holds iff min_{i<j} W(S)_ij == MU AND every view has degree exactly 4 in the graph of pairs with W_ij == MU. This is the gate in `degree_candidates` (min == MU, all degrees 4), i.e. the v15.43 carriers "degree_not_four" admission at the MU level.
- Diagnostic predicate G' (reported, not primary): min-edge graph (pairs at the actual minimum, whatever it is) is 4-regular.

## 2. Recovery definition and primary objective
- A path of length k is a sequence of legal moves m1..mk starting at S1. Its FIRST ACTOR is the view of m1. Later moves may be by any views (including the first actor again).
- The path RECOVERS at depth k if G(S_k) holds. (Intermediate states are not required to fail G; min depth is reported.)
- A first move m1 = (i, v) is RECOVERING within bound K if some path of length 1..K beginning with m1 recovers.
- PRIMARY OBJECTIVE: for each first-actor view i in 0..24, with bound K = 2:
  recovers_i (yes/no), min_depth_i (1, 2 or none), N_raw_i = number of recovering first moves (i, v) counted by raw feature index v, N_class_i = same counted by feature class (section 4), and the list of recovering depth-2 completions by (second actor, class).
- Bound K = 2 rationale: the state space is finite (deletion-only; each step removes one of the finitely many row-incidences, so every path has length <= total incidences), but exhaustive search to the terminal depth is astronomically large (about 3.3e4 moves at step 1). K = 2 is the largest depth that is exhaustive within the compute budget below: about (number of first-move classes) x (number of second-move classes), order 1e8 to 1e9 G-evaluations, vectorized. Depth >= 3 is NOT searched and recovery at depth >= 3 stays an UNRESOLVED proposition for every view whose result at K=2 is "no".

## 3. Diagnostic objectives (reported, not decision-bearing)
- D1 per view i: number of legal first-move classes and raw moves (must reproduce per-view counts summing to 32,575).
- D2 counts of depth-2 states passing G' but not G.
- D3 for each recovering depth-2 path: whether (B, ULEAF) is one of the two moves, whether the first actor's move is "undone" in the sense that W(S_2) row of the first actor equals W(S1) row, and whether the final MU-edge set equals the depth-1 repair edge set (the A<->B swap of the initial edge set).
- D4 engine conformance: inherited legality function vs engine.atomic acceptance on the control set in section 6.

## 4. Enumeration domain and dedup (canonicalization)
- Full domain: all legal m1 at S1; for each, all legal m2 at S1.m1. Depth-1 G check on all m1; depth-2 G check on all (m1, m2).
- Feature classes: two features are equivalent iff they have the same parent, the same grade (hence same sq, both being childless leaves), no children, and the same initial support. All cut features (index >= 6) have parent 0 and no children. Within a class, deleting copy c or copy c' from the same row gives states identical up to a permutation of equivalent feature indices, which preserves W, G, and legality at all later steps. So the search runs over class-level moves; raw counts are recovered by multiplying by copy multiplicity at that state (copies of the class still held by the actor; at depth 2 this accounts for a class whose copy was removed at depth 1).
- Special features T, ULEAF, R, CHILD, B_PRIVATE and the root are kept as singleton classes (they have distinct supports/parent relations).
- Canonical state key: sorted multiset of (class id, frozenset current support) over features. Used to dedup depth-2 states for D2/D3 counting; primary per-first-move counts are reported per (m1 class) regardless of dedup.

## 5. Competing outcomes / branches (falsifiable), at K = 2
- BRANCH ONE: exactly one first-actor view recovers within K=2, and it is B (=12). Implication: within depth 2, actor uniqueness survives relaxing "one step"; selection is still by supplied G on this supplied preparation; not an inherited selection (536.2 stands).
- BRANCH ONE-OTHER: exactly one view recovers and it is not B. Implication: contradicts the depth-1 picture; would flag a fixture/enumeration error first (re-check) before any reading.
- BRANCH SEVERAL: two or more first-actor views recover within K=2. Implication: "which view acts" is not unique even under G once one extra step is allowed; the actor is fixed by schedule/continuation (supplied), strengthening the Q536 closure.
- BRANCH NONE: zero views recover. Impossible given known finding 0.2 (B recovers at depth 1); if observed it is a production error (RED).
Prediction stated before running (author's expectation, not a claim): SEVERAL is plausible (the first actor's perturbation may be compensated in one further move by an actor holding a same-square feature), but BRANCH ONE is also plausible because a single-row change of size sq breaks degree-4 rows that one further single-row change usually cannot fully repair. No numerical prior.
None of the branches can change the status line: G and the preparation remain SUPPLIED.

## 6. Production, verification and rejecting controls
- Production P: numpy vectorized class-level enumeration (incremental row update W_i += sq * (+1 if v in row_j else -1)).
- Verifier V (algorithmically independent): pure-Python, uses the cut formula W_ij = sum_f sq_f [exactly one of i,j in supp_f] with support-delta updates (not row XOR), generates depth-2 candidates by necessary-condition pruning (second actor must touch every pair that violates min>=MU and every view whose degree != 4 must be the second actor or adjacent through a changed entry), and recomputes W from scratch for every recovering state found and for a fixed-seed random sample of 200 non-recovering depth-2 states. Acceptance: exact equality of the full set of recovering (m1 class, m2 class) pairs and of per-view counts between P and V (identity equality, not count equality alone).
- Rejecting controls (each must be REJECTED, else RED):
  C1 illegal moves: (A, R) non-leaf; (A, CHILD) same union; (i, 0) root; (i, v) with v not in row_i; (A, T) again at S1 (already deleted). Checked against both the legality function and engine.atomic.
  C2 wrong values: a W with one MU edge raised by 1 must fail G; S1 must fail G; S0 must pass G.
  C3 missing / duplicated / substituted records: the comparator must flag a result set with one recovering pair removed, one duplicated, and one replaced by a non-recovering pair.
  C4 false coverage: the comparator must flag a per-view legal-move count table with one view decremented (vs 32,575 total and the script's column counts).
  C5 depth-1 reproduction: depth-1 recovering set must equal [(B, ULEAF)] exactly; else RED and stop.
- engine.atomic conformance: run on all C1 controls and on a fixed-seed sample of 300 legal class representatives at S1 and 300 at random depth-1 states; acceptance must agree with the legality function on every sample.
- Failed runs and RED evidence are preserved in the artifact folder, not deleted.

## 7. Resource and stopping rules
- Budget: production <= 60 min wall clock, verifier <= 90 min, peak RAM <= 1.5 GB (box has ~2 GB free), disk <= 200 MB, local CPU only (8 cores), no network after source fetch, no GitHub Actions.
- If a budget is exceeded: stop, report per-view results only for first-actor views whose depth-2 enumeration completed in both P and V, label everything else PARTIAL/UNRESOLVED exactly. No extension of the budget or depth after seeing results.
- Seeds fixed: 536 for all sampling.

## 8. Outputs
In the scratch run folder: code (production, verifier, controls), RESULTS.json (per view: recovers, min_depth, N_raw, N_class, depth-2 completions), VERIFY.json, CONTROLS.json, logs, SHA256SUMS, RESULT.md with claim limits.

## 9. AGENTS.md compliance (explicit)
Done here: prereg committed before execution; known findings disclosed; objects, objectives, domain, outcomes, resource and stopping rules frozen; independent production/verification; rejecting controls; typed arguments vs bounded evidence separated.
NOT done in this local run (missing requirements, reported, not waived): GitHub run of the complete inherited foundational stack with pinned dependencies and inspected logs; uploaded execution artifacts with fresh reproduction in a publication job; committed durable evidence/manifests with downloaded digest inspection; review, PR readiness, merge and post-merge audit. Hence the stage is NOT CLOSED/CERTIFIED. Results are local bounded evidence only.

## 10. Claim limits (fixed in advance)
- Scope: this fixture, this commit, inherited legality as defined, G as defined, K <= 2.
- No physical, energetic, temporal, geometric or gravitational reading. G and the preparation are SUPPLIED; no result here moves anything SUPPLIED -> DERIVED.
- Status line unchanged regardless of branch: native bridge NOT_DERIVED; physical result Not claimed; scientific_breakthrough false.
