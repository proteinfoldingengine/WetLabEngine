# A11.X56 — colored graph guards without the anchor-edge product

Status: frozen analytical candidate; independent review pending. Exact parent 2fd7531f3c86df2d9e289b0bc299c0a532ffeee2. Scope A11_X56_SCOPE.md at a3393866d52baee219704d405305f803cd3a9361. No numerical execution or implementation certification.

## 1. Actual carrier and theorem

Fix m>=10, role set G={0,...,m-1}, anchors A={0,1,2,3}, and outside roles R=G minus A. Each anchor a has its own simple graph Gamma_a on R. The actual type set is
Qset={ {a} union e : a in A, e in E(Gamma_a) }.
Every declared type has an arbitrary positive number c_Q of ORIGINAL labelled root copies. Absent anchor-edge combinations are absent throughout.

For nonempty J subset A, let Gamma_J have edge set union_(a in J) E(Gamma_a). Assume the colored guard condition
(C) vc(Gamma_J)>|J| for every nonempty J subset A.
Assume four actual compatible relay types: e_u={4,6} belongs to Gamma_1 and Gamma_3; e_v={5,7} belongs to Gamma_0 and Gamma_2. The numeric cyclic labeling is fixed before endpoints and successor j->j+1 are declared. More generally an abstract colored carrier with two disjoint edges having these memberships admits such a labeling: assign their endpoints 4,6 and5,7 and choose m-1 from the remaining outside roles. This is supplied relay compatibility; it is not derived from (C).

Take t>=1 disjoint original labels x_(j,h), j in G, 1<=h<=t, and pairwise disjoint original padding sets Z_j of sizes p_j>=0. Their union is the fixed palette. Source groups are B_j=Z_j union {x_(j,h):1<=h<=t}; destination groups are D_j=Z_j union {x_(j-1,h):1<=h<=t}, modulo m. Each original root copy of Q has source E_Q=union_(j in Q) B_j and exact destination C_Q=union_(j in Q) D_j. Its original individual floor satisfies 1<=f_i<=N_Q=3t+sum_(j in Q)p_j.

There is an explicit finite native path from E to C with 3<=tau<=4 after every single-incidence primitive. Every original labelled destination support is restored. Every differing endpoint incidence toggles exactly once and no other incidence changes, giving the global minimum primitive length. Individual floors may differ and may all be saturated at N_Q. This theorem removes X55's complete anchor-edge product while retaining a derived actual guard and four supplied relay types.

## 2. Exact structural characterization of the guard

Within this actual one-anchor-plus-edge carrier, the following statements are equivalent:
(i) condition (C);
(ii) every role footprint F with |F|<=4 and F!=A is avoided by some actual type;
(iii) A is the only role hitting set of size at most four.

For (i)->(ii), let J=A minus F and X=F intersect R. J is nonempty, since |F|<=4 and F!=A. Also |X|<=4-|F intersect A|=|J|. By (C), X cannot cover Gamma_J. Thus some actual edge e of Gamma_a, with a in J, avoids X. The actual type {a} union e avoids all F. Statement (ii) is precisely (iii), since A hits every type.

Conversely, if (C) fails for some nonempty J, choose a vertex cover X of Gamma_J with |X|<=|J|. Then F=(A minus J) union X has size at most four and differs from A. It hits all actual types: roots with anchor outside J meet F at that anchor, and roots with anchor in J meet X. Hence (iii) fails.

This is an exact criterion for the declared complete-footprint guard and unique small role cover, not a necessary condition for native repair. If it fails, a different cover of size four may exist while exact target four and repair remain possible. No disconnection is inferred.

Every current prepared group has size t+p_j>=1. A physical cover projects to the roles containing its labels. A hits all actual roots, and the equivalence excludes every role cover of size at most three. Thus every source, destination and completed-column prepared tuple has exact transversal four. Its four-label minimum covers select one label from each anchor group. Copies and fixed padding do not affect this conclusion.

## 3. Actual lower protection during a column

Resolve columns in increasing h. Its selected label x_(j,h) has current owner j and required owner j+1. Other labels have one unchanged current owner during this exchange. For a physical pair K, combine current and required owner roles. Ordinary labels contribute one role and selected labels contribute {j,j+1}; the footprint has size at most four.

