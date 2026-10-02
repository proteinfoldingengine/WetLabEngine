# Changing overlap structure: all-floor-two connectivity

Status: candidate analytical theorem for independent review. Parent analytical head 59676cb889d1ec044e36873527ea256092a9efa9. No implementation, numerical enumeration or scientific execution. Earlier accepted proof files remain unchanged.

## 1. Statement and mechanism

Keep the width-floor carrier, fixed ordered palette P of size k, r ordered nonempty roots, and single-incidence primitive moves. Here every floor a_i is 2. Let tau be the minimum hitting-set size and fix exact-q endpoints with q>=3.

**Theorem O.** For arbitrary feasible r,k,q with all floors equal to 2, any two exact-q endpoints admit a finite path preserving every floor and tau in {q-1,q}. This includes arbitrary positive slack and distinct endpoint overlap structures; no disjoint root witnesses, clique-boundary parameter identity or symmetry equivalence of the endpoints is assumed.

The proof first constructs a lower-guard path, tau>=q-1, through compact graph representations. A star edit changes only root edges incident to one palette label, so deleting that label's entire constraint family would lose at most one hitting unit. Degree-nonincreasing symmetrization then reaches clique components without exceeding the fixed number of root slots. Splitting and balancing those components yields a common normal form. Finally Theorem A in GENERAL_PARENT_CONNECTIVITY.md removes all upper excursions. Thus symmetrization may raise tau; we do not silently demand exactness during it.

This is a theorem for all floors 2, not yet for mixed or higher floors. It addresses all complementary pair/higher-subset guards associated with feasible q in that carrier.

## 2. Exact compaction and representation

Compact each endpoint to pairs by retaining one anchor from a minimum q-label hitting set in each root and one other label. Delete remaining incidences. Floors remain 2; deletion cannot lower tau and the retained hitting set prevents an increase. Compaction is exact-q.

Interpret each pair root as an edge on P. The simple graph G retains one instance of each distinct edge; the r ordered root slots may contain duplicates. Isolated palette labels are retained as vertices. Graph vertex-cover number equals root hitting number, and independence number alpha(G)=k-tau(G). Exact compaction therefore begins with alpha(G)=m:=k-q. In particular m>=1: for roots of size 2 any k-1 labels hit every root. All subsequent graph constructions use the same palette and r slots.

## 3. A floor-safe star-edit lemma

**Lemma O1.** Suppose a pair-root tuple represents G with tau(G)>=q. Change only edges incident to a selected label u, producing a graph G' with deg_{G'}(u)<=deg_G(u). Then the change can be implemented in the r slots by single-incidence moves preserving floors 2 and the lower guard tau>=q-1. This lemma asserts no upper guard and no lower bound q for the final graph beyond what its separate construction proves.

Freeze every root slot whose edge is not incident to u. Together these slots represent G-u (with u isolated). Since a vertex cover of G-u together with u covers G,

    tau(G-u)>=tau(G)-1>=q-1.

There are at least deg_G(u) slots incident to u, enough to represent every desired distinct u-edge because the new degree is no larger. Assign those slots to the desired edges, using duplicates to fill extras. If the new degree is zero, fill them with copies of any edge of G-u; such an edge exists because tau(G-u)>=q-1>=2. If the old degree is zero, there are no incident slots and the permitted change is empty.

Replace each assigned old pair X by its new pair Y through X -> X union Y -> Y, toggling one incidence at a time. Intermediate roots have size at least 2. Every intermediate tuple retains the frozen G-u constraints, so tau>=q-1. At the end the simple graph is G'. No fresh root slot, label, simultaneous edge operation, or numerical search is used. The representation may have different duplicate multiplicities, which is harmless and will later be normalized.

## 4. Degree-nonincreasing symmetrization

For a simple graph write N[v] for the closed neighborhood of v. Equal closed neighborhoods define equivalence classes. Each class is a clique; between two classes either every cross edge is present or none is. Indeed members of a class have identical adjacency to all vertices outside it.

If two distinct classes U,V are adjacent, all vertices of U have a common degree d_U and all of V have degree d_V. Choose the orientation with d_U>=d_V (break ties by the supplied order). Replace the adjacency of all vertices of U to vertices outside U by the pattern of a representative v in V, retaining all edges within U and between U and V. Equivalently, clone v's closed-neighborhood pattern onto U. We establish three facts.

**(a) The change is a sequence of degree-nonincreasing star edits.** Process u in U one at a time. Replace its open neighborhood by (N(v)\{u}) union {v}, where N(v) is v's open neighborhood at that step. Its new degree is d_V. The degree of v remains d_V throughout because v was and remains adjacent to every U vertex, and no other incident edge of v changes. Every unprocessed U vertex retains degree d_U: its adjacency to a processed U vertex remains present and its other edges are untouched. Thus each processed star has new degree d_V<=d_U. Lemma O1 applies whenever the current graph has tau>=q.

**(b) Each completed single-vertex clone cannot increase alpha, hence cannot decrease tau.** An independent set of the new graph not containing u already existed in the old graph. If it contains u, it cannot contain v because uv is retained. Replace u by v. The new neighbors of u outside {u,v} are precisely the old neighbors of v outside {u,v}, and all edges not incident to u are unchanged. The replacement is therefore independent in the old graph. Consequently alpha(new)<=alpha(old). This holds after each individual clone, not only after the whole class operation. Starting from tau=q, all graph endpoints used by O1 have tau>=q.

