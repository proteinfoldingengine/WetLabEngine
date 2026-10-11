# Independent analytical review — cover-aware static reserve

Review date: 2026-10-11 UTC. Parent checkpoint supplied for scope: `de41f3857b4c81690526fd6c0381bae07d0c0270`.

## Verdict

ACCEPT the prospective mathematical theorem as stated in `RESULT.md`, within its explicit endpoint domain. No blocking mathematical correction or counterexample to that statement was found. This is an analytical acceptance, not computational verification, publication approval, or scientific closeout.

I read `RESULT.md` and `progress.md`, and compared the static argument and boundary statements with `nonuniform_reserve/RESULT.md` and `private_cover/RESULT.md`. The review used proof reasoning and the small hand derivations below. No scientific enumeration, implementation, native-path search, GitHub write, or new verification campaign was performed. The supplied parent commit identity was not independently audited here.

## Proof audit

1. **Source and domination.** Since every type has at least one original label, covers by original stars correspond to vertex covers of H, so the source hitting number is q. This remains true when distinct vertices have equal stars or some stars are nonmaximal: the image of any selected labels is still a vertex cover, and repeated types cannot improve its cardinality. In the finite family, every original star is contained in an inclusion-maximal original star, so the two stated domination predicates are equivalent. The proof correctly retains all original types, rather than requiring anchors to be maximal.

2. **Expansion and prescribed anchors.** Each nonempty endpoint footprint can be assigned one containing original star. A prescribed anchor is assigned its own original star, so expansion leaves that actual label unchanged. Every original floor is monotone under expansion; empty labels stay empty. The q actual anchors continue covering every root, hence expansion also respects the upper-q gate. It is unnecessary and would be incorrect to assume that arbitrary expansion preserves an arbitrary upper-cover constraint without tracking a covering label set; this proof does track one.

3. **Unrestricted expansion and choice of C.** Select a cover by at most q current labels before expansion. After assigning containing stars, their distinct types form a vertex cover of H of size at most q. Minimality of q forces q distinct types and a minimum cover C. Thus n_v >= 1 on C. This covers duplicate containers, nonmaximal original stars, and endpoints whose original covering labels were not themselves original anchors. The subsequent construction produces a potentially different endpoint preserving original anchors; it does not retroactively identify those anchors with the covering labels of the first endpoint.

4. **Deficit-level necessity.** With d_v = max(a_v-n_v,0) and p_v = max(n_v-a_v,0), the vacancy gives sum d_v - sum p_v = A-sum n_v >= 1. Finite integer layer sums therefore yield some positive integer h with |D_h| > |P_h|. A saturated edge from v in D_h forces its other endpoint w to have surplus at least d_v >= h. Consequently D_h is independent, its open neighborhood is contained in P_h, and D_h is nonempty and deficient. If a_v = 1 and v belongs to C, the retained occupant gives d_v = 0. This proves precisely the claimed eligibility condition, including arbitrarily large initial endpoint deviations. No uniform-multiplicity assumption is used.

5. **Unit redistribution sufficiency.** For independent I, the open neighborhood N_G(I) is disjoint from I. Decreasing each I-count by one and increasing each neighborhood count by one keeps all counts nonnegative. A decreased type in C has multiplicity at least two, so every C-type retains an occupant. Every saturated loss is compensated at its opposite endpoint; all other saturated edges have no loss. Every unsaturated root meets C and therefore keeps its floor of one through a retained anchor. These same anchors enforce the upper-q gate. The total active count is exactly A-|I|+|N_G(I)|, so the construction saves exactly the stated positive deficiency.

6. **Actual labels and palette.** The q selected anchors are distinct actual labels. Once they are fixed, the remaining required positions total sum n_v-q, a nonnegative integer at most A-q-1. They can be filled injectively from the A-q original non-anchor labels, leaving at least one empty. A label may receive a star of a different original type because the stated admissibility rule is domination by some original footprint, not by that label's own footprint. That global interpretation is essential and is already explicit in the setting. The proof therefore supports every choice of original anchor identities for the same C.

7. **Profile dependence.** For fixed H and G, minimum covers and independent-set deficiencies are independent of a. The only multiplicity information in eligibility is membership in S={v:a_v=1}. Hence both prescribed-C and unrestricted existence depend only on S throughout the all-positive integer domain. This is an existence statement; it does not assert that every feasible endpoint is a unit redistribution, or that optimal reserve size or native cost depends only on S.

## Hand audit of the six-type rejecting control

For H=K6 minus edge 45, the sole independent pair is {4,5}; no independent triple exists. Thus the unique maximum independent set is {4,5}, and its complement C={0,1,2,3} is the unique minimum vertex cover, of size four.

When G removes all edges incident to 0, its nonempty independent sets consist of {0}, a singleton from {1,...,5}, the pair {4,5}, or one of the latter sets with 0 adjoined. Vertices 1,2,3 have four neighbors in G; vertices 4,5 have three. The pair {4,5} has neighborhood {1,2,3}. Adding isolated 0 leaves these neighborhood sizes unchanged. Thus neither a singleton, a singleton plus 0, the pair, nor the pair plus 0 is deficient; the last has sizes three and three. Exactly {0} is deficient.

