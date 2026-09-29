# v16.30 — Interaction-component closure

Parent: v16.29 publication commit `3543d37f83a9d6849a4f62796c8fd17b907992f0`.

## Question

For a fixed same-union endpoint refinement with event poset E and existing local profile tau(S)=(tau_v(S)) on reachable deletion ideals S, does the profile determine a canonical decomposition of deletion events into independent interaction components?

No new observable is introduced. Only the already-earned local child-cover counts are used.

## Frozen construction to adjudicate

For distinct events e,f define them to be **locally coupled** when there exists a reachable ideal S enabling both and at least one vertex v has nonzero local mixed difference

D_v(S;e,f)=tau_v(Sef)-tau_v(Se)-tau_v(Sf)+tau_v(S).

Let G_tau be the undirected graph on events with an edge for such a witnessed pair. Let its connected components be C_1,...,C_k.

Candidate theorem:

C1. If e and f affect different parent vertices, their local mixed differences vanish at every state; therefore every G_tau edge lies among events whose removed nodes share a parent.

C2. Consequently every connected component is parent-local. Components at different parents are independent in the full local profile even though the scalar maximum h may couple them as shown in v16.29.

C3. For each vertex v, tau_v depends only on deletion events whose removed node has parent v, plus a constant fixed by the endpoint interval. Events at other parents cannot change tau_v.

C4. Therefore the full profile factors exactly by parent:
tau(S) is reconstructed from the restrictions S intersect E_v independently for each parent v.

C5. The finer connected components of G_tau need NOT automatically imply additive factorization within one parent. Adjudicate whether disconnected same-parent components are genuinely independent for tau_v or whether higher-order dependence can exist without any pairwise mixed edge.

Competing outcomes for C5:
A. PAIRWISE_GRAPH_COMPLETE: disconnected G_tau components give exact independent factorization of tau_v.
B. HIGHER_ORDER_OBSTRUCTION: an admissible retained endpoint has no pairwise cross-component mixed difference but nevertheless has irreducible higher-order dependence.
C. UNRESOLVED: bounded search does not decide and no proof settles it.

Do not choose an outcome in advance.

## Required higher-order test

For each parent-local event set through the bounded universe, compute exact Möbius coefficients of tau_v on the reachable Boolean subcubes where those events are simultaneously independently enabled. Search orders 3 through 5. A nonzero coefficient whose support crosses distinct pairwise G_tau components is an explicit higher-order obstruction.

Do not call ordinary predecessor constraints an interaction: comparable events cannot form an enabled square and must be reported separately as order constraints.

## Bounded universe

Reaudit v16.29's complete five-vertex two-event corpus. Extend endpoint-interval enumeration on rooted trees through five vertices, at most four distinct initial views, and at most five deletion events, preserving the same union. Enumerate all reachable ideals, local profiles, pairwise graph edges, connected components and all eligible higher-order Boolean cubes.

Controls must include:
- v16.29 MAX_ONLY: no local edge between different parents despite scalar D_h != 0;
- v16.29 LOCAL_MASKED: a local edge exists even when D_h=0;
- same-parent transmitted examples;
- a synthetic checker-only Boolean function with pure 3-way interaction and zero pairwise mixed differences, labeled CHECKER_CONTROL, proving the higher-order detector can reject pairwise sufficiency;
- malformed endpoint/order/relabeling rejection.

A finite absence of higher-order obstruction is not by itself a theorem. Positive universality requires proof from the child-cover definition.

**Time is pruning / ordered recoverability update.**
