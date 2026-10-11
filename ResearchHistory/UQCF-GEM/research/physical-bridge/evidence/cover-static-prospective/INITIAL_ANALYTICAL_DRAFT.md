# Cover-aware static reserve on general pair-root carriers

Status: prospective analytical candidate, OPEN pending independent analytical review, prospective publication, declared verification and scientific closeout. No new scientific enumeration has been performed. Parent: de41f3857b4c81690526fd6c0381bae07d0c0270, the completed nonuniform five-type checkpoint.

## Intent and native domain

Extend static reserve availability beyond the complete five-type root graph without promoting endpoint existence to reachability or importing a native observer. Retain original positive floors, original palette and original-footprint domination. No geometry, new outcome rule, full-state sensor, acknowledgment or commitment premise is derived.

Let H=(V,E) be a finite simple root graph with no isolated vertices. Roots are the edges of H; type v has footprint M_v consisting of the roots incident to v. Source type v has a_v>=1 distinct original labels, each with footprint M_v. Let A=sum_v a_v and let q be the minimum vertex-cover cardinality of H. Restrict the protected application to q in {3,4}. These source stars need not all be inclusion-maximal; domination by an original footprint and domination by an original maximal footprint are equivalent. No source type is missing.

Fix a saturation subgraph G=(V,E_G), E_G subset E. The ORIGINAL floor at root uv is a_u+a_v when uv is in E_G and 1 otherwise. A static admissible core uses the same A labelled palette, permits empty footprints, has each current footprint contained in some ORIGINAL M_v, meets every original floor, and has core hitting number at most q. For q=4 this is the inherited upper-four static safety domain. For q=3 the upper bound q is an explicit tighter endpoint constraint; the result does not classify all endpoints of the looser upper-four domain.

A static reserve means at least one original palette label is empty. It means neither a native path nor an observer-accessible record. The source hitting number is q. Let S={v:a_v=1}. Let C be any specified minimum vertex cover of H, |C|=q. Choose any one actual ORIGINAL label at each type in C as its anchor; these q label footprints must remain identical at the static endpoint. This is an endpoint preservation requirement, not a statement about an intervening path.

## Theorem

For each prescribed C and each such actual anchor choice, an anchor-preserving static reserve exists if and only if there is a nonempty independent set I in G such that

    |I| > |N_G(I)|    and    I intersect S intersect C = empty.

Consequently an unrestricted static reserve exists if and only if such a pair (C,I) exists for at least one minimum cover C. In particular, whenever any static reserve exists, some static reserve preserves an actual original minimum cover. The same C works for EVERY choice of one original anchor label per type in C. This does not assert that every C works, or that a reserve can be reached with those labels unchanged.

The witness has explicit counts

    n_v = a_v - 1[v in I] + 1[v in N_G(I)].

It saves |I|-|N_G(I)| labels. Thus any existence witness, however large its count changes, implies a unit-per-type decrease/increase witness. Existence depends on the profile only through the singleton set S; actual multiplicities greater than one do not change the answer, although original floors and other quantitative questions do change.

## Proof for prescribed anchors

Necessity. Take a static endpoint with the prescribed anchors and at least one empty label. Expand each nonempty current footprint to some containing original star; choose the given star for each anchor. Expanding preserves floors and the actual anchor cover: those unchanged q anchors already cover all roots. Empty labels remain empty. Let n_v be the resulting type counts. Then sum n_v<=A-1, n_v>=1 for v in C, and n_u+n_v>=a_u+a_v on each saturated edge uv.

Put d_v=max(a_v-n_v,0), p_v=max(n_v-a_v,0). Since sum d_v>sum p_v, the finite integer layer identities sum d_v=sum_{h>=1}|{v:d_v>=h}| and sum p_v=sum_{h>=1}|{v:p_v>=h}| imply a level h with |D_h|>|P_h|. For any saturated edge from v in D_h, its other endpoint w must have n_w-a_w>=a_v-n_v>=h. Hence D_h is independent in G and N_G(D_h) is contained in P_h. Thus I=D_h has |I|>|N_G(I)|. If v is in S intersect C, n_v>=1=a_v, so it cannot be in I. This proves necessity without presupposing a bound on the endpoint's count changes.

