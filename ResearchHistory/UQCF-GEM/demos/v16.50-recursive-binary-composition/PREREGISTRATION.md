# v16.50 prospective recursive binary-composition campaign

PREREGISTERED / NOT EXECUTED / NOT CERTIFIED.

## Exact parent and disclosed prior knowledge
Verified integrated parent: a8280c1c77d7e29f8b90dfd4807bede6411c7ca7; tree687f0ae2981b032aae44a36e68ebd3a869d83ad9; merged PR97. Actual-merge run36863457271 succeeded. Workflow receipt9d087aff03d694b84dd6da4f7b823f68e98df380 was independently audited; documented independent closeout9ffa81ccf39b2d89dead721bf18a9f856550f33f is on the separate audit branch. There is no external-auditor dependency.
v16.49 established one binary parent with two chain children. Its proof and finite results are prior knowledge. The induction proposed below is motivated by that proof, not a blind prediction. No v16.50 scientific numerical execution or implemented recursion precedes this protocol.

## Question and precise proposed interface
Does joining two children satisfying the following interface preserve it?
I1: positive minimal palette requirement m(T,q), with feasibility for every fixed ordered nonempty root palette P iff |P|>=m.
I2: a canonical state C(T,q,P) whose proper descendants use exactly the first m labels of P (a leaf has no proper descendants; it is represented by its singleton compact root support when attached).
I3: every admitted exact-profile state with root support P fixed normalizes to C via admitted one-incidence moves, with total L1 excursion summed over ALL internal vertices <=1, and exact endpoint. Only proper descendants move.
I4: replacing one complete label role by a label absent throughout that subtree preserves EVERY internal hitting coordinate exactly, via parent-before-child additions and child-before-parent deletions. At a fixed parent this is an attached-subtree operation that may change its root support; I3 and I4 are distinct.
I5: unused labels at the child root can be contracted without changing inner profiles; a compact endpoint has nonempty root support of size m, all descendant labels contained in it.
I6: canonical construction is equivariant under ordered-palette relabeling; sequential phases return to the whole exact profile before another deviation phase starts.
Base leaf m=1, no internal coordinates, fixed support needs no normalization. At a binary join, proposed m=max(mA,mB) for target root hitting1, m=mA+mB for hitting2. Distinguish canonical descendants at fixed root P from the compact attached endpoint obtained by root contraction.

## Composition argument and failure gates
Extract each guarantee from the v16.49/v16.48 arguments. Prove base case and preservation under binary joining, including fixed-root normalization, compact endpoints, overlap anchor, disjoint role transport and endpoint uniqueness. The role-dominance argument must apply to arbitrary internal binary subtrees, not only chains. In overlap phases keep parent hitting exact while active child carries <=1; in disjoint transport require every inner coordinate exact while parent alone may carry unit deficit. Track total sum, not per-coordinate bounds. Explicitly prove the palette lower bounds. Any absent hypothesis or counterexample to an interface guarantee is recorded as INTERFACE_NOT_PRESERVED with exact state/profile/failed lemma. A failed construction alone does NOT show a nonunit barrier.

## Frozen validation corpus
Leaf L; cherry C=(L,L); fork F=(C,C). Use exactly two ordered nested-fork trees N=(F,C) (5 internal,11 total vertices) and D=(F,F) (7 internal,15 total vertices). Indices are preorder; left then right. Targets are all {1,2}^5 for N and all {1,2}^7 for D, lexicographic. For each compute proposed width M recursively, test k=M and M+1, global permutations identity/reversal/cyclic j->(j+1) mod k, and two starting modes:
compact: the recursive canonical state globally permuted;
overlap_inflated: start with compact permuted state, visit internal vertices preorder and, at each target-hitting1 vertex, expand both child-root supports to that vertex's current support using admitted root additions; descendants otherwise retained.
This is 1920 case identities, retained even if raw states coincide. No domain expansion/reduction or result-dependent early success stopping. These are directed validation cases, not an exhaustive state-space universe.
Producer saves exact case identity, tree, target, k,M,start and every raw state in each normalization path. Independent verifier reconstructs ALL canonical corpus identities, palette bounds, canonical endpoints and starting states without calling producer logic; requires exact identity equality and independently computes support nesting/nonemptiness, fixed global root, primitive moves, hitting numbers at every internal vertex, and total L1<=1 at EVERY intermediate state.
Mechanism controls also freeze N mirrored (C,F), asymmetric child palettes, anchor excluding0, minimal/spare palettes, whole-role exchanges, both same-child pivot directions, leaf/internal joins, and two individually unit defects totaling2 (must reject). Reject missing/duplicate/substituted case/path identities, invalid state/move/profile/width/endpoint, false coverage/provenance and claimed universal scope.

## Competing outcomes
RECURSIVE_BINARY_INTERFACE_VALIDATED: independent proof review accepts all interface preservation claims and every frozen case/control passes. Generality comes from induction, not directed evidence.
INTERFACE_NOT_PRESERVED: explicit failed guarantee/proof obligation or invalid/overcost construction. Preserve raw evidence; no nonunit inference.
NONUNIT_WITNESS: only if a separately independently verified complete unit-threshold cut over an explicitly declared admitted finite graph plus admitted unrestricted connecting path establishes the relevant independent scalar obstruction. This corpus is not such a cut; new witness experiments require prospective amendment before execution.
INCOMPLETE: any coverage, provenance, resource, verification or reproduction failure blocks certification.
All primary B1/Binf/Bs remain independent scalar minima; LEX is a separate diagnostic. Binary-tree induction, if established, does not prove higher-arity or arbitrary retained-category universality.

## Execution and closure contract
Commit this document prospectively as a DIRECT CHILD of exact integrated parent before numerical science. Preserve genuine missing-recursion and supplied-only-coverage RED on GitHub before implementation. All science/tests GitHub Actions ONLY, Python3.11, Sympy1.13.3, mpmath1.3.0, ubuntu24.04. Full934 inherited checks plus new substantive controls and freshly rerun complete parent49/nested science, byte-identical to published parent. Independent proof/source review; science and fresh reproduction on separate runners; artifacts retain raw paths/certificates/logs/source/input/Git bindings/exact run/head/attempt/workflow/dependencies. Preflight<=5min, science/reproduction/publication/postmerge<=45min each, receipt<=10min. Resource exhaustion yields INCOMPLETE, no adaptive case dropping. Audit downloads/manifests/Git blobs, publish complete evidence, ready and merge exact reviewed head, rerun actual merge, independently audit and durably publish receipt closeout before CLOSED/CERTIFIED. No physical energy/action/gravity/metric/fundamental-time claim.
