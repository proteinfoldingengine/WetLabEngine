# Singleton anchors and mixed-floor reduction

Status: candidate analytical proof for independent review. Parent analytical head 721473f6d36a132715c82dc5a2b9b0a8819455b0. No implementation, numerical enumeration or scientific execution. All earlier accepted proofs are preserved.

## 1. Results and scope

Keep the fixed ordered palette P of size k, r ordered roots A_i with positive floors a_i, single-incidence moves, and hitting number tau. Fix exact-q endpoints with q>=3. Let p be the number of indices with a_i=1, called singleton-capable indices. Such roots need not initially be singletons.

**Theorem P (enough singleton anchors).** If p>=q, every pair of exact-q endpoints has a floor-safe path with tau in {q-1,q}, even if the other floors are arbitrarily large.

**Theorem Q (mixed floors 1 and 2).** If every a_i belongs to {1,2}, all exact-q endpoints are connected with tau in {q-1,q}, for arbitrary feasible r,k,q. Together with the earlier q=1,2 arguments this covers all feasible targets in this floor class.

These are structural reductions using a fixed hitting contribution from singleton roots. They do not establish general mixed/higher-floor connectivity when fewer than q indices have floor 1. Neither theorem assumes disjoint witnesses in the original endpoints or treats a root replacement as one primitive move.

We first build finite paths preserving only tau>=q-1, with exact-q endpoints, then invoke the accepted upper-excursion-removal theorem. Intermediate exact graph states may have tau>q; this is permitted only in that preliminary lower-guard construction.

## 2. Exact compaction and making anchors distinct

At an exact-q endpoint choose a minimum hitting set H of size q. In every root retain one anchor from H and delete excess labels down to its floor. All moves preserve floors. Deletion cannot lower tau and retained H prevents any increase, so this compaction is exact-q.

Each floor-1 root is now a singleton. Let T be the set of their labels; there may be duplicate singleton roots. If two such roots equal {x}, one may be reassigned to a label y outside T by

    {x} -> {x,y} -> {y}.

The other {x} root remains fixed, so removing the duplicate constraint does not change the hitting requirement of the old tuple. During the union step all old constraints are still enforced by the other roots. The final singleton adds a constraint on y. Consequently tau never decreases during this operation. Floors remain satisfied. The number of distinct singleton labels increases by one.

If p>=q, repeat until q distinct singleton labels exist. A duplicate is available whenever fewer than q labels appear among p>=q singleton roots; a new label exists because k>=q. Stop at q distinct labels even if p>q.

If p<q, repeat until all p singleton roots have distinct labels. Again duplicates exist until that point and k>=q>p leaves an available label. In both regimes the procedure is finite and all completed states have tau>=q; union steps do too. It does not assert that tau remains exactly q after anchor creation.

## 3. Proof when p>=q, including arbitrary other floors

Select one singleton root for each of q distinct anchor labels. Leave these q roots fixed and expand every other root to P, one incidence at a time. The q fixed singleton roots require q hitting labels throughout, so tau>=q. At the endpoint all other roots are P and tau=q. Every floor is at most k and is respected by expansion.

This endpoint is a protected exact-q tuple with q disjoint roots. Theorem J in PROTECTED_EXCHANGE.md connects any two such tuples on the same floor vector through the common protected normal form, with tau in {q-1,q}, even if their witness indices differ. Connect the original first endpoint to its protected tuple, use J, and reverse the second endpoint's normalization. The resulting finite path preserves tau>=q-1 and has exact-q endpoints. Theorem A removes upper excursions. This proves P without any restriction on the non-singleton floors.

## 4. Separate the anchored contribution when p<q

Assume now all floors are 1 or 2 and p<q. After Section 2, all p singleton roots are distinct and all other roots are pairs. The current hitting number q' is at least q. Permute the palette so the singleton roots, in their fixed index order, hold the first p labels of P. This is realizable through Lemma L's single-incidence label-transposition paths. Each completed transposition preserves q', and its intermediate states have tau>=q'-1>=q-1. The endpoint has a fixed canonical anchor set T independent of the original tuple.

Let R=P\T, n=|R|=k-p, and ell=q-p>=1. Pair roots touching T are redundant because every hitting set must contain every label of T. The other pair roots form a simple graph G on R, with duplicates allowed in the root representation. Therefore at this state

    tau = p + tau(G),   tau(G)>=ell.

In particular G has an edge, n>=2, and tau(G)<=n-1; hence m:=n-ell=k-q>=1. All these facts follow from feasibility, not extra restrictions.