With all multiplicities one, that unique witness meets S intersect C, so no admissible static reserve exists. Deleting the original type-0 label leaves every saturated root supported twice and every root 0w supported once. It satisfies the original floors and domination. The five roots 0w are each supported by their respective remaining type-w label alone, so all five remaining labels are indispensable and the endpoint hitting number is exactly five. This verifies the claimed rejection and the failure of the unrestricted isolate shortcut.

For a_0 >= 2, I={0} is eligible and removing one original type-0 label keeps a type-0 anchor. Isolating 4 or 5 instead permits deleting that singleton label while preserving C. Both positive controls follow directly without computation.

## Scope qualifications and optional strengthening

No theorem correction is necessary. Retain the following qualifications in any frozen or published statement:

- For q=3, the domain has upper bound three. It does not classify all endpoints in the inherited upper-four domain. For q=4 those bounds coincide.
- Anchor immutability is an endpoint requirement here. Neither the unit count formula nor assigning actual labels constructs a native route, preserves anchors along a route, gives edit costs, or solves a prescribed-label target problem.
- Original floors, original palette, all-positive multiplicities, pair-supported roots, and global original-footprint domination are part of the theorem, not conclusions to be weakened silently.
- The unrestricted result is existential in C. It neither says every minimum cover works nor preserves a predetermined original minimum cover at an arbitrary given endpoint.
- No C3 information origin, native observer, carrier correlation, access/retention mechanism, physical derivation, general C4 closure, or transfer of the private-maxima path theorem follows.

An optional small control makes the q=3 qualification concrete: take H=K5 minus edge 34, all multiplicities one, and G obtained by isolating vertex 0. The unique minimum cover is C={0,1,2}. An eligible I would have to lie in {3,4}; either singleton has two neighbors, while {3,4} has exactly two neighbors. Hence no eligible deficient I exists and the upper-three theorem excludes a reserve. Nevertheless, deleting type 0 meets all original floors and has hitting number four, because the four roots 0w each require their corresponding remaining label. Thus the looser upper-four domain does admit a reserve. This is a hand-derived illustration, not a new required computational scope.

For H=K5 itself, a minimum cover omits exactly one vertex, so a suitable C exists precisely when an independent deficient I contains at most one singleton type. This matches the parent static criterion; an isolated singleton is included via its one-vertex witness. None of the parent reachability or cost conclusions has been used in proving the general-root statement.

## Review disposition

The prospective theorem is suitable for scope freeze on the stated analytical basis. Computational checks, if subsequently authorized and declared, would corroborate finite instances rather than establish the all-positive, arbitrary-finite-H theorem. All later execution, publication, and closeout gates remain separate and unassessed by this review.

## Requested strengthening: exact inherited upper-four domain

After the preceding audit, the author requested analytical assessment of replacing the upper-q endpoint bound by four and permitting C to be any vertex cover of H with |C| <= 4. I ACCEPT this strengthening. It requires no enumeration and removes the need to impose the tighter upper-three endpoint domain when the source has q=3.

The precise strengthened statement is: retain finite simple H without isolates, all a_v >= 1, source vertex-cover number q in {3,4}, original saturated/unsaturated floors and the original palette/domination rules. A static endpoint is admissible when its hitting number is at most four. For any specified vertex cover C with |C| <= 4 and any one actual original anchor per C-type, an anchor-preserving static reserve exists if and only if some nonempty independent I in G satisfies |I| > |N_G(I)| and I intersect S intersect C is empty. An unrestricted upper-four static reserve exists if and only if at least one such pair (C,I) exists. Every affirmative instance consequently has an endpoint preserving an actual original cover of at most four labels, although that cover need not be minimum when q=3.

For fixed C, the proof above applies verbatim except that the number of anchors and the palette subtraction are |C|, not q: the remaining positions total sum n_v-|C| <= A-|C|-1. These anchors ensure the upper-four gate. The deficit proof uses only n_v >= 1 on C, not minimality of C.

For unrestricted necessity, select at most four current labels covering all roots and expand all nonempty footprints to containing original stars. Their set of distinct star types is a vertex cover C with |C| <= 4, and each C-type is occupied. The selected covering labels need not have distinct types; passing to the set of types is sufficient. No minimum-cover argument is needed. The layer proof then supplies eligible I and the construction realizes original anchors for that C. Unit redistribution and dependence only on singleton membership remain unchanged.

The six-type rejecting control is unaffected: q=4 forces every cover of size at most four to be its unique minimum cover. For H=K5, all covers of size at most four have size four, so the five-type reduction is also unchanged. In contrast, the q=3 hand example above now supplies the eligible pair C={1,2,3,4}, I={0}; the deletion endpoint has hitting number four as permitted. It also proves that the stronger upper-four theorem must not retain the assertion that every affirmative instance has a reserve preserving an original *minimum* cover. In that example the sole minimum cover is {0,1,2}, for which no eligible witness exists.

Necessary editorial changes if adopting this extension: state endpoint upper-four throughout; quantify over vertex covers C of size at most four; replace q by |C| only where counting selected anchors; remove the unrestricted minimality/distinct-type conclusion; and replace the unrestricted minimum-cover-preservation conclusion by preservation of some original cover of size at most four. The original fixed-minimum-C theorem remains a valid special case. The source restriction q in {3,4} and all endpoint-versus-path and native-premise boundaries remain intact.
