# A sufficient structural condition for unit retained barriers

Status: exploratory mathematical proof independently reviewed as sound; numbered-stage certification remains pending. This argument was developed after v16.38; it is not retroactively called preregistered. No new numerical science has been executed for it.

## Definitions

Let T be a finite rooted tree and K={1,...,k}, k>=1, the indexed views. Write S_v for the nonempty set of views containing vertex v. Admissibility is exactly S_root=K and empty != S_w subseteq S_v on each parent-child edge v->w. A legal move adds or removes one label at one nonroot vertex, preserving these conditions.

For a nonleaf v, q_v is the transversal number of the family (S_w: w a child of v): the minimum size of H subseteq K meeting every S_w. For a leaf q_v=0. This is exactly the minimum number of views covering the children. Fix an attainable target q and two states X,Z with that profile. Primary barriers independently minimize the maximum L1, Linfinity and support-size deviation from q along legal paths.

Call v active when q_v>=2, and saturated when q_v=k>=2. Let A be the active vertices and let H be the root together with every ancestor of every vertex in A, including A itself. Descendants include the vertex itself unless stated otherwise.

**Saturation condition (SC).** For every edge u->w with u,w in H and u active, the subtree rooted at w contains a saturated vertex.

## Theorem

If SC holds, any two states with target profile q can be joined by a legal path on which at most one q-coordinate differs from its target, and its absolute difference is at most one. Consequently, for endpoints in different components of the exact q-fiber,

    (B1, Binf, Bs) = (1,1,1), and LEX_BARRIER = (1,1,1).

This is a sufficient condition, not an asserted characterization of all unit-barrier profiles.

## Lemma 1: saturation forces full support

At a nonleaf v, S_v itself meets every child support, so q_v<=|S_v|<=k. Therefore q_v=k implies S_v=K. By nesting, every ancestor of a saturated vertex also has support K, in every state of the target fiber.

## Lemma 2: local transversal reconfiguration has width one

Consider m labeled nonempty subsets of K, with any additional fixed sets equal to K. Suppose two configurations have the same transversal number r>=1. They can be joined by single-label additions/removals in the variable sets, never emptying a set, with transversal number always within [r-1,r+1]. If m=0 there is nothing to change; the only attainable positive transversal number is 1, when a fixed K set is present. The completely empty family has transversal number 0 and is handled separately as a leaf.

Proof. Choose a minimum transversal C of size r in the first configuration. In each variable set retain one chosen element of C and delete the other elements one at a time. Deletion cannot lower the transversal number; C remains a transversal throughout, so the number remains r. The resulting singleton sets use exactly r distinct labels: their number of distinct labels is their transversal number; fixed K sets do not change it when m>0. Do the same independently for the second endpoint, obtaining singleton assignments f,g with r used labels each.

First align the used-label sets. For b used by f but not by g, and a used by g but not by f, replace every occurrence of b by a, one variable at a time. Realize b->a as {b}->{a,b}->{a}. During this global replacement, singleton support uses r or r+1 labels; during a doubleton intermediate the transversal number is r or r+1. If the last b occurrence is the doubleton, a or b can cover that set and the number is r. Repeat until both assignments use the same r-label set C.

Now fix incorrect positions to their g-label, never changing a correct position. When all r labels are present, choose any incorrect position. When exactly r-1 labels are present, choose a position whose g-label is the unique missing label a; this position is necessarily incorrect. Recolor it to a. At every singleton assignment at least r-1 labels remain: in the latter case one missing label is introduced while at most one other label disappears. Each recoloring fixes a position, hence terminates at g.

During a doubleton intermediate of this second phase, when r labels were present the transversal number is at least r-1. When r-1 labels were present the new label was missing: if the old label was unique, the other r-2 forced singleton labels plus the doubleton require r-1 labels; if it was not unique, the existing r-1 singleton labels suffice and are necessary. The transversal number never exceeds r. For r=1 the same-palette phase is already finished. Reversing the endpoint shrinkage completes the proof.

## Lemma 3: normalize the active skeleton at zero cost

Under SC, every target-fiber state can be transformed, without changing q, to one with S_v=K for all v in H.

