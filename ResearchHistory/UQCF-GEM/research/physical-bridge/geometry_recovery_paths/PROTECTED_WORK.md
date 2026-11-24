# Competing last copies can leave a permanent difference in chart-pair work

Two source charts start with equal numerical P1 grades and equal work to a fixed third chart. Each is allowed to delete its own copy of the same leaf. After one deletion the existing work value between charts 2 and 1 is 3. After the other it is 4. These values hold through **every subsequent union-preserving deletion**, including histories that raise the minimum cover size. The third chart's own P1 vector remains (6,1) on both arms. The measured quantity belongs to a pair of charts.

The earlier [same-source result](FLAT_COVER_NEXT_EDIT.md) concerns different leaves at one source. This experiment deliberately varies the source chart while holding the leaf fixed. It uses the original v16.26 deletion rule, the unit-grade incidence embedding, the v15.40 exact work constructor, and v16.25 P1 pushforward. The constructors are called on the states under comparison. No subsequent receiver write, invocation rule, physical measurement or gravitational interpretation follows from this calculation.

## A native fork that cannot rejoin by pruning

Take a finite rooted tree and indexed, root-containing, ancestor-closed chart views. A native atom removes a nonroot local leaf from a chart while keeping the union. Consider two distinct legal atoms at the same preparation.

If they delete different vertices, neither changes the other's surviving holders, and deleting a local leaf cannot add children to either view. If they delete one vertex from different charts and it has at least three holders, a third holder survives. In both cases the other deletion stays legal in each arm and the two orders give the same indexed state. This includes any two distinct cuts at a single source chart. The common state admits a common maximal continuation.

The sole exception is a vertex held by exactly two charts when both copies are locally deletable. It is then a leaf of the union tree. A proper descendant in the union would require one of the two holders to contain a child. Either cut leaves a sole holder. The rule protects that holder for the rest of every deletion-only history. The two arms can never reach the same indexed state. An addition can restore the missing copy.

For clarity about the original caller question, we ran the v16.25 directed refinement code and v16.33 profile-move verifier on archived row 1349 with the original two cuts at chart 2. Directed refinement accepts both first cuts and the cover-raising second cut, and rejects the inverse addition. The profile verifier accepts both first cuts and the inverse as invisible and rejects the second cut as invisible. Its visible classification accepts the second. The v16.25 enumerator returns the whole directed interval. The previously traced v16.43 normalizer binds its covering set before acting. These named calls supply no autonomous commitment to cover-preserving deletion at the original same-chart fork. The competing-last-copy fork needs no such commitment to protect ownership.

## When the ownership survives in the numerical geometry

On a rooted star let each leaf have grade one, with the same source and response membership coordinates used in the archived work embedding. The inherited work is W(i,j) = |Y_i △ Y_j|, counting the leaves in exactly one chart. At a maximal deletion state each leaf has exactly one holder. All such assignments are reachable by retaining each chosen holder and deleting surplus memberships. Writing n_i for the number of leaves assigned to chart i, every off-diagonal entry then equals n_i+n_j. For at least three labeled charts the full work matrix determines every n_i by the identity 2n_i = W(i,j)+W(i,k)−W(j,k) for distinct i,j,k. This count argument uses unit grades. With only two charts the sum need not identify either count.

Fix a disputed leaf v with exactly two holders A and B. Build a graph on charts by connecting any two that co-hold **some other leaf** in the common prior. Then the terminal work families under the two source choices are disjoint **exactly when A and B are disconnected in this graph**.

* **Disconnected owners.** Every other leaf's initial holders lie entirely in one component, so its terminal assignment stays in that component. The total number assigned to A's component differs by precisely one according to who retains v. Equal terminal work would give equal chart counts and hence equal component totals.
* **Connected owners.** In the bipartite incidence graph excluding v, take a simple path from A to B alternating charts and other leaves. The path uses distinct leaves. Assign those leaves successively toward B in the arm where A retains v, and toward A in the arm where B retains v. Give every off-path leaf the same original holder in both arms. All individual chart counts then agree. Both complete assignments are reachable, have different holders of v, and give the same entire labeled work matrix. Other leaves may have more than two possible holders.

In the census with at most three other-than-blank chart labels, a disconnected A and B have at least one singleton owner component. All its other holdings are private and hence immutable. Work from the designated blank chart to this owner counts its leaves at every intermediate state. The two source choices differ by exactly one in that single work entry, even with independently varying schedules and stopping points. In the connected case the terminal collision already disproves such all-stages separation. The terminal theorem above also applies to more charts. Its all-stages strengthening here uses the three potentially active charts and the blank reference.

For a star there is also an exact matched-history check. Switch the sole copy of v between A and B at any downstream state. Every legal edit on any other leaf transports with the same chart and address, since legality is leafwise. This pairs the two remaining transition graphs. If the A-cut arm is compared with the B-cut arm at corresponding states, the signed change in W(i,j) is the indicator that B lies in the pair minus the indicator that A lies in it. This corollary was additionally checked against the complete intervals after the initial census. The disconnection criterion asks the stronger question of whether *any* pair of independently chosen terminal continuations can erase the work difference.

