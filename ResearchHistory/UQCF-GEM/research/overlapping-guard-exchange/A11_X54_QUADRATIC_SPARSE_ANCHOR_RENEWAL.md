# A11.X54 — Quadratic sparse anchor renewal

Status: frozen analytical candidate; independent review pending. Parent: 89b29986c918d06e9376629c7fcbba481bbf821d. Scope: A11_X54_SCOPE.md at d60aba9edf15c72672a8fc946f5710336400ce58. No numerical execution, implementation certification, or universal connectivity claim.

## Statement and native carrier

Let m>=10, G={0,...,m-1}, A={0,1,2,3}, R=G\\A, and n=m-4. There is one type Q={a,u,v} for every a in A and unordered pair {u,v} in R. Each type has an arbitrary positive number c_Q of ORIGINAL labelled root copies. Thus the distinct type count is 4 binom(n,2)=2n(n-1), with constant role width three.

Fix t>=1 and disjoint original labels x_(j,h), j in G, 1<=h<=t, and original padding sets Z_j, |Z_j|=p_j>=0. Source groups are B_j=Z_j union {x_(j,h):1<=h<=t}; destination groups are D_j=Z_j union {x_(j-1,h):1<=h<=t}, indices modulo m. The fixed palette is their union. Each source root of type Q is union_(j in Q) B_j; its EXACT labelled destination is union_(j in Q) D_j. Each original copy retains its own positive floor f_i<=N_Q=3t+sum_(j in Q)p_j. In particular floors at least three and saturated unequal floors are permitted.

These endpoints admit an explicit finite primitive path with 3<=tau<=4 throughout, restoring every labelled destination support. No labels, root slots, or floor changes are introduced. The path changes each differing endpoint incidence exactly once, and no other incidence; it is globally shortest in primitive incidence count for this endpoint pair. For one copy per type its length is 12t(n-1)^2.

The structural advance is replacing the dense complementary-root carrier by quadratically many constant-width types, with a moving lower witness and a deterministic five-stage upper-cover handover. Complete outside-pair coverage is still an explicit hypothesis. This is not arbitrary sparse-mask accessibility or a new classification of native connectivity.

## Exact endpoints

Every group remains nonempty. A role set hits all types iff it meets every {a,u,v}. The four anchor roles hit all types. If a role cover of size at most four omits anchor a, its outside roles must hit all pairs of R. That needs at least n-1>=5 outside roles, impossible. Consequently every role cover of size at most four equals A, and the transversal is exactly four. Actual minimum covers select one existing label in each anchor group. Multiple labels in one group cannot improve role coverage.

This reasoning applies to the source, destination, and every completed column exchange: group cardinalities remain t+p_j and the same type system persists.

## Pair protection and its single exception

Exchange columns h in order. At the beginning of a column, its selected label x_(j,h) still has owner j; its required owner is j+1. Labels in other columns and padding retain their current owners during this exchange.

For any role footprint F of size at most four other than A, choose an anchor a outside F and two outside roles u,v outside F. Such choices exist since n>=6. The actual root type {a,u,v} avoids F. If F=A no type avoids it.

For a physical pair K, combine each label's current and required owners for this column. A nonselected label contributes one owner; a selected label contributes {j,j+1}. The combined footprint has size at most four. It equals A only for the selected pair K*={x_(0,h),x_(2,h)}: a four-role footprint requires two selected labels, and the only two disjoint directed consecutive edges covering A start at 0 and 2. Every other pair therefore has an actual root whose ENTIRE old/new support union avoids K. Such a witness remains valid even while that root is edited.

For K*, use u*={1,4,6} and v*={2,5,7}. A source copy of u* avoids its old owners {0,2}; a completed destination copy of v* avoids its new owners {1,3}. Neither is a common witness. We complete every v* copy before starting u*, leaving an untouched old u* copy until a new v* copy exists. That new copy persists thereafter. This proves the lower guard for ALL physical pairs, including anchor/anchor, mixed, outside/outside and same-group pairs. No capacities are assigned independently to overlapping obligations.

## Three upper covers and five stages

Write a selected-label cover by its source indices:
K0={0,1,2,3}, L={0,2,4,6}, K2={m-1,0,1,2}.
Their destination owner sets are respectively {1,2,3,4}, {1,3,5,7}, A.

Let U be the type set missed by a cover in old supports and V the type set missed in new supports. Directly:
U0=empty;
V0={ {0,u,v}: {u,v} avoids 4 };
U1={ {a,u,v}: a in {1,3}, {u,v} avoids {4,6} };
V1={ {a,u,v}: a in {0,2}, {u,v} avoids {5,7} };
U2={ {3,u,v}: {u,v} avoids m-1 };
V2=empty.
Here "avoids" means neither outside role is in the listed set.

Put b={0,5,7} and c={3,4,6}. Process the following disjoint stages, in any fixed order inside each stage:
1. v*={2,5,7}.
2. Every type in U1.
3. b.
4. Every still unprocessed type in U2.
5. Every remaining type.

Indeed v* belongs to neither U1 nor U2; b belongs to neither source set. No type in stages 1 or 2 belongs to V0; b is the first V0 type. No type in stages 1 through 4 belongs to V1: stage 2 uses anchors 1/3, stage 4 uses anchor 3, and v* and b contain outside roles 5,7. Every U1 precedes every V0; every U2 precedes every V1. Also u* is in stage 5, so v* precedes u*. The type c is in stage 4 (it is not U1 and avoids m-1 because m>=10).

