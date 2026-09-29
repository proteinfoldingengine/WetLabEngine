# v16.29 — Types and general arguments L1–L7

Written arguments before the new adjudication. Self-reviewed, not proof-assistant formalized. All inherited references below are at parent `d732a772b5c9244896e481c77658b78d7cdb9efc`, under ResearchHistory/UQCF-GEM.

## Typed provenance

| Object | Construction and type | Provenance / assumptions |
|---|---|---|
| X, V=(V_i), U | Finite common-Genesis rooted tree, indexed nonempty root-containing prefix-closed views, U their actual union | v16.27 completion/PROOFS.md T1–T3, C1; v16.28 PROOFS.md T1–T3 |
| e=(i,c), f=(j,d) | Distinct current nonroot leaf incidences, both removable in either order, common union preserved after BOTH deletions | Same references; distinct enabled events form an actual commuting deletion square |
| t_v(V)=tau_v(V) | Minimum cardinality of a subfamily covering Ch_U(v), zero for a leaf or a vertex outside U; integer | v16.24 TYPE_AND_PROOF.md C7–C8,H2–H3; v16.27 C2 |
| h(V) | max(1,max_v t_v(V)); integer consistency-testing order | v16.28 T4. Cone interpretation is inherited formal nonnegative rational feasibility, not physical attainability |
| D_v, D_h | Four-state mixed differences of t_v and h respectively | Derived from those SAME fixed quantities; no new source or response object |
| B | max(1,unchanged local components), evaluated on the initial state | Auxiliary exact algebra, not a fitted baseline |
| Equivalence | Parent-preserving bijection plus simultaneous view permutation, transporting event identities | v16.27 C6 / v16.28 D7; no equal-dimension carrier identification |

Finite scalar additivity is not used to postulate a real vector space here. All computations are exact finite sets and integers. No inherited response carrier is discarded or redefined.

## L1 — Support of the full local profile

Removing c from V_i changes membership of precisely that identity in that indexed view. It changes a child-cover incidence only at p=parent(c); all other child families are identical. Because the joint endpoint keeps U fixed, the sets Ch_U(v) stay fixed throughout. For two events with distinct parents p,q, the change to t_p is independent of deleting f, and the change to t_q is independent of deleting e. Thus every D_v is zero. This does not assert h is additive: maximum is nonlinear.

The atomic local increments are 0 or 1: loss of an incidence cannot improve a minimum cover. If all old t-covers fail, another still-retaining view covering the deleted child can be added to any old minimum cover, giving a (t+1)-cover. Such a view exists by unchanged union. This recovers the inherited bound from its assumptions.

## L2 — Distinct-parent maximum interaction

Let H=h(V), and let u=h(V_e)-H and v=h(V_f)-H. They lie in {0,1}. The two changed profile components are disjoint, so h(V_ef)=max(H,h(V_e),h(V_f))=H+max(u,v). Therefore

    D_h=max(u,v)-u-v=-u*v.

A negative scalar diamond occurs exactly when both single deletions raise the old global maximum. The two local profile changes remain mutually independent; all D_v vanish. This is competition in the scalar maximum, not propagation between vertices.

## L3 — Same-parent threshold law

Let p be the common parent and (a,b,c,d) its values in states V,V_e,V_f,V_ef. All other profile entries are unchanged. Put B=max(1,those entries). Therefore the exact scalar diamond is

    D_h=max(B,d)-max(B,b)-max(B,c)+max(B,a).

Write b=a+x, c=a+y, d=a+z. Atomic monotonicity gives x,y in {0,1} and max(x,y)<=z<=min(x,y)+1. There are only six possible triples: (0,0,0),(0,0,1),(0,1,1),(1,0,1),(1,1,1),(1,1,2).

If B<=a, all four values exceed the threshold and D_h=D_p=z-x-y. If B=a+1, the first three scalar states all equal B; only the last triple reaches B+1, so D_h=1 only for (1,1,2), otherwise zero. If B>=a+2, all scalar states equal B and D_h=0. These cases exhaust the integer possibilities, including ties.

