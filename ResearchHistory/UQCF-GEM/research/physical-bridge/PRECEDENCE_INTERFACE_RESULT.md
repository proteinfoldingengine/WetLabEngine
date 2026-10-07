# Multi-payload retained precedence interface theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: PRECEDENCE_INTERFACE_SCOPE.md at 28ec21aee2b2bcc3aaee271b75c0ee85bda9d422.
Evidence: written mathematics only.

## 1. Retained quotient repair system

Let X be a declared class of full labelled incidence states satisfying their original floors and protected-band condition 3<=tau<=4.

Let R be a retained-record space and
    pi:X->R
a deterministic retained map.

A repair instance has a finite set V of labelled endpoint obligations. V is complete: when every v in V is completed and no completed obligation has been undone, the full state equals its declared exact labelled destination.

At any stage let U subseteq V be the unfinished obligations and r the retained record. Write
    X(r,U)
for the full hidden states consistent with r and with exactly the same already-completed obligations.

From retained data alone derive a directed graph
    G(r,U)
on U.

The declared policy authorizes exactly vertices of indegree zero.

For each authorized v, retained address/phase data determine a finite native macro m_v.

## 2. Uniform macro-renewal hypotheses

For every reachable (r,U) and authorized v require:

**H1 Uniform legality.**
For every x in X(r,U), every primitive of m_v is syntactically legal, preserves every original floor and remains in 3<=tau<=4.

**H2 Uniform retained update.**
There is one deterministic r'=Phi_v(r) such that
    pi(m_v(x))=r'
for every x in X(r,U).

**H3 Exact obligation completion.**
m_v completes the exact labelled endpoint requirement v and does not undo any obligation in V minus U.

