# A native joint reading distinguishes two cover-matched source cuts

The same retained receiver and source can give different joint root grades after two equally graded source deletions. In the four-leaf example the old v16.23 function returns 4 after deleting leaf 1 and 3 after deleting leaf 2. Both atomic events preserve cover order 2, and every chart has the same ordered numerical payload in the two histories. Only the source changes its retained address list. The receiver alone keeps its complete prior state.

## Premises and operator boundary

| Status | Object used here |
|---|---|
| INHERITED | Finite rooted tree with one common Genesis, indexed root-containing prefix views, and P1 pushforward to the nearest retained ancestor. v16.23 gives unique compatible gluing on a union. v16.26 deletes one duplicated source leaf while preserving the full-family union. |
| ACCEPTED-CONDITIONAL | Grades are exact extensive rational amounts. A single fixed strictly positive fine assignment generates all views in a comparison. Positive gluing checks the nonnegativity of its output. |
| DERIVED | A star's original resolved root reading, its loss under a cut, and the constraint on a receiver if this reading is restored. The witness receiver is identifiable before the event among minimum two-chart partners of the specified source. |
| SUPPLIED FOR THE EXPERIMENT | Which legal source cut occurs, and evaluation of the existing binary reader on the indicated pair. The archived source event returns an updated family and a certificate. The archived reader takes both views and returns a vector. |
| OPEN | A native event-dependent call or rule that places this distinction in a persistent record accessible at the receiver without supplying a joint source read or a restoration objective. |

Historical checkpoint is `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`. The two prospective records are `7b83a729f7d40f53fbad1a002010ff65a3e44ce4` and `fc66b066ba952b99cbebd099c3112c8f9d1b4f1d`. The second states exactly what had already been computed.

## Two source events with the same recorded cover measurements

Write R for chart 0, S for chart 1 and H for chart 2. Every chart includes the root. The fine grade is 3 at the root and 1 at each of four leaves. The following are the pre-event leaf sets.

| Chart | Leaves |
|---|---|
| R | 2, 3 |
| S | 1, 2, 4 |
| H | 1, 4 |

R alone holds 3. The minimum two-chart covers are {R,S} and {R,H}, so R is the unique minimum-cover partner of the specified source S. Fix this pair before choosing the cut. S can legally remove 1 or 2 in the same initial configuration. The two histories have identical starting grade, views and source identity.

| Quantity after the cut | S drops 1 | S drops 2 |
|---|---:|---:|
| Transferred grade | 1 | 1 |
| Ordered local numerical payload of each of R, S and H | (5,1,1) | (5,1,1) |
| Local cover and global consistency orders, before and after | 2 to 2 | 2 to 2 |
| v16.26 trigger | false | false |
| Common-intersection root grade | 6 | 7 |
| Joint root returned by v16.23 on R,S | **4** | **3** |
| Root from all three charts | 3 | 3 |
| Grade pushed to the root-only view | 7 | 7 |

The existing binary glue forms the sum of the two local data on their union and subtracts the common data on their intersection. After S drops 1, R and S share root and leaf 2. The common root amount is 7 − 1 = 6, giving 5 + 5 − 6 = 4. After S drops 2, the intersection contains only the root. Its amount is 7, giving 5 + 5 − 7 = 3. The complete labeled source record distinguishes the cuts. Every nonsource chart has identical labeled inputs across them. Applying the pair reader to R and H alone yields the same result in both histories.

A separate prior-unique construction has six leaves. R holds 2,3,4; S holds 1,2,5,6; H1 holds 1; H2 holds 2. The fine grade array is (3,2,2,1,1,1,1). Private leaves on both R and S make {R,S} the unique minimum cover overall. Two grade-2 deletions by S give local roots 7 and 7 in both histories. The pair roots are 5 and 3. The post-cut cover orders here are 3 and 2. If leaf 2 is initially removed from R so both marked leaves are exclusive to S within the pair, the same two cuts give pair roots 5 and 5. Those pair unions still have different labeled domains.

## What one reading requires at any later endpoint

On a star let the fine root amount be g(o) and leaf amounts g(l). For U = R ∪ S, P1 sends every missing leaf to the root. Gluing coherent chart data gives exactly P_U g. Consequently the returned root is

\[
   (P_U g)(o)=g(o)+\sum_{\ell\notin U}g(\ell).
\]

Suppose the prior pair covers the full star and the same fine assignment is strictly positive on the leaves. Exact return of the pair's original raw root value is equivalent to retaining every leaf in that same pair. If S keeps leaf j removed, **every** endpoint with the original raw reading has j in R. There is no path-length, minimum-cover, shortest-repair or receiver-capacity premise. If every other leaf remains covered, adding j to R suffices, and also restores the full original fine record on the pair. With the whole family still covering the star, the current full-family glued root provides the same numerical reference as the old root. A fixed fine grade and the condition that the pair should reproduce that reference are separate premises.