Sufficiency. Given (C,I), independence gives I disjoint from N_G(I), so the displayed n_v are nonnegative integers. If v is in C and I, eligibility ensures a_v>=2, hence n_v>=1. All other types in C also retain at least one label. On saturated edge uv, a decreased endpoint has an increased neighbor; no saturated edge has two decreased endpoints. Thus n_u+n_v>=a_u+a_v. Each nonsaturated root has an endpoint in C, whose retained anchor alone meets its floor 1. These anchors cover every root, giving hitting number at most q. Domination and original palette are respected by assigning active labels to the indicated stars.

For the actual assignment, leave each chosen anchor unchanged. There are n_v-1 remaining positions at every v in C and n_v positions elsewhere, totalling sum n_v-q <= A-q-1. Assign that many distinct original non-anchor labels to these positions; leave the rest empty. No fresh label is introduced and no label is assigned twice. The particular original identity selected as each anchor is immaterial. This realizes the claimed endpoint for every anchor choice.

## Proof of unrestricted equivalence

Start from an arbitrary static reserve with a cover of at most q CURRENT labels. Expand every nonempty footprint to a containing original star. The selected covering labels still cover all roots after expansion. The set C of their star types is a vertex cover of H of size at most q; minimality of q forces exactly q distinct types. Therefore n_v>=1 on this minimum cover C. The same deficit-level argument yields an eligible (C,I), and the constructive direction replaces the arbitrary endpoint by one preserving ORIGINAL anchors of that C. This replacement is static; no native route from the source or between endpoints is implied.

## Sharp upper-cover control beyond five types

Let H=K6 with only edge {4,5} removed, source a_v=1 at all six types, and G be H with all edges incident to type 0 removed. The unique independent pair in H is {4,5}; hence its unique minimum cover is C={0,1,2,3}, q=4. Type 0 is isolated in G but belongs to C.

The only deficient independent set in G is {0}. To verify this directly: on vertices 1..5 the only nontrivial independent pair is {4,5}, with neighborhood {1,2,3}. A single remaining vertex has at least three neighbors; adjoining isolated 0 does not make either of those sets deficient (the pair plus 0 has sizes 3 and 3). Thus {0} is the only deficit, and its singleton type lies in C, so the theorem excludes a static reserve.

Deleting the type-0 label is a floor-valid, original-dominated endpoint, but all five remaining types are needed to cover roots {0,w}, w=1..5. Its hitting number is 5 and it is inadmissible. This is a direct counterexample to generalizing “isolated saturated type guarantees a static reserve” or using deficiency without the cover condition. It is not a search-derived claim.

With a_0>=2 instead, the same I={0} is eligible and deletion of one type-0 label leaves an original type-0 anchor. With G isolating 4 or 5 instead, a singleton deletion is eligible because these types lie outside C. These are algebraic positive controls, not executed experiments.

## Reduction and boundaries

For H=K5, minimum covers omit exactly one vertex, so some C avoids I intersect S exactly when I contains at most one singleton. The theorem therefore recovers the closed five-type STATIC criterion, including isolates through I={v}; it does not re-prove that family's reachability/cost theorem. If all a_v>=2, the cover condition is vacuous for every C, and existence reduces to an independent-set deficiency in G.

Changing the root graph changes both the available covers and the meaning of an isolated saturated type. The five-type reachability criterion “static and minimum degree<=1,” four-anchor PATH theorem and costs 4/8/13 are not generalized here. Arbitrary root hypergraphs with roots supported by more than two source types, missing source types, exact labelled exchange/restoration, committed progress, native observation/access/retained output, broad C3 and general C4 remain OPEN.

The preserved C3 source screens require a justified native input, carrier/initial correlation, action connection and accessible retained output. This endpoint theorem supplies none of those objects. Path A remains active; Path B closed. No physical derivation or full-stack closure is claimed.
