# A11.X57 — derived handover without shared relay types

Status: frozen analytical candidate; independent review pending. Parent 01216defde7c584d433049e85f11c1b41d74f8c1. Scope A11_X57_SCOPE.md at 89db2f534a7ad4e9a7e8449c625d8de6ed0f91e9. No scientific execution or numbered certification.

## 1. Structural theorem and order of declarations

Let m>=10. Take an ABSTRACT outside role set of size m-4 and four ABSTRACT anchors. Each anchor a has its own actual simple outside graph Gamma_a. The actual root types are precisely {a} union e for e in Gamma_a, with arbitrary positive ORIGINAL labelled multiplicities c_Q.

Assume X56's colored guard
(C) vc(Gamma_J)>|J| for every nonempty anchor subset J,
where Gamma_J is the union of the actual edge sets of its anchors.

Condition(C) alone supplies two actual disjoint edges at distinct anchors by section2. Choose those anchors to be roles1 and2, their edges to be {4,6} and {5,7}, and the other anchors0 and3. Choose a further outside role for m-1; other outside labels are arbitrary. ONLY AFTER both anchor and outside labeling are fixed, declare G={0,...,m-1}, A={0,1,2,3}, R=G minus A and the numerical successor j->j+1.

For t>=1, let the original fixed palette consist of disjoint labels x_(j,h), j in G, 1<=h<=t, and pairwise disjoint original fixed padding Z_j, |Z_j|=p_j>=0. Source groups B_j=Z_j union {x_(j,h):1<=h<=t}, destination groups D_j=Z_j union {x_(j-1,h):1<=h<=t}, modulo m. Each original copy of Q has source E_Q=union_(j in Q)B_j and exact labelled destination C_Q=union_(j in Q)D_j. Its ORIGINAL individual floor is 1<=f_i<=N_Q=3t+sum_(j in Q)p_j.

A finite explicit path connects these exact-four endpoints with 3<=tau<=4 after every one-incidence primitive, arbitrary original copy multiplicities and arbitrary unequal saturated floors. Each completed column renews protection for the next; every exact original labelled destination support is restored. The total path globally minimizes primitive incidence count.

The improvement is removal of X56's supplied four shared relay types. The guard itself derives the two actual transfer roots and an upper-cover order compatible with them. This is an existence theorem for a compatible exchange declared AFTER labeling, not all preassigned cyclic orders or arbitrary exact endpoint pairs.

## 2. Finite actual cross-anchor witness selection

The full union Gamma_A has vertex-cover number at least five. Construct a maximal matching by repeatedly taking an actual edge whose endpoints are not yet used, until none remains. This terminates since the graph is finite. The endpoints of a maximal matching cover every union edge; otherwise an uncovered edge could be appended. A maximal matching therefore cannot have at most two edges, as its at most four endpoints would cover Gamma_A. Select three pairwise disjoint actual matching edges.

For each, choose one anchor color in which it actually occurs. If two selected edges have different chosen colors, they are the required disjoint cross-anchor edges. If all chosen colors equal a, choose any different anchor b and any actual edge f of Gamma_b. Such an edge exists because(C) for {b} gives vc(Gamma_b)>=2. The two endpoints of f can meet at most two of the three disjoint edges, so f is disjoint from at least one selected edge e of color a. Their actual types have distinct anchors.

Every selection step specifies a finite eligible object. No cloning, missing combination or graph edge is introduced. With m-4>=6, after labeling four endpoints4,6,5,7 there is a further outside role available for m-1. Anchor color renaming is a preliminary choice of this declared exchange, not a permutation of existing unequal-floor root slots.

Thus every abstract colored carrier satisfying(C) admits the compatible labeling used in section1. This does not assert that a given pair of numerical colors1,2 always has disjoint edges, or that relabeling preserves an already declared numeric cycle.

## 3. Exact-four prepared states and ordinary actual pair guard

For completeness, reproduce X56's exact footprint characterization. If a role footprint F has |F|<=4 and F!=A, put J=A minus F and X=F intersect R. Then J is nonempty and |X|<=|J|. By(C), X is not a vertex cover of Gamma_J. Some actual edge e in an actual color a in J avoids X, so actual Q={a} union e avoids F.