Only two selected labels can produce a four-role footprint. Their footprint equals A only when their consecutive directed edges partition A, which for m>=10 happens precisely at starts0 and2. Hence the sole exceptional pair PER ACTIVE COLUMN is K*={x_(0,h),x_(2,h)}. Every other pair, including pairs in one group, padding, labels in completed/uncompleted other columns, and mixed anchor/outside pairs, has an actual type avoiding its entire old/new support union by section2. That witness survives all edits of its own root and every other root.

For K*, actual old u={1,4,6} avoids its old owners0,2; actual completed new v={2,5,7} avoids its new owners1,3. Complete all v copies before changing any u copy. An untouched old u copy remains until a new v copy exists; afterward that completed actual v copy persists. There is no independent capacity allocation per pair: common witnesses may serve many obligations, and all supports are their actual shared supports on the one sequence below.

## 4. Five-stage upper handover on the SAME actual types

Write selected physical four-covers using current source indices:
K0={0,1,2,3}, L={0,2,4,6}, K2={m-1,0,1,2}.
Their new owner sets are respectively {1,2,3,4}, {1,3,5,7}, A.

Let U_j and V_j denote actual types missed by cover j at the old and new endpoint of this column. Directly:
U0=empty;
V0={actual {0} union e : 4 not in e};
U1={actual {a} union e : a in {1,3}, e disjoint from {4,6}};
V1={actual {a} union e : a in {0,2}, e disjoint from {5,7}};
U2={actual {3} union e : m-1 not in e};
V2=empty.
All these sets use each Gamma_a separately; absent combinations are never inferred.

The four supplied types are v={2,5,7}, u={1,4,6}, b={0,5,7}, c={3,4,6}. Process:
1. v;
2. every actual type in U1;
3. b;
4. every still unprocessed actual type in U2;
5. every remaining actual type,
with fixed order within stages and complete consecutive blocks of original copies.

These stages are disjoint and complete. v lies in neither U1 nor U2 and b in neither. Stages1/2 contain no V0 type. Stages1 through4 contain no V1 type: U1 and U2 use anchors1/3, while v and b contain5,7. Thus all U1 precede all V0 and all U2 precede all V1. Type u is in stage5. Type c is in stage4, since it meets4,6 but avoids m-1. These facts use only the four actual relay types and their stated positions.

Use K0 in stages1/2, L in stages3/4 and K2 in stage5. K0 has no new exception begun; L has every old exception completed and no new exception begun; K2 has every old exception completed and no new exception. The chosen cover therefore hits all other current endpoints and BOTH endpoints of every active type, including coexistence of arbitrary old/new copies.

For each original copy, add every missing new incidence one at a time, then remove every old-only incidence one at a time. During additions it contains its full old support; during removals it contains its full new support. Its size never falls below N_Q, so it retains its original floor. It stays within the fixed palette and the full endpoint union. Section3 supplies all lower witnesses on precisely this schedule; the displayed cover supplies the upper witness. Thus every primitive has 3<=tau<=4. No compaction, simultaneous move, extra slot, extra label or floor weakening is used.

## 5. Renewal, next-move existence, termination and exact restoration

Every stage explicitly lists existing types, existing copies and finitely many incidence edits. Skip empty lists. Whenever a column is unfinished, the first pending edit exists and is eligible by sections3/4. The pending list length strictly decreases per primitive.

After a column finishes, every group again has t+p_j labels and every original root again has its prepared type support of size N_Q. Exact four, (C), the relay types and all floor margins are renewed. If another column remains, its selected labels still have their original current owners, so the same argument applies with those labels. No witness resource is consumed.

After h completed columns, m(t-h) column labels remain assigned to the wrong auxiliary owners. This decreases by m per completed column. Roles and owners are a proof organization of incidences; relabeling owners with no affected incidence is not an additional native primitive. Each column's actual edit list is finite and nonempty, since every nonempty proper Q crosses the full cycle. All t columns terminate at the exact labelled destination supports. Padding stays fixed.

For t>=2, after the first column each root has a changed crossing incidence from that column and a pending crossing incidence in a later column, so every root differs from both outer endpoint supports while renewal remains available. This does not prove absence of another whole-root order.

## 6. Global minimum and graph-dependent count

A selected label with old owner s and new owner s+1 belongs to a root precisely according to 1_Q(s) and 1_Q(s+1). The construction touches it only if these differ, once in its own column. Common incidences, absent incidences and padding are untouched. Therefore length is
t sum_(Q in Qset) c_Q |Q symmetric-difference (Q-1)|,
exactly the full outer endpoint Hamming distance. Every primitive changes one incidence, so this is the global lower bound for any path between those exact supports; our path attains it.

