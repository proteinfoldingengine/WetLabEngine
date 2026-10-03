# Distributed exchange of two label roles

Status: candidate analytical theorem for independent review. Parent: 66a2d75c1b34809e458c2baf7c44f18345735b03. Native admissibility and certified baseline remain as in SCOPE.md. No implementation or numerical execution.

## 1. A class of configurations with fixed background incidences

Fix two distinct existing labels u,v and put Q=P minus {u,v}. For every labelled root i, fix a background support D_i subset Q and fix whether that root is active. Inactive roots equal D_i. Active roots equal D_i union S_i for some nonempty S_i subset {u,v}. Only configurations meeting all original positive floors a_i are admissible. Background sets may be empty; native root supports may not.

Thus the two role labels occur in the same union of root slots throughout this class, but either label's individual membership may vary arbitrarily. Roots may change from u-only to v-only or to both roles, subject to their own floors. No extra slot, label, simultaneous primitive or imposed root permutation is used. Call this a two-label fiber, with the above definition fixed.

Let F be the family of inactive supports and let g=tau(F). Let lambda_0=tau({D_i: all i}), computed on Q. These are auxiliary hitting problems. An empty family has transversal zero; a family containing an empty support has transversal +infinity. The latter convention concerns auxiliary backgrounds, not native empty roots.

For a particular admissible tuple X in the fiber, define

    lambda_u(X)=tau({D_i: u is absent from X_i}),
    lambda_v(X)=tau({D_i: v is absent from X_i}),

again on Q.

## 2. Exact endpoint formula and renewal condition

**Theorem T1.** Every admissible X satisfies

    tau(X)=min(lambda_0, 1+lambda_u(X), 1+lambda_v(X), 2+g).

Partition hitting sets by their intersection with {u,v}. Avoiding both imposes all background supports, giving lambda_0. Using u but not v imposes exactly the backgrounds of roots lacking u, giving 1+lambda_u. The v case is symmetric. Using both leaves only inactive roots, giving 2+g. These four cases exhaust the hitting sets and attain their stated finite minima. Infinite terms denote impossible cases.

Suppose the fiber contains an exact-q tuple A, q>=3. Then lambda_0>=q, g>=q-2, and g<=q, the last inequality because F is a subfamily of A. For any admissible X in the same fiber,

    tau(X)>=q iff lambda_u(X)>=q-1 and lambda_v(X)>=q-1.

Exact equality tau(X)=q additionally requires at least one of

    lambda_0=q; lambda_u(X)=q-1; lambda_v(X)=q-1; g=q-2.

These are exact conditions, not an assumption that arbitrary role reassignment renews exactness. Constants lambda_0 and g are unchanged in the fiber; the two single-role residual problems carry the variable renewal obligation.

If g=q-2, the inequality conditions alone give exactness, because the term 2+g already equals q. In this case they have a useful structural interpretation. For every minimum transversal H of F, of size q-2, define

    E(H)={active i: H misses D_i}.

Every E(H) must contain at least one u-only root AND at least one v-only root. Roots carrying both roles do not supply either pure-role witness. Indeed H together with u hits X exactly when all v-only roots have backgrounds met by H; the symmetric statement holds for H together with v. Inactive roots are already hit by H. Since no smaller set hits F, these tests exclude all residual covers of size at most q-2. This proves equivalence to the two lambda inequalities, including empty backgrounds and repeated supports.

## 3. A common saturation with at most one unit of loss

Define S, the common saturated tuple, by giving BOTH u and v to every active root and retaining every background and every inactive root. Saturation is admissible because it only adds incidences to any admissible fiber member.

**Theorem T2.** Any two exact-q endpoints A,C in the same two-label fiber are connected by a finite primitive path with tau in {q-1,q}.

For S the exact formula reduces to

    tau(S)=min(lambda_0,1+g).

Both role-present cases have residual family F; the term 2+g cannot improve 1+g. The exact-q source gives lambda_0>=q and g>=q-2, so tau(S)>=q-1. S contains A, hence tau(S)<=q.

Expand A to S one incidence at a time, then contract S to C. Every expansion state contains A and every contraction state contains C, giving the upper bound q. Every intermediate tuple is contained in S, giving the lower bound tau(S)>=q-1. Floors hold because each state contains its corresponding endpoint support at every slot. Each change is a single incidence; saturation is an intermediate tuple, not a simultaneous native move. Finitely many missing/excess incidences are processed, giving finite termination and the exact labelled destination.

The protection can span arbitrarily many active roots. It is supplied by the fixed background/occupancy structure and the two-label hitting-set formula, not by keeping all but a fixed number of roots at their global endpoint supports.

This extends the accepted global label-transposition mechanism: a transposition is a special case, but the individual roots need not all swap roles consistently. T2 may change root sizes and incidence overlap types. It does not assert connectivity between different fibers without further work.

## 4. Safe iteration and its remaining global obligation

A finite sequence of such exchanges with exact-q completed tuples concatenates directly in the unit band. T1 supplies an exact renewal test at every completion, even if the selected label pair, fixed backgrounds and active slots change between exchanges.

More generally, if every completed tuple retains tau>=q, the saturation argument in each current fiber retains tau>=q-1 throughout that exchange. If the entire finite sequence has exact-q endpoints, the accepted maximum-layer-removal theorem clips any upper excursions. No global sequence is asserted to exist merely because individual moves are safe.

Each specified exchange has finitely many eligible additions/deletions. A supplied finite sequence terminates. To turn this into a universal algorithm one must prove existence of an eligible exchange that makes well-founded progress until the target is reached. T1 is a guard test, not such an existence or termination theorem for choosing exchanges.

Native lifting remains conditional on the previously accepted child interfaces and fixed-root clearance. No implementation certification, efficiency, originality or physical claim is made.