Conversely, a violating vertex cover X of Gamma_J with |X|<=|J| produces F=(A minus J) union X, a hitting set of size at most four different from A. Therefore(C) is equivalent to A being the only role cover of size at most four, and to every other footprint of size at most four having an actual avoiding type. Necessity here concerns this footprint condition, not native repair.

Every prepared role group is nonempty. A physical cover projects to its owner roles, so no three-label cover exists; one label per anchor supplies a four-cover. Source, destination and every completed-column boundary consequently have exact transversal four.

During column h, selected x_(j,h) changes owner j to j+1. Every other label has one unchanged current owner during that column. A physical pair's combined current/required owner footprint has size at most four. A four-role footprint requires two selected labels; it equals A only when their two directed consecutive edges partition A. For m>=10 the only starts are0 and2. Thus K*={x_(0,h),x_(2,h)} is the sole exceptional pair PER ACTIVE COLUMN.

All other physical pairs, including same-group labels, padding, other columns, mixed and outside pairs, have an actual root type avoiding the entire old/new support union. Throughout the edits below every copy stays inside its endpoint union, so these actual witnesses remain valid even while their roots are active.

For K*, derived old u={1,4,6} avoids old owners0,2; derived new v={2,5,7} avoids new owners1,3. Complete v before changing u. An untouched old u copy supplies the pair witness until a completed actual v copy exists; afterward that completed v copy persists. Shared witnesses retain their actual supports on the same sequence, without separate capacity assumptions for overlapping obligations.

## 4. Three-stage path and two actual upper covers

Use selected physical covers, named by source indices:
K0={0,1,2,3}, K2={m-1,0,1,2}.
Their new owner sets are {1,2,3,4} and A.

The types missed by K2 in old supports are
U={actual {3} union e : m-1 not in e}.
The types missed by K0 in new supports are
V={actual {0} union e : 4 not in e}.
K0 hits every old support; K2 hits every new support. Crucially U and V have different anchor colors.

Process these disjoint and exhaustive stages:
1. the derived type v={2,5,7};
2. every actual type in U, in a fixed order;
3. every remaining actual type, in a fixed order.
Process all original labelled copies of a type consecutively. Type v is not in U or V; u has anchor1 and is in stage3. Thus v completes before u starts. No type in stages1/2 belongs to V.

Use K0 during stages1/2: every new completed or active endpoint avoids the exception set V, while every old endpoint is hit. Use K2 during stage3: every old exception U is already complete, and every new endpoint is hit. At the stage boundary both four-covers hit the prepared state. At every active copy the chosen cover hits BOTH endpoints. This handles arbitrary old/new copy coexistence.

For each copy, add every missing new incidence one at a time, then remove every old-only incidence one at a time. During additions it contains the full old support; during removals it contains the full new support. It never has fewer than N_Q labels and retains its individual original floor. It stays within the fixed palette and its endpoint union. Section3 proves all lower pair protection on this SAME order, while K0 or K2 supplies an actual four-cover. Every primitive therefore has 3<=tau<=4.

The additional X56 types b={0,5,7} and c={3,4,6} are not required. They may exist or be absent. When they exist, c belongs to stage2 and b to stage3, reversing the boundary used to prove three-cover necessity on X56's different schedule. X56 explicitly restricted that necessity to its supplied schedule, so the results agree.

## 5. Renewal, eligible progress and labelled restoration

Each stage is a finite list of actual types, actual original copies and literal incidences. Empty lists are skipped. If a column is unfinished, the first pending incidence edit exists and is eligible by sections3/4; each primitive reduces this list length.

After a column finishes, every group again has size t+p_j and every original root has its prepared type support of size N_Q. Exact four, condition(C), the derived u/v types and all original floor bounds persist. Remaining selected columns still have their original current owners. Apply the same construction with the next column's labels. No old/new witness resource is consumed.

After h completed columns, m(t-h) selected labels remain assigned to wrong auxiliary owners. This decreases by m per finite column exchange and reaches zero. Owner assignments merely organize root incidences; an auxiliary owner change affecting no root incidence is not counted as a native primitive. Each proper nonempty type Q crosses the full directed cycle, so every actual column edit list is nonempty. All labelled root supports, including arbitrary padding and copies, finish at their exact original destination.