**H4 Graph renewal.**
    G(r',U minus {v})
is exactly the induced subgraph
    G(r,U)[U minus {v}].

**H5 Hidden-invariant preservation when declared.**
Any incidence family designated hidden-invariant is neither read nor changed by m_v.

The graph and all H1-H4 certificates must be derived/proved from retained data and the declared carrier. They may not be obtained by querying which hidden x is actually present.

## 3. Acyclic completion theorem

**Theorem P.**
If the initial precedence graph G(r0,V) is acyclic and H1-H4 hold at every reachable stage, then repeatedly selecting ANY indegree-zero unfinished vertex yields a finite protected native repair to the exact labelled destination.

The process uses exactly |V| macros. Its macro rank
    rho=|U|
decreases by one after each macro.

### Proof

A finite nonempty DAG has an indegree-zero vertex. Therefore if U is nonempty, the policy has at least one authorized v.

By H1, m_v is a legal protected native sequence for the actual full state, regardless of which hidden member of X(r,U) is present.

By H2 the controller can update r to Phi_v(r) without learning the hidden full state.

By H3, v becomes exactly complete and previously completed obligations remain complete. Thus the new unfinished set is U' = U minus {v}.

By H4, the new graph is the induced subgraph of the old DAG on U'. An induced subgraph of a DAG is a DAG.

Therefore the same argument repeats whenever U' is nonempty.

At each completed macro |U| decreases by one. Since V is finite, after exactly |V| macros U is empty.

By completeness of the obligation set and H3, every exact labelled endpoint requirement is then satisfied simultaneously, so the full state is the declared exact destination.

Every primitive along the entire concatenated path was protected and floor-legal by H1. QED.

## 4. No hidden-state read theorem

The controller's decisions at stage (r,U) use only:
- r;
- U/completed-obligation bookkeeping;
- G(r,U);
- the declared deterministic choice among indegree-zero vertices;
- retained macro address/phase data.

H1 says the chosen macro is legal for EVERY x in X(r,U). H2 says all those possible x produce the SAME next retained record r'.

Thus neither selecting the macro nor updating the retained state requires distinguishing which hidden x is actual.

This is the exact quotient property:
    all hidden full states in one retained fiber have the same authorized retained transition.

They need not have the same full successor; they need only remain represented by the same next retained record while satisfying the same completed obligations.

## 5. Cycle obstruction for the declared policy

**Theorem C.**
If G(r,U) contains a directed cycle, no vertex on that cycle can be executed while all cycle vertices remain unfinished under the indegree-zero-only policy.

Each cycle vertex has an incoming edge from the preceding unfinished cycle vertex, so its indegree is at least one.

Vertices outside the cycle that become indegree-zero may still be completed. H4 only deletes completed vertices and incident edges. Since no cycle vertex is eligible, every edge of the directed cycle persists.

Because the graph is finite, after all removable outside vertices have been exhausted, the policy reaches a nonempty remainder with no further eligible progress on the cycle. In particular the cycle obligations cannot all be completed by this policy.

Equivalently, a finite precedence graph admits complete repeated source deletion iff it is acyclic.

This is a POLICY obstruction. It does not prove native disconnection. A different macro, interleaving, probing step, retained record or quotient may remove/bypass the cycle.

## 6. Hidden multiplicity can survive exact completion

Suppose a subset of incidence coordinates Z is hidden-invariant under H5.

If two states x,x' in X(r,U) differ only on Z, every macro reads/changes only non-Z coordinates. Therefore their Z differences persist after the same retained macro sequence.

H2 may map both full trajectories through identical retained records even though their full states remain distinct.

If an initial fiber contains N different assignments of Z and no macro changes or identifies them, the corresponding N full trajectories remain distinct through completion, each reaching its own exact destination that preserves its original Z.

Thus exact retained control does not require the quotient map pi to become injective.

## 7. Embedding of the closed two-payload theorem

Use the corrected joint theorem at
    6454074a95b526bf2125272f76bfad392e2f468f.

Retained record:
    r=(M_core,D,phase).

Obligations:
    V={p,q},
one exact target-core replacement for each labelled payload.

M_core identifies environment x in {b,c}. D identifies the labelled payload P_x whose target equals x and the other payload P_y.

Derive
    G(r,V): P_x -> P_y.

This graph is a DAG with one edge.

### H1

The joint theorem proves uniformly for every hidden spectator set Z that completing P_x first stays at tau=4 through both primitives. After that, completing P_y also stays at tau=4. Floors are preserved.

### H2

M_core updates by its retained miss-count formula using only the active core state; D is immutable and phase/completion bookkeeping updates deterministically. Z is never consulted.

### H3

Each two-edit macro changes exactly its payload core from a to its prescribed target and leaves the other payload, environment, controlled roots and Z unchanged.

### H4

After P_x completes, the remaining graph is the induced graph on {P_y}, namely one isolated vertex.

### H5 and hidden multiplicity

Z is never read or changed. For fixed initial environment and D there are 2^s possible Z assignments with the same retained record and same macro order. All remain distinct and reach their corresponding exact Z-preserving destinations.

Thus the closed joint theorem is a concrete non-injective retained quotient satisfying Theorem P.

## 8. What the interface adds

The two-payload theorem showed one precedence edge.

The present theorem identifies the reusable structure needed to scale that discovery:

    full state
       -> retained quotient record
       -> retained-derived precedence graph
       -> source macro
       -> uniform quotient update
       -> induced precedence graph
       -> exact completion.

The important condition is not merely DAG acyclicity. It is DAG acyclicity PLUS uniform legality/update over every hidden state in the retained fiber.

Without fiber-uniformity, a retained controller could appear valid only because a hidden full-state distinction was silently consulted.

## 9. Non-circularity and limits

This theorem does not tell us how to derive a useful graph G from arbitrary native endpoints. H1-H4 must be established independently from concrete retained certificate formulas.

Defining an edge by first examining the hidden full state or by simulating an unretained support would violate the interface.

The theorem also does not claim:
- every repair problem has a finite macro quotient;
- every valid native path factors into these macros;
- acyclicity is necessary for native connectivity;
- a cyclic macro policy cannot be repaired by another construction.

## 10. Next frontier: realizability

The next mathematical task is not another abstract graph theorem.

It is to derive a genuinely multi-vertex G directly from native retained certificate+address formulas in a concrete carrier.

A useful realization should:
1. have at least three labelled endpoint obligations;
2. derive at least two nontrivial precedence edges from retained miss/cover data;
3. renew the retained graph after each macro;
4. preserve hidden incidence multiplicity;
5. include a concrete cyclic retained graph whose declared macro policy stalls, while carefully distinguishing that stall from native disconnection.

That would test whether the quotient-precedence interface is a real recurring mechanism rather than only a formal wrapper around the two-payload example.

No physical force, geometry, energy, observer field or fundamental time is inferred.