In particular, a positive scalar diamond CAN occur with every D_v=0: two unit rises in one local count only become globally visible after crossing another vertex's unchanged threshold. A nonzero local D_p can also be hidden by that threshold. When both local and scalar differences are nonzero, B<=a and their signs agree.

## L4 — Exact four-way diagnostic

Classify MAX_ONLY iff D_h!=0 and all D_v=0; LOCAL_TRANSMITTED iff D_h!=0 and some D_v!=0; LOCAL_MASKED iff D_h=0 and some D_v!=0; ZERO otherwise. L1–L3 derive the full classification without proposing any transport between the integer profile and response spaces. The names describe calculated evidence, not physical mechanisms.

This tests two universal implications independently: nonzero D_h need not imply nonzero D_v, and zero D_h need not imply all D_v zero. It leaves the .28 theorem about its scalar F intact; it limits extrapolation from F to the richer already-defined profile.

## L5 — Explicit admissible controls

Negative maximum-only: X has parent array (-1,0,0,1,1). Use V=({0,1,2},{0,1,3,4},{0,2},{0,1,4}); delete e=(0,2), f=(1,4). The union is preserved by the other views. Root and vertex 1 each initially have a one-view child cover. e changes only the root minimum from 1 to 2; f changes only vertex 1 from 1 to 2. The four h values are (1,2,2,2), D_h=-1, but every D_v=0.

Positive maximum-only: X=(-1,0,0,1,1,1). Use V=({0,1,3,4,5},{0,1,3},{0,1,4},{0,2}); delete e=(0,3), f=(0,4). Root minimum is constantly 2. Vertex 1 has counts (1,2,2,3), with zero local mixed difference. Scalar h is (2,2,2,3), giving D_h=+1. All four covers are actual prefix sets and their union is unchanged. This six-vertex control is outside the <=5 exhaustive extension.

Masked local dependence: X=(-1,0,0,1,1). Use V=({0,1,3,4},{0,1,3},{0,1,4},{0,2}); delete (0,3),(0,4). Root minimum remains 2; vertex 1 has (1,2,2,2), so D_1=-1 while all scalar h values are 2. Thus even an attribution-independent scalar interval can hide local attribution dependence.

Transmitted negative: the inherited .27 root/two-child example, views ({0,1},{0,2},{0,1,2}), deleting (2,1),(2,2), has h=(1,2,2,2), D_root=D_h=-1.

Transmitted positive: two repeated full views {0,1,2}, deleting (0,1),(1,2), have h=(1,1,1,2), D_root=D_h=+1. Repeated initial views are a separate admitted control, not included in the distinct-cover primary enumeration.

These are direct mathematical witnesses, not source-law choices. The program must reconstruct their minima and reject any incorrect recorded state.

## L6 — Why the previous bounded universe cannot expose this distinction

Two distinct branching vertices require at least four outgoing child edges and hence at least five vertices in a rooted tree. Thus with <=4 vertices there is at most one vertex with two or more children. All other local minima are at most one. If there is a branching vertex, h equals its tau on every full-union retained cover; otherwise h=1. Therefore on that size-restricted class D_h is precisely its only possibly nonzero D_v. Matching localization there is not a theorem for larger carriers.

The five- and six-vertex controls show where an inference beyond that domain fails. No numerical enumeration cutoff is promoted to physics.

## L7 — Naturality and scope

Parent-preserving bijections carry leaves, child sets and covering subfamilies bijectively. Indexed-view permutations transport the first event coordinate. Local profiles are permuted with vertices; h, D_h, the same/different-parent condition, background B and the four-way classification are unchanged. Storage order is irrelevant. No arbitrary winner in a tied maximum is selected.

The square still commutes as actual pruning; the oriented sum of state differences is zero. Neither nonzero D_h nor D_v constitutes curvature, holonomy, energy, or a physical-time law. This is foundational auditing of the existing diagnostic, not a newly supplied model.

**Time is pruning / ordered recoverability update.**
