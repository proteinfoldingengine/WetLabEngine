# Multi-payload retained precedence interface scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parent joint closeout:
- JOINT_RETAINED_CLOSEOUT.md at 63f1be4edbf0ee99f9df22012e99285d7a256829.
Continuation index:
- POST_A12_THEOREM_FIRST_SYNTHESIS.md at 25aab220e23c54d6248b8074f90b385168feb793.

## Objective

Extract a reusable theorem for finite retained-information scheduling.

The central object is a quotient map from full labelled incidence states to retained records. A retained controller is legitimate only when an authorized macro is uniformly legal over the entire hidden fiber and produces a uniquely determined next retained record.

Add a finite directed precedence graph on unfinished labelled endpoint obligations. Prove that acyclicity plus quotient-uniform macro renewal yields a legal topological repair to the exact destination, while a directed cycle is an exact deadlock for this declared precedence policy.

This is an interface theorem. It does not claim every native repair problem admits such a quotient or precedence graph.

## Full and retained state

Let X be a declared finite class of protected full labelled incidence states with original floors and 3<=tau<=4.

Let
    pi:X->R
be a retained-record map. Fibers pi^{-1}(r) may contain multiple full states.

Each problem instance also has a finite set V of labelled endpoint obligations. Completing v in V means executing a declared finite native macro m_v whose exact incidence changes are determined from retained address/phase data.

For retained record r and unfinished set U subseteq V, derive a directed graph
    G(r,U)
on U.

The policy authorizes exactly vertices of indegree zero.

## Required quotient-uniform macro condition

For every reachable retained state (r,U) and every authorized v:

1. UNIFORM LEGALITY:
   for every full state x in pi^{-1}(r) consistent with the same completed obligations, every primitive of m_v is syntactically legal, respects original floors, and stays in 3<=tau<=4.

2. UNIFORM RETAINED UPDATE:
   there is a deterministic update
       r'=Phi_v(r)
   such that for every such x,
       pi(m_v(x))=r'.

3. EXACT OBLIGATION UPDATE:
   v reaches its exact labelled endpoint requirement and does not undo already completed obligations.

4. RENEWAL:
   the newly derived graph satisfies
       G(r',U minus {v}) = G(r,U) induced on U minus {v}.
   Thus completing an eligible macro deletes its vertex and incident edges but does not secretly create new precedence among the remaining obligations.

5. HIDDEN-FIBER PRESERVATION:
   if a family of hidden distinctions is declared invariant, the macro does not read or alter those incidences. Record whether distinct full states remain in the next fiber; do not assume injectivity.

## Required theorem

Prove:

A. If initial G is acyclic, repeated selection of any indegree-zero vertex terminates after |V| macros at the exact labelled destination, with every primitive protected and floor-legal.

B. The retained controller needs no hidden-state read because legality and update are uniform over each fiber.

C. If the remaining induced graph contains a directed cycle and the policy authorizes only indegree-zero vertices, then after all vertices outside the cycle that can be removed are exhausted, the policy deadlocks on a nonempty cyclic remainder. Scope this to the policy, not native connectivity.

D. A decreasing rank |U| proves termination in the acyclic case.

E. If initial fibers contain multiple hidden states and the declared macros preserve a hidden invariant family, quantify the surviving multiplicity when possible.

## Concrete embedding obligation

Show that the closed two-payload joint theorem is an instance:
- retained r=(M_core,D);
- V={p,q};
- environment x derived from M_core;
- graph has one edge P_x -> P_y;
- the joint theorem supplies uniform legality for every hidden spectator Z;
- after P_x completes, the remaining graph has one isolated vertex;
- 2^s hidden spectator states remain indistinguishable.

This embedding must use the corrected joint theorem at 6454074a95b526bf2125272f76bfad392e2f468f.

## Non-circularity requirement

The interface is useful only if graph derivation and macro certificates are obtained from retained data and proved uniformly over hidden fibers. Do not define an edge merely by consulting whether a hidden full-state execution succeeds.

A future realization theorem must derive G from concrete retained certificate formulas.

## Boundaries

No claim that acyclicity is necessary for native repair. No claim that every cycle is disconnected. Interleaved primitives, different macros, probing, extra retained information or another quotient may repair a cyclic instance.

No physical force, geometry, energy, observer field, continuum or fundamental time.

If successful, next work is REALIZABILITY: derive nontrivial multi-vertex precedence graphs directly from native retained certificate formulas and test a genuine cycle family.