Use physical cover K0 in stages 1 and 2, L in stages 3 and 4, and K2 in stage 5. Each chosen cover hits all completed new supports, all unprocessed old supports, and BOTH endpoints of every active root. For K0 no new exception V0 has begun. For L all old exceptions U1 have finished and no new exception V1 has begun. For K2 all old exceptions U2 have finished and there are no new exceptions.

Process all original copies of an active type consecutively. In each root add every missing new incidence before removing every old-only incidence, one incidence at a time. Until additions end it contains its old support; during removals it contains its new support. The selected cover therefore hits the root throughout. Its size never drops below N_Q, hence never below its own original floor. It stays inside the fixed palette and the endpoint union. All pair witnesses from the preceding section consequently remain actual. Together these facts prove 3<=tau<=4 after EVERY primitive, with shared labelled roots treated once, not as separate capacities.

## Renewal, eligible continuation, termination and restoration

Each stage supplies a finite explicit list of existing types, each with its original finite list of copies and a finite add-before-delete list. Whenever this column is unfinished the next pending incidence in these lists is eligible by the preceding proof; an empty list is skipped. Pending edits decrease at each primitive. Every nonempty proper Q crosses a boundary of the full directed cycle, so each root has actual additions and removals.

At a completed column, each role again has t+p_j labels; every root again has its prepared type support and size N_Q. Exact four and the same pair-witness derivation are restored. If a column remains, its selected labels have not yet moved, so precisely the same construction applies with those labels. This is reusable renewal with no reserve spent.

The count of selected labels still at wrong owners is m(t-h) after h columns, strictly decreasing by m at each finite exchange. All t columns finish. Padding stays fixed; every column label reaches its prescribed owner; each ORIGINAL labelled copy equals its exact prescribed destination support. For t>=2, after the first column every root can differ from both outer endpoint supports while the mechanism remains reusable. This is not whole-root completion relative to those outer endpoints.

## Exact primitive minimum

For each selected label its source and destination owners determine its incidence in every root. If both owners lie in Q it is common and untouched; if neither does it stays absent; if exactly one does it toggles once in its column. Padding is untouched. Thus the total length is
sum_Q c_Q |E_Q symmetric-difference C_Q|
= t sum_Q c_Q |Q symmetric-difference (Q-1)|.
Every primitive changes only one incidence, so every path between these exact supports has at least this length. Our path attains it. Q+1 gives the same aggregate distance if the shift convention is reversed.

For one copy per type, each |Q symmetric-difference (Q-1)|=6-2e(Q), where e(Q) counts cyclic adjacent pairs inside Q. Outside adjacent pairs contribute 4(n-1) over the types; the two anchor/outside boundary pairs {3,4},{m-1,0} contribute 2(n-1); no type has two anchors. The sum is 6(n-1). Therefore the per-column count is 6[2n(n-1)]-12(n-1)=12(n-1)^2. Uniform d copies multiply by d. These are analytical counts, not executed benchmarks.

## No permanent union guard; precise three-cover control

The full outer endpoint-union family has transversal exactly two. The pair {x_(0,1),x_(2,1)} hits every root union because its combined owner footprint is A. No singleton hits all unions: its footprint has size at most two (one for padding), and the common-witness choice above supplies an actual union root avoiding it. Thus lower protection is genuinely transferred; a permanently fixed union guard is unavailable.

In the singleton one-column control t=1, all p_j=0, the unique physical four-label source cover is K0 and the unique destination cover is K2. Immediately after stage 3 and before stage 4, K0 misses the new b root (new owners of K0 are {1,2,3,4}), while K2 misses the still-old c root. Hence no family of two physical four-label covers covers this entire specified schedule: such a family must contain both unique endpoint covers. The three displayed covers suffice, so three is exact for THIS schedule. This does not exclude a different order or prove an all-order obstruction, and is not claimed for larger groups where additional covers may exist.

## Dependencies, limits and next obligation

The argument supplies its own actual lower and upper witnesses, primitive legality and continuation; it instantiates the X51/X52 multicover handover interface without requiring order averaging. It does not invoke band conversion or compact endpoints. Floors belong to the same original labelled copies throughout; no mixed-floor slot permutation is assumed.

Underlying native connectivity of applicable symmetry/uniform classes was already accepted (including the X15 uniform-floor-three result and inherited symmetry methods). New content is this sparse renewable mechanism, explicit compatible order and incidence-minimum construction, not re-certification of connectivity. The dense X39 complementary carrier has role width m-3; here every type has width three and only quadratic many types. X53 still used a dense complementary carrier after omissions.

The outside-pair family is complete on R; arbitrary missing types, multiple coupled exceptional pairs, arbitrary owner changes, and arbitrary unequal corresponding group counts are not proved. Role cyclic order describes the supplied exchange, not new admissibility geometry. Stronger derived bounds and reusable multiple-overlap handovers beyond this single exceptional obligation remain the mathematical direction. Separate efficiency implementation/fixtures/benchmarks remains unstarted and out of scope. Certified v16.54/v16.55 and frozen inherited sources/evidence are unchanged.
