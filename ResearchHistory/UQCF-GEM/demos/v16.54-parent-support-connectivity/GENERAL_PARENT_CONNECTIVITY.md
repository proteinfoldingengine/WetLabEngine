# General parent-support connectivity — candidate analytical proof

Status: candidate for independent analytical review, not implemented or numerically certified. Native scope was frozen at3932248af7bb5c64bdd3d467fcd6d78ddf7adde5. This proof was developed after that scope commit, except for the preliminary leads explicitly disclosed there.

## 1. Typed problem and main result

Fix r>=2, a finite ordered palette P of size k, and floors 1<=a_i<=k. Let D(a) consist of tuples A=(A_1,...,A_r), A_i subset P, |A_i|>=a_i. An edge toggles one incidence (i,x), remaining in D(a). Let tau(A) be the minimum number of labels meeting every A_i. All roots are nonempty, so 1<=tau<=min(r,k).

For q>=2 with exact-q endpoints, define the lower graph L_q by tau>=q-1 and the unit-band graph G_q by q-1<=tau<=q+1. The central statement is:

**Theorem A — upper-excursion removal.** Two exact-q tuples are connected in G_q if and only if they are connected in L_q. Moreover, whenever they are connected in L_q, there is a finite path between them with tau in {q-1,q} throughout.

Thus, in this width-floor parent problem, the upper guard is not an independent obstruction. The remaining question is whether the required exact endpoints are connected while preserving the lower guard. The theorem does NOT assert that L_q is connected for every r,a,k,q. It does NOT make width-floor disconnection a necessary native obstruction; Section7 explains that distinction.

The structural ingredients are explicit: the root carrier is closed under adding incidences and taking unions; a completed merge of two label roles lowers transversal by exactly one when chosen from a minimum cover; the union of two such repairs lowers it by at most two. Those two units are measured from the forbidden layer immediately above the desired band, leaving at most one unit below the exact target. Extra constraints forbidding arbitrary root incidences or unions would invalidate this argument unless separately checked. No such additional constraint is present in the frozen native carrier.

## 2. Monotonicity and a controlled merge of label roles

Tuples are ordered componentwise by inclusion. Adding incidences cannot increase tau. A single addition can decrease tau by at most one: if label x is added to A_i, take any hitting set for the new tuple and, if necessary, add one old label y in A_i. This hits the old tuple with at most one extra label. The reverse statement holds for a deletion that leaves all roots nonempty.

For distinct labels x,y, define M_{x<-y}(A) by adding x to every root containing y, retaining all original incidences. Each addition is a legal native root move and preserves every floor. Any hitting set K for the expanded tuple yields a hitting set for A contained in K union {y}: only uses of the newly extended x role can need repair. Hence

    tau(A)-1 <= tau(M_{x<-y}(A)) <= tau(A).

If tau(A)=t>=2, choose x,y in a minimum hitting set H of size t. Then H\{y} hits M_{x<-y}(A), so its hitting number is exactly t-1. Denote one such completed expansion by S(A). Its internal construction need not be included as a prefix of the final path: S(A) is an auxiliary tuple used in the path replacement below. The final output starts at the original endpoints and consists only of the legal incidences in those replacement paths.

A second bound will be useful. Add to a base tuple Z two such packets, each defined from ORIGINAL source-role membership in Z, with pairs (x_1,y_1) and (x_2,y_2). Any hitting set of their union becomes a hitting set of Z after adding y_1 and y_2. Therefore the union has transversal at least tau(Z)-2. The pairs may share labels; the same bound holds. We do not assume two sequentially recomputed packets have identical membership to these two original-role packets.

## 3. Removing the maximum layer of a path

Suppose a finite root path has tau>=L everywhere, maximum value t, endpoints below t, and t-2>=L. Replace every vertex A with tau(A)=t by S(A), and leave the other vertices alone. We now connect consecutive replaced vertices without visiting level t or dropping below L.

If both old vertices were below t, retain their original edge.

If A has tau=t and its neighbor C is below t, the one-incidence bound forces tau(C)=t-1. Monotonicity forces C=A union {e} for one added incidence e. Let U=C union S(A). Connect S(A) to U by additions and U to C by deletions; omit unchanged steps. Along the first segment every state contains S(A), and along the second it contains C, so tau<=t-1. Every state is a subset of U. Since U is S(A) with at most one extra incidence, tau(U)>=t-2. Width floors hold on the addition segment because it starts at S(A), and on the deletion segment because it ends at C. Reverse this construction if the order of the edge is reversed.

