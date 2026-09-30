# UQCF-GEM v16.37 — Structural minimax audit

Date: 2026-09-30. Parent: `ce4f0c0396fc4a763e5fac1826c180df599d9a00`.
Status: mathematical/source audit, with a small executable algebra control. This is not a completed fresh certification of the retained campaign.

## Question and scope

Continue the v16.36 barrier-law investigation by separating consequences of minimax definitions from retained-incidence-specific information. Preserve the historical artifacts. No physical energy, action, metric, geometry or fundamental time is introduced.

Source authority: v16.35 PREREGISTRATION.md; v16.36 producer.py, verifier.py, PREREGISTRATION.md and PROOFS.md at the pinned parent.

## T1 — Fixed-fiber scalar minimax barriers are ultrametric by construction

Fix one legal cover graph G and one endpoint signature q0. Let c(Y)=||q(Y)-q0||_1. For endpoints a,b in q^{-1}(q0), define

d(a,b)=min over a-to-b paths gamma of max over Y in gamma of c(Y).

Finite graph connectivity guarantees a minimizing path. For any a,b,c in this SAME fiber, concatenate a minimizing a-to-b path and a minimizing b-to-c path. Its maximum cost is max(d(a,b),d(b,c)), hence

d(a,c) <= max(d(a,b),d(b,c)).

Reversing paths proves symmetry. Constant paths give d(a,a)=0. Nonnegativity is immediate. Thus d is a pseudoultrametric on the fixed fiber.

Two endpoints have d=0 exactly when they lie in the same q-preserving move-component: every zero-cost vertex has q=q0, and conversely a q-preserving path costs zero. Appending zero-cost within-component paths shows that d is independent of the representatives. On the set of q-preserving components it is therefore an ultrametric (distinct components have positive distance).

The proof applies separately to any nonnegative vertex cost that vanishes exactly on the fixed fiber, including the Linf and changed-coordinate-support scalar costs. It does NOT assert that barriers based on different q0 values form a single ultrametric.

Whole-union cover graph connectivity also has a direct retained proof: add missing incidences ancestor-first in every view until every view is the full tree. Reverse such expansions to reach any other cover. Prefix validity and full union are preserved. No bounded enumeration is needed for this connectivity argument.

## Consequence for Gate E

The v16.36 five-vertex zero-ultrametric-violation count remains a useful implementation control, but the scalar B1 inequality follows from path concatenation for all finite admitted cover graphs. It is not evidence selecting a new physical geometry or a special retained law. The empirical statement remains intact; this audit supplies its mathematical explanation.

This proves a fixed-fiber scalar statement. It does not prove the v16.36 candidate-signature factorization.

## T2 — Candidate signature is downstream of the target barrier

The source computes the barrier triple z first, then defines the allowed set by the three coordinatewise bounds dev(Y)<=z. It computes compulsory coordinates by reachability in that allowed set and attainable values across the allowed set. The dependency is

legal graph and q -> z -> allowed set -> compulsory coordinates / attainable ranges -> C.

Consequently C is not presently an independently computable local predictor that avoids solving for z. No-collision is still a well-defined descriptive factorization question; dependence on z alone does NOT prove that the factorization is tautological, nor that it is false.

A predictive follow-up must define input data without first solving the target barrier and prove that those data suffice, or exhibit equal input data with unequal barriers. Simply enlarging the historical no-collision search cannot settle the predictor issue.

## T3 — Single lexicographic label pruning is not generally sound

Both pinned v16.36 source files use the same recurrence: at a vertex, keep only one lexicographically best triple, extend a label by componentwise maximum with the next vertex's cost, and discard a lexicographically larger label.

Componentwise maximum is not order-preserving for lexicographic order:

x=(2,2,1) <lex y=(3,1,3),
but with w=(3,1,3),
max(x,w)=(3,2,3) >lex max(y,w)=(3,1,3).

Therefore discarding y solely because x is lexicographically smaller can remove the eventual optimum.

An explicit UNDIRECTED abstract graph has edges a-u, u-x, a-v, v-x, x-w, w-b. Set q0=(2,2,2), label a,x,b with q0, label u with (4,2,2), and label v,w with (3,3,3). The corresponding (L1,Linf,support) costs are zero at a,x,b, (2,2,1) at u and (3,1,3) at v,w.

There are exactly two simple a-to-b paths. The u route has triple (3,2,3); the v route has triple (3,1,3). The latter is the true lexicographic optimum. Single-label pruning at x retains (2,2,1) and rejects (3,1,3), so it reports (3,2,3).

This is an abstract q-labeled graph control, NOT an admissible retained-tree counterexample: no claim is made that these q labels/edges arise from legal one-incidence retained moves. It refutes a general justification for the recurrence, not the 18 numerical records. The historical scalar B1 is unaffected by this particular label-pruning defect; correctness of secondary objectives needs an independent method or a retained-specific theorem.

Producer and verifier being separate files is insufficient algorithmic independence when both use this same recurrence. The canonical 18-record completeness repair remains valid as a coverage repair; this is a separate objective-search issue.

## T4 — Sound route for lexicographic and independent scalar objectives

For lexicographic optimization, solve three reachability problems in sequence:

1. Find the least t1 such that a,b connect in {Y:c1(Y)<=t1}.
2. Within that subgraph, find the least tInf such that a,b connect when cInf(Y)<=tInf.
3. Within both bounds, find the least ts such that a,b connect when cs(Y)<=ts.

Finite thresholds are attained vertex-cost values. The resulting tuple is lexicographically minimal by the definition of nested optimization. Equivalently, keep all componentwise nondominated labels instead of one lexicographic label.

If the intended B1, Binf and Bs are THREE INDEPENDENT scalar minima, each must instead be solved on the unrestricted graph separately. The original v16.35 preregistration states independent scalar minima; its later localization addendum refers to a lexicographic triple. These are different objectives in general and must be explicitly distinguished before a generalized certification.

No replacement implementation or altered historical result is supplied by this audit.

## Verification and status

The added GitHub Actions control checks the exact lexicographic reversal, enumerates both simple paths of the six-vertex abstract graph, reproduces the pinned producer and verifier failure on the controlled graph, and checks the nested-threshold answer against exhaustive paths. It is a diagnostic control, not a retained scientific run.

The theorem above is a direct written proof, not proof-assistant formalization or independent authorship review. No literature novelty claim is made.

Next concrete obligation: independently recompute the inherited 18 retained endpoint triples with threshold reachability, disambiguate independent-versus-lexicographic objectives, and preserve any differences and their smallest admitted witnesses. Only then generalize the barrier classifier without target-barrier-derived input.

Time is pruning / ordered recoverability update.
