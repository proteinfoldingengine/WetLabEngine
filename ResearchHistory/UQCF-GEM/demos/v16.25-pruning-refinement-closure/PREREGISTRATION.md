# v16.25 — Pruning/refinement closure preregistration

Parent: v16.24 publication commit `afdbd1b405193a7e83bf905342ea9ff50338f6cc`.

## Question

Given a fixed common-Genesis finite prefix tree and a retained cover V whose exact nonnegative consistency order h(V) is established in v16.24, what is determined when each view is replaced by an actual retained subview through admissible ancestral pruning, with the same final union?

This campaign asks for the exact relation between h before and after pruning and whether successive pruning factorizations give the same result. It does not add a response operator, geometry, metric, connection, fitted law or physical source postulate.

## Frozen candidate theorem to adjudicate

Let V=(Y_i) and Z=(Z_i) with Z_i subseteq Y_i actual root-containing prefix-closed retained subviews and union Z_i = union Y_i = U. Define h by v16.24's child-cover criterion.

1. MONOTONICITY: h(Z) >= h(V).
2. EXACT LOCAL LAW: for each v, tau_v(Z) is the minimum number of pruned views whose retained child sets cover Ch_U(v); therefore h(Z) is recomputed from actual incidence, not inferred from branch count.
3. EQUALITY CRITERION: h(Z)=h(V) iff max_v tau_v(Z)=max_v tau_v(V), with leaf/order-one convention explicit. This is intentionally numerical; any stronger structural iff must be separately proved.
4. COMPOSITION: for W_i subseteq Z_i subseteq Y_i with common union U, direct Y->W pruning and staged Y->Z->W produce identical retained views, source pushforwards, child incidence, tau and h.
5. SOURCE FEASIBILITY: for fixed compatible subtree data c on unchanged U, global feasibility is unchanged by cover refinement, while the worst-case amount of joint local checking can increase.
6. SHARPNESS: every refined cover with h>1 retains the v16.24 admissible sharp witness for its own actual child incidence. No witness may be copied from the coarse cover unless its marginals are recomputed through actual fibers.

A counterexample to any item is a valid scientific result.

## Proof obligations

Derive monotonicity directly: each pruned child set A'_i(v) is a subset of A_i(v), so any k pruned views covering Ch_U(v) imply the corresponding k coarse views cover it. Hence tau'_v >= tau_v. Composition must be derived from longest-retained-ancestor retractions/fiber sums, not from a matrix whose construction presupposes composition.

The common-union premise is essential. If pruning changes U, the node inequalities themselves change and no monotonicity claim is preregistered across the different global carriers.

## RED/GREEN and rejection requirements

RED is not satisfied only by missing modules. Before GREEN, tests must include a deliberately false "refinement can lower h" certificate, an incorrect staged pushforward coefficient, an illegal non-prefix subview, a changed-union case mislabeled comparable, and a composition endpoint mismatch. At least one substantive RED must fail against inherited implementation behavior before its correction/implementation.

GREEN must independently reconstruct direct and staged fiber aggregation using exact rational arithmetic and verify representative examples plus a bounded exhaustive universe. The verifier must not import the producer.

Metamorphic checks: parent-preserving relabeling, view/storage reorder, identity pruning, repeated pruning, and two different legal factorizations with the same final retained family.

## Bounded implementation universe

Enumerate all rooted unordered trees through 5 vertices; all distinct legal covers with at most 4 views; and all componentwise legal subview refinements preserving the same union. Deduplicate by exact labeled retained subsets, not dimension or isomorphism alone. The finite enumeration audits implementation; the general claims require the written proof.

Preserve v16.24 and inherited v16.21–v16.23 regressions. Record execution SHA, run/job/attempt, exact counts, artifacts and checksums. Failed attempts remain failures.

**Time is pruning / ordered recoverability update.**