If both A and C have tau=t, they differ by one incidence and are comparable by inclusion. Put Z=A union C, the larger tuple; tau(Z)=t. Let U=S(A) union S(C). Then U contains Z and is contained in Z with two original-role merge packets added: source-role memberships in A and C are subsets of those in Z. By the bound in Section2 and monotonicity, tau(U)>=t-2. Connect S(A) to U by additions, then U to S(C) by deletions. Each half contains its corresponding completed expansion of transversal t-1, so tau<=t-1. Every intermediate state is a subset of U, so tau>=t-2. Floors again hold because every state contains either S(A) or S(C).

The resulting path has maximum at most t-1 and minimum at least L. All intermediate changes are single incidences; set unions in the argument specify endpoints of finite addition/deletion segments, not simultaneous native moves. Endpoint tuples are unchanged. Repeat for decreasing maximum levels until the maximum is U_0, provided U_0>=L+1. This terminates because every replaced finite path is finite and its maximum strictly decreases; no path-length efficiency is claimed.

For Theorem A, take L=q-1 and U_0=q. The first removed level at the end is t=q+1, and t-2=q-1=L. The converse follows because G_q is a subgraph of L_q. This proves the theorem.

## 4. Exact general reformulation by complementary blocks

Let B_i=P\A_i and b_i=k-a_i. Then |B_i|<=b_i<=k-1. A label subset H fails to hit A exactly when H subset B_i for some i. Consequently

    tau(A)>=q-1  iff every (q-2)-subset of P is contained in some B_i.

Exact-q feasibility implies k>=q, so this level of subsets exists. For q=2 the empty subset gives the trivial lower condition. For q>=3 this is a capacity-bounded cover of all (q-2)-subsets by complete subset families on the blocks B_i. Root incidence toggles are precisely reversed block incidence toggles. Theorem A therefore yields:

**Corollary B — general parent criterion.** The exact-q tuples have unit-band connectivity if and only if their complementary block tuples are connected through capacity-bounded covers of all (q-2)-subsets. Any such connection can be converted into a root path with only downward parent excursion, tau in {q-1,q}.

This is a necessary-and-sufficient criterion for the abstract width-floor root graph. It is not an assertion that the required capacity-constrained subset-cover connectivity always holds. The structural frontier is now explicit: ordinary element covers for target3, pair covers for target4, and higher subset covers for higher targets. Total unused capacity alone has not been proved sufficient at the higher levels.

For comparison, target1 is connected by expansion to all roots P and contraction to the target tuple, keeping tau=1. Target2 uses the same route with tau in {1,2}. These work for every r.

## 5. Target3 is connected for arbitrary parent arity

**Lemma C — bounded element-cover connectivity.** Let blocks B_i cover P, with |B_i|<=b_i, and sum b_i>=k+1. Any two such covers are connected by single block-incidence moves preserving coverage and capacities, including zero capacities.

Proof. Select one owner for each label and remove its other copies. This gives a partition into bins of capacities b_i. To transform one partition f into another g, leave correctly placed labels fixed. Choose a misplaced x with destination j=g(x). If bin j has room, add x there and then delete its old copy. If j is full, some occupant y is misplaced: otherwise its b_j correctly destined occupants together with x would violate the target capacity. Because total occupancy is k and total capacity is at least k+1, another bin h has room. Transfer y from j to h by add-then-delete, then transfer x to j. The spare bin h may be x's current bin; these two transfers still preserve coverage and capacities. No previously fixed label is displaced, and one additional label becomes fixed. Repeat finitely, then add target duplicate occurrences. Each final bin remains a subset of its target until complete. This proves the lemma.

Now take exact-q endpoints with q=3. At an exact-q tuple, no label can appear in more than r-q+1 roots: a label in d roots, together with one label from each of the remaining r-d roots, would be a hitting set of size at most1+r-d. Thus for q=3,

    sum a_i <= sum |A_i| <= (r-2)k,
    sum b_i = rk-sum a_i >= 2k >= k+1.

The last inequality is valid because exact target3 requires k>=3. Both endpoint complementary block tuples cover P. Lemma C connects them in L_3. Theorem A removes all upper excursions and gives a path with tau in {2,3}.

