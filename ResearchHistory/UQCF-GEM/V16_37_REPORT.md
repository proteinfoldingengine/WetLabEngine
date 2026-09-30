# UQCF-GEM v16.37 — Structural minimax audit

Date: 2026-09-30. Parent: `ce4f0c0396fc4a763e5fac1826c180df599d9a00`.
Status: mathematical/source audit with GitHub-executed diagnostic controls and independent threshold recomputation of the supplied 18 endpoint records. This is not a completed fresh certification of the full retained campaign.

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

## T5 — The inherited target is constant, so no-collision is non-discriminating

The independent threshold audit reconstructs legal views by subset/prefix validation, constructs one-incidence neighbors by direct toggles, recomputes child-cover profiles by exhaustive subfamilies, and solves each scalar objective separately as well as the lexicographic nested objective. It imports neither historical producer nor historical verifier.

All 18 supplied endpoint records have:
- published triple (1,1,1);
- independently recomputed scalar-minimum triple (1,1,1);
- independently recomputed lexicographic triple (1,1,1).

There are zero published-value disagreements and zero objective distinctions in this corpus. Thus the general label-pruning limitation does not refute these 18 numerical values.

Since the target triple is constant throughout this dataset, ANY signature, including a constant signature, satisfies its no-unequal-barrier-collision condition. The observed four candidate-signature groups do not provide discriminating evidence that compulsory-coordinate information selects the barrier. This is stronger than the earlier statement that finite no-collision does not prove universality: this particular corpus has no target variation to explain.

This audit consumes the supplied 18 endpoint identities; it does not re-enumerate the full canonical endpoint universe. Completeness is inherited from the separate PR81 enumeration audit. Threshold values are independently reconstructed for each supplied endpoint.

## Verification and status

The added GitHub Actions control checks the exact lexicographic reversal, enumerates both simple paths of the six-vertex abstract graph, reproduces the pinned producer and verifier failure on the controlled graph, and checks the nested-threshold answer against exhaustive paths. It is a diagnostic control, not a retained scientific run.

The theorem above is a direct written proof, not proof-assistant formalization or independent authorship review. No literature novelty claim is made.

GitHub Actions run **36742357518**, execution SHA `45649dbd61c9ffbb14ad4bfa8709157e77a070d7`, succeeded. Its logs show five diagnostic tests passed, both historical routines returned (3,2,3) on the abstract graph versus the exhaustive (3,1,3), and all 18 retained-record numerical checks agreed. The first diagnostic-only successful run was 36742073514.

No retained production code was modified and the full inherited stack was not rerun in this diagnostic stage. Historical completeness/closure receipts remain historical evidence.

Next concrete obligation: prove a unit-barrier theorem in the retained category, or construct an admitted retained pair with a genuinely different barrier using objective-correct threshold reachability. Define a barrier-independent candidate only after determining whether there is target variation to explain. Resolve independent-versus-lexicographic scope explicitly before further generalized certification.

Time is pruning / ordered recoverability update.