Process H from the root downward. A vertex w whose parent u is active already has S_w=K by SC and Lemma 1. At any other nonroot w in H, its parent u has q_u=1 (u has a child, hence is not a leaf). Add missing labels to S_w one at a time, after its parent has become K. This is legal: it respects the parent bound and only enlarges the support above existing children. Changing S_w affects only q_u, not any other q-coordinate. Adding labels cannot increase q_u, and a nonleaf has q_u>=1; therefore q_u stays 1. Root support was K from the outset.

## Lemma 4: normalize and operate the attached subtrees

Every component below H is a subtree with no active vertex, so all its nonleaf targets are 1. Let its root be w and its present root support be S. Keeping S_w fixed, add missing labels from S to descendants in ancestor-first order until every support in that subtree equals S. Nesting guarantees every old support lies in S. All affected q-coordinates start at 1, can only decrease, and remain at least 1; leaf coordinates remain 0. Thus normalization preserves the entire target profile, including the parent of w.

A single-label change S->S' at the root of such a normalized subtree, with both sets nonempty, can be implemented on the entire subtree while all its internal q-values remain 1. For addition, add the label in ancestor-first order. For removal, remove it in descendant-first order. Legality follows from nesting. At every intermediate state, all child supports share a label in the old S (addition) or in the nonempty S' (removal), so the internal q-values stay 1. Only the q-coordinate of w's parent in H can change. The subtree is normalized again at completion.

## Proof of the theorem

Apply Lemmas 3 and 4 separately to X and Z, obtaining normalized endpoints at zero cost. Keep all H supports fixed at K. For each vertex u in H, its children in H have fixed support K; its children outside H root distinct normalized subtrees whose nonempty root supports are the variable sets of Lemma 2. If u has no children its q is fixed at zero. Otherwise both endpoint configurations at u have transversal number q_u>=1.

Process the vertices u of H one at a time. Apply Lemma 2 to change their attached root supports from the normalized X values to the normalized Z values. Lift every local move by Lemma 4. The attached subtrees for different u are disjoint, and no support in H changes. Therefore only the currently processed coordinate q_u can deviate, by at most one. Finish by reversing the zero-cost normalization of Z.

This constructs a single path with all three maxima at most one. Distinct exact-fiber components cannot be connected at zero cost for any primary objective. Costs are nonnegative integers, hence each primary barrier is at least one. The constructed joint path also establishes the claimed lexicographic value, without identifying independent minima with lex optimization in general.

## Consequences

1. **All two-view constructions have unit barriers between distinct equal-q components, at every finite tree size.** For k=2 every active vertex is saturated. Any subtree required in SC contains an active vertex by definition of H, hence contains a saturated vertex. For k=1 there is only one admissible state, so no such distinct components exist.
2. **If the active vertices form an antichain, unit barriers follow for any k.** There is no edge in H from an active vertex toward another active descendant, so SC is vacuous. In particular, one-active-vertex profiles and rooted stars are covered.
3. **If every active vertex has q=k, unit barriers follow.** More generally it suffices that every descendant-maximal active vertex is saturated: every subtree containing an active vertex then contains a saturated one.
4. **Necessary obstruction for a nonunit example between distinct exact-fiber components.** It must violate SC: some active u has a child w whose subtree contains an active vertex but contains no saturated vertex. In that subtree, a descendant-maximal active v has 2<=q_v<=k-1. Thus k>=3 and nested active branching are necessary. This is not sufficient for nonunit behavior, and no witness or minimality claim is made.

There is also an endpoint-sensitive strengthening: Lemma 3 works without SC whenever both endpoints already have S_w=K on every H-edge whose parent is active. Therefore a nonunit endpoint pair must have at least one such edge with a proper support S_w subsetneq K in at least one endpoint. For that edge, the subtree has no saturated vertex by Lemma 1. This identifies a restricted view palette feeding another active subtree as the remaining obstruction to this proof.

## Limits and next falsification target

SC failure only identifies where the normalization proof can fail. It does not show that widening a restricted support forces a nonunit excursion, nor that a different path cannot avoid one. A targeted next experiment should inspect these nested, unsaturated support restrictions and distinguish whether their repair can always be serialized into one-coordinate unit excursions. An undirected seven-vertex enumeration is not implied.

This is an ordinary constructive mathematical argument, not a proof-assistant formalization, physical derivation, or completed numbered-stage certification. Independent proof review and any subsequent preregistered numerical validation must be recorded separately.
