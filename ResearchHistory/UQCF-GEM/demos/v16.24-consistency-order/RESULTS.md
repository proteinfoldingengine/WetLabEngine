# v16.24 — Exact consistency order: combined findings

| Required question | Adjudicated answer and support |
|---|---|
| What retained operation is now classified? | The exact worst-case number of overlapping retained views that must be tested jointly to establish nonnegative source realization on their union. Assumptions are fixed common Genesis, finite prefix tree, actual ancestor-closed retained views, and compatible formal nonnegative rational source data. Proofs H0–H4. |
| What happens to the actual prior obstruction? | v16.23's signed-gluing/nonnegative-realization obstruction persists and is sharpened into an exact hierarchy. No cumulative Green obstruction is redefined or claimed to descend. |
| Is any new splitting or structure supplied? | None is postulated. Existing source pushforwards and subtree coordinates are retained. A minimum child-cover is an admissible certificate, not a uniquely chosen physical structure. |
| Can source information be compared across views? | Yes. All local witness data are checked by direct ancestral-fiber pushforward of their unique signed union source. Dual certificates contradict any hypothetical nonnegative union source. H1,H5. |
| What was verified computationally? | 30 current tests and 82 inherited tests; all 3,522 original covers on 17 rooted shapes and their exact metamorphic copies; all 94,185 compatible integer local-source inputs of total ≤2; separate sharpness witnesses for all 1,841 covers of order >1; eleven logged corruptions plus additional coverage/naturality controls. |
| What remains open? | Physical source attainability, physical response-law selection, the operational quantum leg, and carrier/morphism classes beyond those explicitly admitted. This theorem neither determines depth coefficients nor produces a metric or physical geometry. |

## 1. The exact theorem

Let V=(Y_i) be a finite nonempty family of actual root-containing prefix-closed views with union U. At v in U write Ch_U(v) for its immediate children. Define tau_v as the minimum number of given views whose union includes ALL those children; tau_v=0 at a leaf. Then

    h(V)=max(1, max_v tau_v).

This is the LEAST POSITIVE integer h such that, for EVERY compatible nonnegative rational local source family, feasibility of every subfamily with at most h views implies feasibility of the whole family. It is a worst-case property of the cover, not a statement that every input fails first at h. The theorem is proved for arbitrary finite covers; the bounded computational universe is an implementation check, not a physical cutoff.

The result depends on which siblings are jointly revealed by the actual views. It is not merely the number of views, the lineage depth, or the maximum branching. A single view may cover all children at a vertex, reducing tau_v to one even when that vertex has many children.

## 2. Why the bound is sufficient

v16.23 gives a unique signed reconstruction in subtree coordinates:

    x_U(v)=c_v-sum_{w in Ch_U(v)} c_w.

Nonnegative global feasibility is precisely nonnegativity of every such node amount. For each nonleaf v choose a minimum subfamily covering all its children. The corresponding local reconstruction tests exactly the full node inequality at v. If all subfamilies of size at most h(V) are feasible, all full node inequalities hold; leaves are already nonnegative by validity of the individual local sources. This proves sufficiency, not merely agreement of measured ranks.

## 3. Why it cannot generally be improved

For a vertex v attaining h=t>1 with d children, define subtree amounts d−1 on v and its ancestors, one on each immediate child of v, and zero elsewhere. Every subfamily of fewer than t views omits at least one child and has a nonnegative realization. The full reconstruction has value −1 at v. Some t-view child-cover already fails. The local views remain individually nonnegative and overlap-compatible.

This constructs a sharp witness for EACH fixed cover with h>1, not just one favorable star example. The code emits its raw local marginals, signed global source, critical vertex and bad subfamily. The independent verifier reconstructs the pushforwards, checks every smaller subfamily, verifies the failure, and checks a separating functional.

For the stacked actual marginal map A, the functional satisfies

    A^t lambda = e_v,       lambda^t local = -1.

Any nonnegative global x would instead give lambda^t A x=x_v>=0, a contradiction. Positive rescaling of this functional is harmless and is accepted by the checker. Non-permutation coordinate controls transform both the map and dual consistently; they do not treat positivity as invariant under arbitrary untransformed basis changes.

## 4. Strongest consequences, including the positive boundary

If every vertex has at most b children, h(V)<=max(1,b). Therefore on a BINARY prefix tree, compatible local data with every pair nonnegatively realizable have a nonnegative global realization. Pairwise overlap agreement ALONE is not enough; pairwise feasibility is the additional premise. This positive result qualifies any overly broad reading of v16.23's counterexample.

Conversely, take an m-leaf star with one view per leaf and m>=2. Give each local view root amount m−2 and leaf amount one, so total m−1. Any r<m views reconstruct root amount m−1−r>=0. The full union requires root −1. Hence there is no fixed k-view sufficiency theorem for all trees of unbounded branching.

For m=4, all singletons, pairs and triples are nonnegatively realizable, but the full source is (-1,1,1,1,1). This is a formal extensive-source consistency obstruction—not quantum contextuality, a new physical memory law, or evidence of geometry.

Repeated views and already-contained redundant subviews do not change the exact cover order. Replacing views by smaller retained views while keeping the same union cannot lower it. For fixed compatible subtree data, the full-union feasibility condition itself is unchanged. H6 proves these distinctions; the runtime checks cover repeated/reordered views and the declared relabeling transformations, not an unclaimed exhaustive experiment over every possible refinement relation.

## 5. Exact bounded coverage

Producer: ancestor-first parent arrays, sorted recursive shape codes, legal view masks and dynamic programming for child-cover minima. Independent verifier: Pruefer labeled-tree generation/deduplication, direct parent-stepping fiber matrices, exact inverse of the subtree-zeta matrix, exhaustive subfamily minima, complete input-key reconstruction and raw dual checks. It imports neither the producer nor its helpers.