Pick an edge e_0 of G. Keep all pair roots contained in R fixed for the moment. Replace every redundant pair root touching T by e_0 through its union with e_0. Every hitting set consisting of T and a minimum cover of G hits both the old redundant pair and e_0, hence their union. Conversely, the fixed singleton roots and the fixed graph G still require p+tau(G) labels. Thus this replacement stays exactly at the current q', with all floors satisfied. At completion all h=r-p pair slots are entirely in R and represent G, possibly with additional duplicates.

From now until final canonicalization keep the singleton roots fixed. All pair-root intermediate supports will stay inside R. Consequently the hitting number is always p plus the hitting number of the residual root tuple, including during union-based primitive moves. This exact additivity is the anchor invariant.

## 5. Residual graph normalization with a lower target

The residual graph may have cover number greater than ell. The construction in Sections 3-6 of FLOOR_TWO_CONNECTIVITY.md applies with any starting graph of cover number at least ell, provided ell>=2. We spell out why this mild strengthening is valid rather than assuming exactness or the earlier q>=3 threshold.

- Its star-edit guard is tau(G-u)>=tau(G)-1>=ell-1. When the new star is empty, a surviving edge is available because ell-1>=1. This is the only nonempty-surviving-edge requirement that previously used q>=3; the weaker bound suffices. Existing slots and duplicate assignments are unchanged.
- Every completed clone does not increase independence number, so cover number stays at least ell. Degree-nonincreasing edits and whole-class termination are unchanged.
- Symmetrization reaches t clique components with t<=n-ell=m. Splitting until m components keeps cover number at least ell. Balancing keeps exactly m components and cover number ell, with the same strictly decreasing potential.
- Duplicate normalization and symmetry exchanges then produce the canonical balanced clique tuple on R in the h pair slots. The label and root swaps apply at exact ell and give residual guard ell-1. For ell=2 their union arguments still apply without modification: they require only positive nonempty roots and the one-unit hitting bound.

Thus for ell>=2 there is a finite residual lower-guard path to one tuple determined by R,h,ell and the supplied orders. Its distinct-edge count does not exceed h because it never increases during the graph normalization; final duplicate normalization fills all h slots. Exact additivity gives total tau>=p+ell-1=q-1, with total tau=q at the destination. We do not apply upper-excursion removal separately to this residual path, whose starting cover number may exceed ell.

If ell=1, an even simpler route suffices. Select the first two labels of R and let e_0 be their pair. Replace every residual root by e_0 through its union with e_0. All residual supports stay in R, nonempty and of size at least 2; h>0 since G has an edge. Their hitting number is at least 1 throughout. Therefore the total hitting number stays at least p+1=q, and the destination has exactly q. This avoids any zero-edge special case in graph symmetrization. The destination is canonical and uses the same h slots.

## 6. Connect the original endpoints

When p<q, each exact endpoint has now reached a common ordered tuple: the same p singleton roots contain the same canonical anchor labels, and the h remaining root slots contain the same canonical residual tuple. Root swaps used for residual ordering involve only floor-2 slots; singleton slots stay fixed.

Concatenate the first endpoint's construction with the reverse of the second. All primitive states preserve floors and tau>=q-1; both endpoints have tau=q. Apply Theorem A to this full path to remove upper excursions, obtaining tau in {q-1,q}.

This proves Q for p<q. The p>=q case follows from P, and p=0 recovers the previous all-floor-two result. The proof does not need a count-based numerical campaign or progression through individual arities.

## 7. Native meaning, limitations and review obligations

The new mechanism is a forced-label reduction. Distinct singleton roots contribute a fixed p hitting units; pair roots intersecting their labels are redundant; the remaining problem is a graph on the complementary palette. When q singleton anchors can be established, all other roots can instead be expanded away while those anchors preserve the required lower bound, even if the other floors exceed 2.

The unresolved general case is now a floor vector containing values at least 3, with fewer than q singleton-capable indices, outside the other earlier scoped results. After anchor reduction such residual roots need not be pairs. The graph symmetrization and fixed-slot degree argument have not been extended to these hyperedges. This is a limit of the current proof, not a root disconnection or native barrier claim.

Conditional native lifting remains the preceding theorem's sufficient statement with the same child-interface assumptions. No numerical execution, implementation, certification, efficiency bound or physical interpretation is claimed. Later execution would require a prospective protocol for duplicate-singleton reassignment, anchor additivity, redundant-root replacement and residual-target edge cases, as well as the already identified proof mechanisms.

Independent review must check exact compaction, monotonicity while separating duplicate anchors, the p>=q route with arbitrary other floors, canonical anchor relabeling, additivity during every primitive residual move, residual targets ell=1 and ell=2, fixed slot counts, and the single final use of upper-excursion removal with exact-q original endpoints.