A strictly passive chart has a different status. Even for a general finite rooted tree, each maximal deletion state consists of the root and the prefix paths to the union leaves assigned to each chart. At a terminal state each union leaf has a unique holder. A nonroot local tip that is internal to the union would be removable, since a chart containing its child would cover it. Conversely, keep the paths to any assignment of union leaves to original holders and remove surplus tips in descending depth order. After the two-holder conflict, assign all other union leaves identically on both arms. This gives identical terminal masks at every chart outside A and B. Indeed the possible terminal masks at each such chart coincide. With the same original fine grades, an equal local mask gives the same local P1 vector. A pair work involving one of the owners can carry the distinction while a chart outside the two owners acquires no new singleton P1 entry.

## Two controls on the original four-chart geometry

The original four-leaf preparation is archive row 1349, with leaf sets ∅, {2,4}, {1,2,3}, {3,4}. Let chart 1 or chart 3 delete leaf 4. Both events preserve cover size two. The other duplicated leaves connect the two owners through chart 2. The following reachable terminal states give the same six works in pair order 01,02,03,12,13,23. Only nonroot leaves are displayed.

| Source deleting leaf 4 | Chart 0 | Chart 1 | Chart 2 | Chart 3 | Six works |
|---|---|---|---|---|---|
| Chart 1 | ∅ | {2} | {1,3} | {4} | 1,2,1,3,2,3 |
| Chart 3 | ∅ | {4} | {1,2} | {3} | 1,2,1,3,2,3 |

One common preparatory deletion of leaf 2 at chart 1 reaches archived row 1079. This cuts the alternate overlap path. Chart 1 now holds only leaf 4. After the two competing cuts its work with the blank chart is respectively 0 or 1 throughout. In the first arm two charts coincide and the separated-metric test fails there. The raw work remains defined. From the active bystander chart 2 the difference W(2,1)−W(2,0) is likewise 0 or 1 because charts 1 and 2 have disjoint leaves. This one-edit modification is sufficient, and the terminal collision at row 1349 shows that zero edits there do not suffice. The exact four-leaf row identities and the archive's inverse-addition bits are checked.

## A fixed nonblank bystander and a single nondegenerate work entry

Use four charts on a six-leaf rooted star with unit fine grades also at the root. Chart 0 holds {5}, chart 1 holds {1,4,6}, chart 2 holds {2}, and chart 3 holds {3,4,5}. The two prospective sources each retain three unit leaves and have P1 root 4. The initial work from chart 2 to either is 4. The two source events have the same target address, grade transfer, before and after counting root, false trigger, and unique minimum cover {1,2,3} before and immediately afterward. The numerical P1 values match across source charts; their retained addresses differ.

| Source deleting leaf 4 | Source root | W(2,1) at every later pruning state | Chart 2 P1 | Cover sizes reached |
|---|---|---:|---|---|
| Chart 1 | 4 → 5 | 3 | (6,1) | 3,4 |
| Chart 3 | 4 → 5 | 4 | (6,1) | 3,4 |

Chart 1's leaves 1 and 6 and chart 2's leaf 2 are private. The work between them counts those three leaves and counts leaf 4 exactly when chart 1 retains it. After the source, leaf 5 may stay duplicated or either of its two holders may give it up. Deleting it at chart 3 forces chart 0 into the cover and raises the size to four. All three reachable states in each arm pass the original constructor's symmetry, identity, separation and triangle checks. An inverse addition would return both arms to the common preparation at cover three. The persistence claim concerns arbitrary v16.26 pruning. The experiment varies the source site, and the reported pair has one of those potential source sites as a member.

The prospectively designated five-leaf control omits leaf 6. It gives W(2,1) = 2 or 3 under all the same subsequent deletions. The source root increments agree, while their initial root grades differ. The six-leaf control above removes that difference. These are new applications of the original atom, P1 and work constructor. Original campaign row numbers are reported only for the four-leaf controls.

## Complete finite comparison

| Quantity in the four-leaf, designated-blank class | Count |
|---|---:|
| Preparations / directed native deletions | 2,401 / 12,348 |
| Unordered distinct same-start event pairs | 32,046 |
| Pairs with a common two-step state | 27,930 |
| Mutually exclusive last-copy pairs | 4,116 |
| Exclusive pairs with disjoint work through every remaining deletion state | 1,212 |
| Exclusive pairs admitting equal complete terminal work | 2,904 |

For each of four disputed labels and three possible holder pairs the remaining three leaf supports admit 7³ words. To disconnect A from B, no remaining support may contain both. The five eligible supports are A, B, C, AC, BC. At least one of AC and BC must be absent. This gives 4³+4³−3³ = 101 choices per disputed label and owner pair, or 1,212 in all. These are input counts; they have no assigned occurrence probabilities.

The producer executed the v16.26 atom and its original verifier on every eligible edge and constructed the labeled work matrix with v15.40 on every census state. The independent calculation reconstructed the entire universe from arbitrary chart masks, submask intervals, terminal assignments and separating partitions. It checked exact event pairs, common states, work matrices, terminal and intermediate collisions, numerical controls and archive identities. Physical access to a pair work and the occurrence of either source cut remain open.

[Main preregistration](PROTECTED_WORK_PLAN.md) · [Equal-source control](PROTECTED_WORK_EQUAL_SOURCE_PLAN.md) · [Certificate](protected_work_certificate.json) · [Full finite evidence](protected_work_universe.json.xz) · [Historical replay](check_protected_work.py) · [Independent reconstruction](verify_protected_work.py)