For t>=2, after the first column each root has a completed crossing incidence and a pending later-column crossing incidence, hence differs from both outer endpoint supports while renewal remains available. No failure of every alternative whole-root order is claimed.

## 6. Global incidence minimum and count

A selected label with source owner s and required owner s+1 has root membership 1_Q(s) and1_Q(s+1). Every differing incidence toggles exactly once in its column; common, absent and fixed-padding incidences are untouched. Path length is therefore
t sum_Q c_Q |Q symmetric-difference (Q-1)|,
the full outer endpoint Hamming distance. Every one-incidence path must use at least that many primitives; this path attains the GLOBAL minimum.

For one copy per actual type, let s=sum_a |E(Gamma_a)| and let a_a count edges of Gamma_a joining consecutive outside roles in the chosen numeric order. Put
H=sum_a a_a + deg_(Gamma_3)(4) + deg_(Gamma_0)(m-1).
Each three-role Q contributes6-2e(Q), with e(Q) the number of cyclic adjacent role pairs inside Q. Summed outside adjacencies give sum_a a_a and the only anchor/outside boundary pairs give the two displayed degrees. Thus the exact length is t(6s-2H). This is an analytical identity, not executed performance evidence.

## 7. Private-edge family that defeats the old relay extraction

For EVERY m>=20, declare only
Gamma_0={ {8,10},{9,12} },
Gamma_1={ {4,6},{11,14} },
Gamma_2={ {5,7},{13,16} },
Gamma_3={ {15,18},{17,m-1} }.
All eight outside edges are pairwise disjoint and no edge is repeated at a second anchor. For each J, Gamma_J is a matching with2|J| edges and vertex-cover number2|J|>|J|. Therefore(C) holds. Actual u and v exist in the fixed labeling, but ALL cross-anchor edge intersections are empty. In particular no four-type shared relay rectangle of X56 can exist in any anchor relabeling of this representation. Its private-edge failure control now has a positive renewable construction.

There are exactly eight distinct root types, with arbitrary positive original copies. All eight edges are nonconsecutive for m>=20, Gamma_3 has degree zero at4, and Gamma_0 has degree zero at m-1. Hence s=8,H=0 and the exact one-copy path length is48t. Uniform d copies multiply by d; arbitrary copies use section6.

Condition(C) for singleton colors requires at least two edges per anchor, so eight is the minimum distinct-type count within this colored footprint representation. It is not a universal native root minimum. Extra isolated outside roles supply no new protection. Saturated unequal floors remain allowed through the original t and p_j data.

## 8. Union control, two-cover necessity and limits

The full outer endpoint-union tuple has transversal exactly two. The selected pair {x_(0,1),x_(2,1)} has footprint A and hits every union, while every singleton's footprint has size at most two and has an actual avoiding union root by section3. Thus no permanently fixed union guard explains the handover.

For singleton one-column endpoints (t=1, all p_j=0), the unique source physical four-cover is K0 and the unique destination physical four-cover is K2. They are distinct. A single physical four-cover cannot serve both endpoints, while the new schedule uses these two throughout. Thus exactly two cover identities suffice and are necessary for THIS singleton schedule. No necessity claim is made with padding or larger groups, where one unchanged cover may exist.

The core new statement is that colored protection DERIVES a compatible actual handover using disjoint cross-anchor witnesses, so shared outside edges and four supplied relay types are unnecessary within the abstract class. Applicable native connectivity was already known; this is a structural completion mechanism and exact minimum, not a new connectivity classification.

Both anchor and outside order are chosen before endpoints. Arbitrary preassigned cycles or exact endpoint pairs, failure of(C), more than one coupled exceptional pair per active exchange, arbitrary ownership graphs and unrestricted mixed/directed/higher-target/nested repair remain open. Unbounded upper-cover stages with several moving lower witnesses also remains open. The next obligation is to transfer several coupled pair protections for a prescribed exchange without the freedom to choose its compatible ordering.

No numerical job, enumeration, implementation, benchmark, integration merge, numbered certification or physical claim is made. Completed v16.54/v16.55, historical method failures and all original evidence are preserved. Separate efficiency runner/fixture/benchmark work remains unstarted.
