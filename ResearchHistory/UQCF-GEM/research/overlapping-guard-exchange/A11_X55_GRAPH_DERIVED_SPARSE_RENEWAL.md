# A11.X55 — graph-derived sparse witness renewal

Status: frozen analytical candidate; independent review pending. Parent b94c9952c79b397986f35a19645f8bec533d8659. Scope A11_X55_SCOPE.md at 9ed853bb880f4634c70a9f1baf5299c9decf0bed. No numerical execution, implementation certification or universal connectivity claim.

## Theorem

Let m>=10 and let an abstract simple graph Gamma on m-4 outside roles have vertex-cover number vc(Gamma) at least five. Before defining endpoint groups or the successor exchange, choose a compatible labeling G={0,...,m-1}, A={0,1,2,3}, R=G minus A such that {4,6} and {5,7} are graph edges and m-1 is not in {4,6}. For every a in A and e in E(Gamma), declare the ACTUAL root type Q={a} union e, with an arbitrary positive number c_Q of ORIGINAL labelled copies.

Fix t>=1 disjoint original column labels x_(j,h), j in G and 1<=h<=t, and disjoint fixed original padding sets Z_j of sizes p_j>=0. Source groups are B_j=Z_j union {x_(j,h):1<=h<=t}; destination groups are D_j=Z_j union {x_(j-1,h):1<=h<=t}, with indices modulo m. Every source copy of type Q has support union_(j in Q) B_j and exact labelled destination union_(j in Q) D_j. It retains its own original positive floor f_i<=N_Q=3t+sum_(j in Q)p_j.

There is an explicit finite primitive path between these exact-four endpoints with 3<=tau<=4 after every edit. It restores every exact labelled destination support, changes each differing endpoint incidence exactly once and no other incidence, and therefore has globally minimum primitive length for the endpoint pair. The same construction resolves all t columns and permits arbitrary unequal p_j and arbitrary unequal original copy floors, including saturation.

The number of distinct types is 4|E(Gamma)|. In particular, for every m>=14 a compatibly labeled five-edge matching (plus isolated outside roles) gives only 20 types, independent of m. This is the minimum type count within the theorem's graph condition because vc(Gamma)<=|E(Gamma)|.

## Existence and timing of the compatible labeling

The endpoints of any maximal matching cover every graph edge. If the maximum matching had size at most two, Gamma would have a vertex cover of size at most four, contrary to hypothesis. Hence Gamma has three pairwise disjoint edges.

For an abstract Gamma, choose two of them and label their endpoints e_u={4,6} and e_v={5,7}. Label an endpoint of the third edge m-1, so m-1 is not in e_u; label the remaining outside vertices arbitrarily. ONLY AFTER this labeling is fixed do we declare B_j,D_j and the numeric successor j->j+1. Therefore every abstract Gamma with vc>=5 supplies at least one compatible cyclic exchange in the theorem. The theorem does not assert the construction for every cyclic order assigned to Gamma in advance.

## Exact-four prepared states

The anchor set A hits every type. Suppose a role set S of size at most four omits anchor a. To hit every type {a} union e, its outside part S intersect R must meet every graph edge. That would be a vertex cover of size at most four, impossible. Therefore the only role cover of size at most four is A itself.

Every role group is nonempty. Selecting one physical label from each anchor group gives a four-label hitting set, while a physical cover of size at most four projects to a role cover of the same or smaller size. Every source, destination and completed-column prepared state consequently has transversal exactly four. Copies and padding do not change the conclusion.

## The derived actual pair guard

Resolve one column h at a time. Before its exchange, selected x_(j,h) has owner j and requires owner j+1. Other labels keep one current owner during this exchange.

Let F be any role footprint of size at most four with F!=A. Choose an anchor a outside F. Because |F intersect R|<=4<vc(Gamma), it is not a vertex cover; some actual edge e of Gamma is disjoint from F. The actual type {a} union e avoids F.

For any physical pair K, take the union of the current and required owners of its labels in this column. An ordinary label contributes one role and a selected label contributes the consecutive pair {j,j+1}, so the footprint has size at most four. It equals A only if both labels are selected and their two directed consecutive edges partition A. Since m>=10, this happens only for
K*={x_(0,h),x_(2,h)}.
Every other physical pair has an actual type whose full old/new support union avoids it. Every copy of that type remains inside the union throughout add-before-delete editing, so an actual witness persists even when that type is active.

For K*, the old actual type u*={1,4,6} avoids owners {0,2}, and the completed new actual type v*={2,5,7} avoids owners {1,3}. Complete all v* copies before changing any u* copy. Until the first v* copy is complete, an untouched u* copy supplies protection; afterward the completed v* copy supplies it permanently. Thus every physical pair has an actual missed root at every primitive. This proves tau>=3 without treating shared roots as independent capacities.

## Compatible five-stage upper handover

Use the physical selected-label covers, written by source indices,
K0={0,1,2,3}, L={0,2,4,6}, K2={m-1,0,1,2}.
Their destination owner sets are {1,2,3,4}, {1,3,5,7}, and A.

Within the restricted actual type set, let U_j be types missed by the old support of cover j and V_j types missed by its new support. Directly:
- U0 is empty;
- V0 consists of actual {0} union e with 4 not in e;
- U1 consists of actual {a} union e with a in {1,3} and e disjoint from {4,6};
- V1 consists of actual {a} union e with a in {0,2} and e disjoint from {5,7};
- U2 consists of actual {3} union e with m-1 not in e;
- V2 is empty.