**Theorem D.** For every r>=3, every finite P and every width vector a admitting exact target3 endpoints, those endpoints are connected with tau in {2,3}. No extra label, additional native admissibility condition or arity-dependent recurrence is used. Five-child target3 is a consequence of this arbitrary-arity result, not a separately fitted case.

## 6. Five-child target4: what pair-cover connectivity needs

Here the lower guard is tau>=3, equivalently coverage of every label pair by complementary blocks. Element-cover connectivity alone does not establish it. We prove this diagnostic case by a second general lemma about sparse incidences, not by enumerating five-child states.

**Compact endpoints.** For any exact-q root tuple, choose a minimum hitting set H and, for each root, an anchor in A_i intersect H. Delete other labels until |A_i|=a_i, retaining its anchor. Deletion cannot decrease tau, while H continues to hit every root, so tau remains exactly q. This works for any r and any positive floors.

At exact target4 with r=5, each label occurs in at most2 roots by the degree bound above. Compact both endpoints. Write S=sum a_i. Necessarily S<=2k.

**Lemma E — degree-two incidence reconfiguration with spare capacity.** For any number r of rows, all binary incidence matrices with fixed positive row sums a_i, column sums at most2 and S<2k are connected by incidence additions/deletions that preserve column capacity2 and row floors a_i. A completed transfer keeps the row sum exact; its add-before-delete intermediate has one extra incidence in that row.

Proof. Fix current and target matrices. In each row pair its surplus columns with its deficit columns, making a directed edge x->y for each pair, colored by that row. If a destination column y has a free slot, perform that transfer: add the row's y incidence, then delete its x incidence. The y incidence is absent and x present because they are a pending deficit/surplus pair. Remove the processed edge.

If differences remain and no edge ends at a column with a free slot, every column with incoming edges is full. At each column, outgoing minus incoming edge counts equals current minus target column occupancy. Thus such a full column has at least as many outgoing as incoming edges, since target occupancy is at most2. Following edges therefore produces a directed cycle; choose a simple one. Its consecutive edges cannot all have the same row color: a column cannot simultaneously be a surplus and a deficit of one row. In fact adjacent cycle edges have distinct colors, so at least two colors occur.

There is a spare column z because S<2k. It has at most one current row occupant and, in this blocked situation, no incoming edge; in particular it is not on the cycle. Choose a cycle edge x->y whose row does not occupy z; at least two colors are available and at most one occupies z. Temporarily transfer that row's x incidence to z. The newly free slot at x allows the preceding cycle edge to transfer into x. Continue backwards around the simple cycle until y is free, then transfer the buffered incidence from z to y. Each transfer adds before deleting, respects column capacity, and preserves row floors. Its destination is absent from the row: cycle destinations were pending deficits, distinct cycle columns have distinct incoming edges, and the buffer is outside the cycle. Repeated row colors do not change this because surplus and deficit sets within that row are disjoint. The buffer returns to its old state and every cycle edge is resolved. This strictly reduces the remaining differences. Repeating the greedy transfers and cycle procedure terminates at the target.

If S<2k, apply Lemma E to the compact endpoints. Every intermediate label hits at most2 of the five roots; therefore tau>=ceil(5/2)=3. Nonemptiness gives tau<=5. This already supplies a unit-band connection. Theorem A can additionally remove level5, giving tau in {3,4}.

**The saturated case S=2k.** Every column of a compact exact endpoint has degree2. Make a graph on the five child indices whose edges are the pairs occupied by labels; parallel labels may give the same edge. Every vertex is incident to an edge. Two disjoint edges would hit four children with two labels and the fifth with a third, contradicting tau=4. Hence all distinct edges pairwise intersect.

A pairwise-intersecting edge family is a star or lies in a triangle. To see this, take ab and ac; an edge avoiding a must be bc, and then any edge meeting ab,ac,bc has both ends among a,b,c. A triangle cannot cover all five nonempty child indices. Thus all edges share a hub h. Every label lies at the hub, so a_h=k, while the other four roots partition P. The width vector forces this same unique hub at both endpoints because the other four widths are positive and sum to k.

Connect the two partitions by label swaps between nonhub bins of fixed sizes. A swap of x in bin i and y in bin j is: add y to i, add x to j, delete x from i, delete y from j. The only shared nonhub labels are between this same pair of bins. The four nonhub roots therefore require either3 or4 hitting labels; the full-palette hub is redundant. Floors hold throughout. Any desired partition of the same bin sizes can be reached by such swaps: select a misplaced label, swap it with a misplaced occupant of its desired full bin, and fix at least that label without moving any already fixed label.