For the two-exclusive-leaf example, two permitted additions copy R's private leaves 3 and 4 to H1 after S drops 1. The family again has a two-chart cover {S,H1}, while the fixed R,S root still reads 5. Returning 1 to S instead restores the pair reading with R unchanged. Keeping the source cut and adding both marked leaves to R in both histories restores the original pair reading and produces identical final receiver records. These examples distinguish a forced inclusion conditional on fidelity from unique event decoding at an arbitrary endpoint. A zero missing grade hides a cut. Signed grades +2 and −2 can hide two missing leaves by cancellation.

The source deletion and positive gluing both succeed with a stationary receiver and an increased pair root. Positive compatibility across all charts survives because their local data are restrictions of the same fine grade. The archived `atomic` replaces only `zs[index]` and returns a certificate. The archived `glue` consumes two views and returns a tuple on their sorted union. Neither function requests a receiver edit or compares the new root with its previous value. This is a counterexample to compulsion from these two operations and their compatibility conditions alone.

## Which information the joint reader retains on a general tree

Let the atom vector range over strictly positive rational assignments on a fixed finite rooted tree X. For each node v let c(v) be its full-subtree grade. The transformation from atom grades to the c coordinates is invertible by subtracting the sums at the immediate children. On a retained prefix view V, P1 preserves c(v) for every v in V. The projected atoms on V recover those same coordinates by subtree summation. Thus the pair of retained views recovers exactly the coordinates indexed by U, its union. Its information is exactly that of P_U. An output with union B determines the entire raw observation on a fixed pair with union A for all fine grades if and only if A is contained in B. Sufficiency follows by restriction from B. Roots are always present. For necessity choose v in A outside B and perturb the fine grade by +1 at v and −1 at its parent, starting from all 2. Both assignments are strictly positive. Every chart in the B pair sees the same values because the two nodes project to the same address. Some chart in the A pair contains v and distinguishes them. The two assignments also have equal total grade.

For a single lost leaf j of the pair union, its *union atom* moves to its parent, which remains in the union. For a true leaf of X this is precisely g(j). A cut deeper in a tree can leave the root grade unchanged. With parents (−1,0,1,1) and fine grade (3,4,2,2), removing leaf 2 from the pair changes the joint vector from (3,4,2,2) to (3,6,2) on the remaining addresses. The surviving parent at node 1 records the increase.

If a star's original {R,S} is globally the unique minimum pair, deleting an exclusive leaf breaks that pair, and deleting a leaf shared with R preserves it. A deletion only removes incidences and cannot create any other full pair. In this case a mixed shared/exclusive contrast necessarily changes the post-cut cover order between arms. An alternative prior cover permits the two orders to match, as in the four-leaf witness. The existence of a distinct joint reading thereby survives matching all six numeric/Boolean cover fields of the source event.

## Exact enumeration

| Check | Result |
|---|---:|
| Prior four-leaf, three-chart states whose fixed pair covers the star | 1,296 |
| All globally covering four-leaf, three-chart endpoints | 2,401 |
| Legal source deletions with complete R record unchanged | 2,592 / 2,592 |
| Equal-grade, common-prior pairs with identical ordered local payloads on every chart | 1,944 / 1,944 |
| Pairs distinguished by the fixed joint root | 864 |
| Distinguished pairs also identical on both cover orders, the increment and the trigger | 816 |
| Of those 816, cases where R was S's unique prior minimum-pair partner | 216 |
| Of those 816, cases where {R,S} was the globally unique prior minimum pair | 0 |
| Ordered-parent-array trees through five vertices | 34 |
| Ordered pairs of views / comparisons between distinct union identities, including equality | 2,551 / 2,551 |
| Strictly positive separating witnesses for failure of factorization | 1,480 |

All comparisons above are labeled and exact. The tree comparison counts include each ordered pair of possible unions on each parent array, including a union compared with itself. The native producer forms matrices from basis-vector pushes and computes exact ranks. The independent checker reconstructs every identity by subtree sums, a separate chart-subset enumeration and the union criterion. The supplement separately reconstructs the partition of all 1,944 comparison identities. Ten evidence mutations test rejection. Complete raw identities are in `fixed_pair_universe.json.xz` and `fixed_pair_matched.json.xz`. The raw primary JSON SHA-256 is `7287e1013c05b3b6a32642f936184b923d4cd16ed1d4e9d2964852feb536e7b9`.

The remaining scientific test is whether an already-invoked operation, given these cover-matched source alternatives, makes the address difference available in state held by a nonsource receiver after the joint source input is withdrawn. The present root contrast is directly computed on the fixed pair.