For one copy per type, put s=sum_a |E(Gamma_a)|. Let a_a count edges of Gamma_a joining consecutive outside roles in the fixed cyclic order. Define
H=sum_a a_a + deg_(Gamma_3)(4) + deg_(Gamma_0)(m-1).
For each three-role type Q, |Q symmetric-difference (Q-1)|=6-2e(Q), where e(Q) counts cyclic adjacent role pairs within Q. Outside adjacencies sum to sum_a a_a; only anchor/outside boundary pairs3,4 and m-1,0 contribute, giving the displayed degree terms. There are no two anchors in a type. Hence the exact one-copy length is t(6s-2H). This is symbolic mathematics, not a benchmark.

## 7. Eight-type extremal incomplete-product family

For every m>=16 choose six pairwise disjoint actual outside edges:
e_u={4,6}, e_v={5,7}, f0={8,10}, f1={9,12}, f2={11,14}, f3={13,m-1}.
Declare only:
Gamma_0={e_v,f0}, Gamma_2={e_v,f2},
Gamma_1={e_u,f1}, Gamma_3={e_u,f3}.
Thus there are exactly eight distinct actual types, with arbitrary positive original labelled multiplicities. All omitted anchor-edge combinations stay absent.

Every Gamma_J is a matching. Its edge count, hence vertex-cover number, is2 for singleton J, 3 or4 for a pair (3 when both anchors share e_u or e_v), 5 for a triple, and6 for all four. Each exceeds |J|, proving (C). The four relay types exist.

None of the six edges joins consecutive outside roles, including f3 because m-1>=15. The only anchor/outside type adjacency is3,4 in c={3,4,6}. Thus H=1, s=8, and the exact one-copy minimum is46t. Uniform d copies multiply this by d; arbitrary copies use section6.

Condition(C) on each singleton anchor implies vc(Gamma_a)>=2, hence at least two edges per anchor. Therefore s>=8. This control attains eight, which is minimal among actual distinct types satisfying(C) in this one-anchor-plus-edge representation. It is not a universal native root-count minimum.

The common graph intersection of the four Gamma_a is empty. Hence no all-anchor edge product is available in this representation, directly removing X55's product input. Extra outside roles may be isolated; their inclusion extends the fixed palette but supplies no additional protective root types. The result is the structural colored criterion and its attaining family, not a campaign over root counts.

## 8. Controls, dependencies and exact remaining scope

The full outer endpoint-union tuple has transversal exactly two. The selected pair {x_(0,1),x_(2,1)} has footprint A and hits every union. Every singleton has a footprint of size at most two other than A, so section2 supplies an actual union root avoiding it. Thus there is no permanent union guard.

For singleton groups and one column (t=1, all p_j=0), K0 and K2 are the unique physical endpoint four-covers. Immediately after b completes and before c begins, K0 misses new b and K2 misses old c. A two-cover family working for this specified schedule would have to contain both unique endpoint covers and therefore fails there. The three supplied covers work. Necessity is only for this schedule and singleton setting, not all possible orders.

The proof derives its actual guard from colored graphs, and spells out the X51-X55 upper/lower interface with its own primitive and renewal checks. It needs no maximum-layer conversion. Applicable uniform/symmetry native connectivity was already accepted; this adds an incomplete-product renewable schedule with an exact minimum, not a new connectivity classification.

Condition(C), the four compatible actual relay types, cyclic labeling fixed before endpoints, equal corresponding group sizes and supplied parallel columns remain inputs. (C) alone does NOT force relay compatibility: give each anchor two private pairwise disjoint outside edges, with all eight edges disjoint; then vc(Gamma_J)=2|J|>|J| but every cross-anchor edge intersection is empty. This defeats this relay extraction method, not native repair.

Failure of(C) gives a competing small role cover; it does not prove disconnection or failure of all handovers. Multiple coupled exceptional pairs, missing compatible relays, arbitrary preassigned ownership exchanges and universal mixed/directed/higher-target/nested repair remain open. Unbounded upper-cover stages with moving lower protection also remains open.

No numerical execution, implementation, efficiency benchmark, integration merge, numbered certification or physical claim is made. v16.54/v16.55 and original evidence remain preserved. Separate efficiency runner/fixture/benchmark work remains unstarted. Next: derive renewable repair when colored protection holds but the four shared relay types do not exist, or handle several coupled exceptional pairs.