**Theorem F.** Every feasible five-child exact-target4 pair is connected by a finite root path with tau in {3,4}, for all palette sizes and positive width vectors. S>2k is infeasible by the exact-endpoint degree bound, not excluded because a construction failed. The no-spare-capacity case is explicitly covered; Lemma E is not misapplied there.

Lemma E is arity-independent, but its hitting lower bound ceil(r/2) meets q-1 for (r,q)=(5,4) and need not do so at higher targets/arities. For example, at r=6,q=5 it supplies only3 where4 is required. That is a limitation of this sufficient mechanism, not a nonunit obstruction.

## 7. Arity-independent lifting and its limit

Suppose each child already has the same six-clause interface, of minimum exact width a_i. First normalize every child on its fixed current root, one at a time while the parent is exact. This costs at most one global unit. Its proper-descendant support union then has exactly a_i labels (a leaf has none).

For a root-path addition, add the incidence at that child root. For a root-path deletion of x, the old root has size>a_i because the new root respects its floor. If x occurs below a nonleaf child root, choose y in that root outside its a_i-label proper-descendant union. Add y wherever x occurs below the root in preorder, then delete x there in reverse preorder. This fixed-root clearance preserves nesting, nonemptiness and every internal hitting coordinate by the original/dominated-label replacement argument from v16.53. It does not alter any child root during clearance, so the outer parent coordinate stays unchanged. Then delete x at the child root. A leaf requires only the direct nonempty root deletion.

All child interiors remain exact during lifted root reconfiguration. Consequently the parent's unit bound is the entire global sum of deviations during that phase. The proper-descendant compact-union invariant is retained by clearance, allowing repeated deletions without recursive normalization while the parent is inexact. At the exact destination root tuple, normalize children again while the parent is exact.

This proves that the root criterion suffices for the native nested repair. It also explains why a disconnected width-floor graph alone would not prove a native barrier: a general native unit path may spend its unit inside a child and temporarily use a palette below that child's minimum exact width. This argument does not exclude such paths.

Exact feasibility and compact canonical endpoint selection can be specified for arbitrary r by the same finite nonempty incidence-region enumeration as v16.53, with 2^r-1 region types. The compact-endpoint argument in Section6 proves the needed reduction from roots above their floors. Existence at some width follows by taking disjoint private palettes and identifying one chosen label in r-q+1 children, leaving q-1 isolated child palettes. This gives transversal q using sum a_i-(r-q) labels. A minimum-width tuple cannot contain an unused label. Choosing the least feasible positional tuple and induced child palette orders supplies the canonical endpoint; all finite choices in the proofs can be resolved by the supplied orders. The inherited attached role-replacement and root-only contraction arguments remain arity-independent.

These statements identify how a proved root connectivity theorem can return the unchanged interface. No arbitrary-arity theorem for all target profiles is claimed: higher subset-cover connectivity remains the missing obligation.

## 8. What this resolves and what remains open

Theorem A and Corollary B supply a general, arity-independent connectivity principle: upper excursions can be removed; exact endpoint connectivity is equivalent to the corresponding capacity-bounded lower-cover connection in the width-floor root graph.

Target3 now has a proof for arbitrary parent arity, using native-derived slack and element-cover connectivity. Five-child target4 has a proof through degree-two reconfiguration plus an explicit saturated-hub argument. Neither conclusion relies on a finite passing-case count.

The unresolved general problem is: for arbitrary feasible r,a,k,q>=4, are the complementary tuples of exact-q states connected through capacity-bounded covers of every (q-2)-subset? Native exact states additionally cover every (q-1)-subset and fail to cover at least one q-subset; these stronger endpoint conditions may matter. Their usefulness beyond the proved cases is not assumed. At exact endpoints every label misses at least q-1 roots, giving sum b_i>=(q-1)k, but a total-capacity inequality has not yet been shown sufficient for pair/higher-subset reconfiguration.

Independent analytical review must check maximum-layer replacement, original-role packet bounds, capacity-cycle buffering, saturated hub classification and the native lifting distinction. No implementation, new numerical campaign, actual-merge replay or v16.54 certification is claimed here.