U contains all 17 rooted unordered shapes of one through five vertices, counts 1,1,2,4,9. On each tree every family of one through four distinct admissible views whose union is the whole tree is retained. Different actual view subsets are not identified merely because they are isomorphic. Duplicate views are separate checker controls.

| Original-coordinate result | Count |
|---|---:|
| Rooted tree shapes | 17 |
| Complete view covers | 3,522 |
| Covers with h=1 | 1,681 |
| Covers with h=2 | 1,720 |
| Covers with h=3 | 120 |
| Covers with h=4 | 1 |
| Subfamily occurrences across covers | 44,004 |
| Separate sharpness witnesses, one for every h>1 cover | 1,841 |
| Compatible integer local-source inputs with total ≤2 | 94,185 |
| Globally nonnegative inputs | 72,626 |
| Inputs first failing at a two-view subfamily | 21,411 |
| Inputs first failing at a three-view subfamily | 148 |

The ENTIRE universe is repeated with 0 fixed, i mapped to n−i for i>0, reverse view ordering and reverse vertex storage in each view: another 3,522 covers and 94,185 input occurrences. The verifier checks actual transformed identities and storage, not a producer label. These are metamorphic copies, not independent physical observations.

The complete grid c in {0,1,2}^n, filtered by nonnegative singleton marginals, exactly enumerates compatible nonnegative INTEGER local source families with common total at most two. It is not all rational inputs. General rational and conditional real claims come from H1–H6. The h=4 sharp witness needs total three, so it is supplied separately; absence of order-four failures in the smaller grid is NOT evidence that h<=3.

## 6. Tests that can reject incorrect mathematics

The 28 original behavioral/adversarial tests cover root/path/branching cases, rational scalars, identity/repeated views, changed lineage/storage, minimum-cover sensitivity, valid and invalid duals, invalid endpoints, and complete small-universe reconstruction. Eleven named corruptions are logged with actual rejection reasons: wrong dual, global witness, local marginal, child cover, falsely high/low order, false sample feasibility, foreign origin, Boolean threshold, missing child ledger, missing sample. Additional tests reject missing covers and false metamorphic claims, and reject a valid ordinary linear section for failing retained naturality. That section test is a checker control, not a new UQCF-GEM source construction.

Self-review found a real producer validation bug: (-1,2,99) could be traversed before all parent targets had been range-checked, producing IndexError rather than explicit ValueError. A two-test regression was committed and observed RED. One malformed-target test failed while a reordered-valid-lineage control passed. The correction validates ALL parent targets before following any. No admitted mathematical input, criterion, proof, witness or independent verifier changed.

Final suites: 28 original +2 validation +25 v16.23 +20 v16.22 +22 v16.21 +15 exact parent =112 tests passed. The corrected producer certificate, VERIFICATION.json, TEST_RECEIPT.json and PRODUCTION.json are byte-identical to the initial successful run. The earlier GREEN is not retroactively credited with later guards.

## 7. Execution, evidence and publication

| Role | Run | Execution SHA |
|---|---:|---|
| Wiring RED, 28 intended failures | 36583580004 | 1335532db55062af83fbe2bfd875c18eecb7d490 |
| Initial GREEN | 36584333728 | f838bd86596db5884a9d3b33f245b127c55f56c8 |
| Substantive validation RED | 36584604280 | 3e50f0fb4930502214bc43ed91ee1fc96596a7aa |
| Corrected scientific GREEN | 36585110111 | 19c7069bad79ff361d612f742ad5e79dbfef1dc6 |

The original scientific certificate has 6,426,004 uncompressed bytes, compressed losslessly to 84,760 bytes. Raw SHA256: `d5354333bab67ee84bcd8e1a108d93ff6767d6f37e0fa8842af139a0cf60ee6b`. Compressed SHA256: `9a2e3f05705682b9f20028b793c36a8c6c39636c6125d18d356555cce5d93ade`. Independent verification JSON SHA256: `379e0d777867d07f78f271c254e9418e5d88550ec33cef4555eac53147e5bcad`.

GitHub used Python 3.11.16, SymPy 1.13.3, mpmath 1.3.0. All eight final scientific command exit codes are zero. The final original ZIP was downloaded and its SHA/CRC, logs, test counts, complete scientific files and equality against the first GREEN archive were inspected. No second-environment full scientific reproduction is claimed.

The separate publication workflow retrieves and hash-checks all four original archives, preserves run/job/attempt metadata and logs, verifies the executed source snapshot, reruns all scientific commands and compares complete scientific bytes before committing. Its exact run/commit provenance is recorded separately in PUBLICATION_EVIDENCE.json and the publication artifact receipt. Documentation after scientific execution is not misidentified as the scientific execution SHA. Original RED/GREEN bytes are retained permanently in evidence/archives, not just temporary Actions storage.

## 8. Interpretation and remaining dependency

This stage turns v16.23's examples into an exact per-cover criterion and a sharp hierarchy. Information can be compatible and feasible on every small subfamily without being globally nonnegative; the amount of joint checking required is fixed by actual retained sibling coverage. On binary branching the required order collapses to at most two. On unbounded branching it is unbounded.

No response equation appears in this criterion, so it does not select v16.22's depth coefficients or change the fixed inverse. The proof concerns the already-declared formal nonnegative cone and actual retained fibers. Whether these sources and operations have the required physical realization remains open. No geometric or gravitational conclusion follows by changing the name of the consistency condition.

Review is SELF-REVIEW. The verifier is algorithmically independent, not a separately authored review. Written mathematical proofs are not proof-assistant formalizations. Historical reports and unrelated protein files are unchanged; publication is on an additive research branch, not main.

**Time is pruning / ordered recoverability update.**