The four actual types
v*={2,5,7}, u*={1,4,6}, b={0,5,7}, c={3,4,6}
exist because e_u,e_v are graph edges. Process disjoint stages:
1. v*;
2. every actual type in U1;
3. b;
4. every still-unprocessed actual type in U2;
5. every remaining actual type,
using any fixed order within a stage.

The membership checks are literal. v* is in neither U1 nor U2. b is in neither source-exception set. Stages 1 and 2 contain no V0 type; b is the first possible V0 type. Stages 1 through 4 contain no V1 type: stages 2 and 4 use anchors 1/3, while v* and b contain both 5 and 7. Hence every U1 precedes every V0 and every U2 precedes every V1. Also v* precedes u*. The type c lies in stage 4 because e_u avoids m-1 and meets {4,6}, so it is U2 but not U1.

Use K0 through stages 1 and 2, L through stages 3 and 4, and K2 through stage 5. During K0, no new exception V0 has begun. During L, all old exceptions U1 are complete and no V1 has begun. During K2, all U2 are complete and V2 is empty. The chosen cover hits all unprocessed old supports, all completed new supports and both endpoints of every active type.

Process all copies of a type consecutively. For one copy, add all missing destination incidences one at a time, then remove all old-only incidences one at a time. It contains its full old support through additions and its full new support through removals. Its size never falls below N_Q and hence never below its own original floor. Every edit stays in the fixed palette. The upper cover and lower actual witnesses therefore coexist on the SAME literal primitive sequence, proving tau<=4 and tau>=3 after every edit.

## Renewal, next-edit existence and completion

Every stage is a finite explicit list of existing types, copies and incidences. Empty lists are skipped. Whenever a column remains unfinished, its first pending literal edit exists and is legal by the preceding argument; the total pending-edit count decreases at every primitive.

After a column completes, every role again contains t+p_j labels and every root again has its prepared type support of size N_Q. Exact four, the graph guard and the same two-edge handover are renewed. If another column remains, all its selected labels still have their original current owners. Apply the same five-stage exchange again.

After h completed columns, exactly m(t-h) selected labels remain at wrong owners. This decreases by m after each finite exchange and reaches zero. Padding never moves. Every ORIGINAL labelled root copy reaches its exact prescribed destination. For t>=2, after the first column every root differs from both outer endpoint supports: every nonempty proper Q has a cycle boundary, so the first column has changed an incidence and a later column retains the corresponding pending change.

## Global incidence minimum

For selected physical label x_(s,h), source membership in a type Q is 1_Q(s) and destination membership is 1_Q(s+1). Common incidences and absent incidences are untouched; every differing incidence toggles exactly once in its column. Therefore the full path length is
t sum_Q c_Q |Q symmetric-difference (Q-1)|,
which equals the endpoint Hamming distance and is a lower bound for every one-incidence path between the exact supports. The construction is globally shortest, not merely columnwise shortest.

For one copy of each type, let q=|E(Gamma)|, let a(Gamma) count graph edges joining consecutive outside roles in the cyclic role order, and let d_4,d_(m-1) be the graph degrees of outside roles 4,m-1. Summing cyclic adjacent pairs inside Q gives
sum_Q |Q symmetric-difference (Q-1)|
=24q-8a(Gamma)-2(d_4+d_(m-1)).
Thus the t-column minimum is t times this expression. This is an analytical identity, not an executed benchmark.

For every m>=14 choose the five-edge matching
{4,6},{5,7},{8,10},{9,12},{11,13} when m=14,
and
{4,6},{5,7},{8,10},{9,11},{12,m-1} when m>14,
with all other outside roles isolated. It has vc=5, no consecutive outside edge, and d_4=d_(m-1)=1. It supplies exactly 20 distinct root types and the exact one-copy length 116t. Five edges are necessary under vc>=5, so 20 is type-minimal within this one-anchor-per-edge theorem.

## Controls and exact limits

The full outer endpoint-union tuple has transversal exactly two. The physical pair {x_(0,1),x_(2,1)} hits every union because its role footprint is A. Every singleton has footprint of size at most two and is avoided by the graph-derived actual union witness. Thus protection is transferred; no permanent union guard exists.

In the singleton one-column control t=1 and all p_j=0, the unique physical endpoint covers are K0 and K2 because A is the unique role cover of size at most four. Immediately after b completes and before c starts, K0 misses new b and K2 misses old c. Any two-cover family valid throughout this specified schedule must contain both unique endpoint covers, so it fails at that boundary. K0,L,K2 work, making three exact for THIS schedule only. No other-order obstruction is claimed.

The theorem replaces complete outside-pair coverage by the sharp proof-level condition vc(Gamma)>=5. In the five-matching control a four-role outside footprint can leave exactly one matching edge unhit; this is not a claim that minimum old/new pair-root redundancy equals one. It still assumes every anchor-edge combination, equal corresponding endpoint group sizes, supplied parallel full-cycle columns and a compatible graph labeling chosen before those endpoints and the successor map are declared. It does not prove arbitrary missing anchor-edge types, several coupled exceptional pairs, arbitrary ownership graphs, or universal mixed-floor, directed, higher-target or nested repair. Applicable native connectivity was already known; the result is a sparse renewable schedule and exact minimum, not a new connectivity classification.

No numerical job, implementation, benchmark, integration merge, numbered certification or physical claim is made. v16.54/v16.55 and all frozen evidence remain unchanged. The next mathematical obligation is to allow missing anchor-edge combinations or several genuinely coupled exceptional pairs without losing actual witness renewal. Unbounded upper-cover stages with moving lower witnesses also remains open. Separate efficiency runner/fixture/benchmark work remains unstarted.