**(c) The number of closed-neighborhood classes strictly decreases after the whole class operation.** U and V now share one closed-neighborhood pattern and merge. Every other former class stays intact, because its members all receive the same changed adjacencies to the whole class U and its internal clique is unchanged. Other classes may merge but cannot split. Thus at least two old classes merge and none splits at the completed operation.

Repeat whenever distinct classes are adjacent. The number of classes is a positive integer and strictly decreases after every completed class operation, so the process terminates. At termination there are no edges between distinct classes. Each class is a clique, so the graph is a disjoint union of complete graphs, including isolated singletons.

Throughout, the number of distinct edges is nonincreasing: each star edit changes it by new degree minus old degree, which is nonpositive. Slot capacity is therefore respected. Graph endpoints have tau>=q, and primitive intermediate states have tau>=q-1. If the final clique union has t components, its cover number is k-t, so t<=k-q=m.

## 5. Split and balance without losing the lower guard

If t<m, choose a component with at least two vertices and isolate one vertex u by deleting its star. Such a component exists because t<m<k. This is a degree-decreasing edit. The resulting clique union has t+1 components and cover number k-(t+1)>=k-m=q. Lemma O1 supplies the primitive path. Repeating reaches exactly m components in finitely many steps. The ability to fill former star slots with a surviving edge is justified inside O1; q>=3 prevents the remaining graph from being edgeless.

Next, if two clique components have sizes a>=b+2, move one vertex u from the larger component to the smaller: delete its a-1 old neighbors and give it the b vertices of the smaller component as its new neighbors. This is one star edit with new degree b<a-1. It leaves m nonempty clique components and hence tau=q at its endpoints. O1 supplies the lower guard during the edit. The sum of squared component sizes decreases by

    a^2+b^2 - ((a-1)^2+(b+1)^2) = 2(a-b-1)>0.

This positive integer potential ensures termination. All component sizes then differ by at most one. Their multiset is uniquely determined by k and m: floor(k/m) or ceil(k/m), with the necessary multiplicities. The edge count never increased, so the resulting balanced clique graph uses at most r distinct root slots.

## 6. One common root tuple, including duplicates

Fix a canonical partition of the ordered palette into those balanced component sizes, and list all clique edges in a fixed order. General safe label-transposition paths from Lemma L in OVERLAPPING_CLIQUE_EXCHANGE.md map any balanced clique graph to this canonical graph. Each completed transposition is exact-q and its primitive states lie in {q-1,q}.

There remains duplicate multiplicity. Keep one root slot for every distinct edge fixed. These retained slots realize the entire canonical graph of cover number q. Select one canonical edge e_0; one exists since q>=3. Replace every additional duplicate slot by e_0 through its union with e_0. The retained graph forces tau>=q. Any minimum cover of that graph hits the old edge, e_0 and their union, so all intermediate tuples also have tau<=q. Thus duplicate normalization is exactly at q. It gives one copy of every distinct edge and r-e extra copies of e_0, where e is the canonical graph's edge count.

Finally use Lemma M's floor-safe root swaps to place these supports in canonical root order. All floors equal 2, so every such permutation is permitted; its primitive states have tau in {q-1,q}. The resulting tuple depends only on r,k,q and the supplied orders, not on the input graph.

Every exact-q endpoint is now connected to this same tuple by a finite lower-guard path, beginning with exact compaction. Reverse the second endpoint's path and concatenate. Apply Theorem A to this finite root path: its endpoints are exact-q, all floors hold and tau>=q-1 throughout. Maximum-layer replacement removes upper excursions and gives tau in {q-1,q}. This completes Theorem O. We do not assert that the unmodified symmetrization path itself already satisfies the upper bound.

## 7. Consequence and remaining frontier

The all-floor-two carrier admits one-unit repair for arbitrary feasible r,k,q>=3. Together with the existing elementary q=1,2 arguments, this resolves all feasible targets when every child minimum exact width is 2. General pair and higher-subset complementary covers arising from these endpoints are connected under their capacities k-2.

The mechanism changes overlap structure rather than only permuting an isomorphism class: independent-set-nonincreasing clones reach clique unions, which can then split and rebalance. The earlier clique-boundary theorem is a special case, and no extremal equality or disjoint witness hypothesis is needed here.

The missing general case is mixed or higher root floors. Compact roots then need not be graph edges; the closed-neighborhood class argument and its edge-budget control do not automatically extend to hyperedges. A degree deficit or total-capacity bound still is not a universal safe-buffer theorem. No universal arbitrary-floor result, disconnected root example, native barrier, efficiency bound or physical implication is claimed.

Conditional native lifting remains exactly as stated in GENERAL_PARENT_CONNECTIVITY.md, including the child-interface hypotheses and the distinction between width-floor connectivity and native necessity. No implementation or numerical campaign was initiated. A later implementation protocol must separately validate symmetrization, class termination, star-slot reassignment, duplicate normalization, and maximum-layer replacement, in addition to the previously identified mechanisms.

Independent review must check the one-unit star guard, available slots including duplicate/zero-star cases, single-clone independence bound, whole-class termination without hidden splitting, split/balance progress, canonical duplicate multiplicities, and application of upper-excursion removal only after the complete lower-guard connection exists.
