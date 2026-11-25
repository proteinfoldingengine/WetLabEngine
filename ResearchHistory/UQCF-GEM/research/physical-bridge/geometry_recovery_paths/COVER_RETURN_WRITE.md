# When restoring coverage forces the receiver to acquire the released leaf

A source can release either of two leaves from one common star and one common receiver prior. In the two-chart construction below, either release raises the minimum cover from two to three. If the cut remains in force, **every one-edit return to two writes the released leaf onto the same other chart**. A separate existing routine actually checks the cover, chooses the donor and recipient from the live state, and makes that write in the displayed chart order. Leaving the atlas at cover three is legal. What would make cover restoration compulsory in physical dynamics remains open.

The address passes through the holding relation. No elapsed time, pair-work value, candidate leaf or receiver index is passed into the packet selection. The target cover and invocation of the procedure are inputs. All references to a first or subsequent edit mean order in a sequence of single incidences.

## A state-triggered caller on the previous star

The existing v16.54 M1 layers dispatcher computes the minimum number of charts covering the current leaves. On its forward leg it repeats a copy operation while this number exceeds the supplied target. It chooses the first two labels x,y in a minimum cover, breaking ties by label order. The operation copies to chart x every leaf of y that x lacks. The reverse leg uses the last two labels in reverse order. The routine then rewrites the path between these two completed endpoints. The post-source state is the initial state of each internal leg. The first vertex of the *returned* path is the completed forward-leg endpoint. These distinctions matter for interpreting a write.

Apply that exact dispatcher with target three to the previous six-leaf star. Original chart holdings, with the common root omitted, are {5}, {1,4,6}, {2}, {3,4,5}. Three equals the original cover, measured before either source choice. The chart-3 choices both transfer one unit to the same source root, from 4 to 5, and leave both bystanders' local priors unchanged.

| Source cut from the common preparation | Cover after cut | Actual forward-leg action |
|---|---:|---|
| Chart 1 drops leaf 4 | 3 | No edit |
| Chart 3 drops leaf 4 | 3 | No edit |
| Chart 0 drops leaf 5 | 3 | No edit |
| Chart 3 drops leaf 5 | 4 | Chart 0 gains leaves 1, 4 and 6 from chart 1 |

These are all four legal deletions. The forward and reverse loops are dormant on the original prior. In the crossing arm the reverse leg also runs and chart 3 copies leaf 2 from chart 2. Chart 2's own holdings remain {2} throughout this routine in the original labels. Swapping labels 0 and 2 throughout the input makes the transported original chart 2 the receiving chart on the forward leg. Palette order is an actual choice in the archive.

For the [previous protected leaf-4 fork](RECEIVER_SPARE.md), both terminal four-cover states activate this dispatcher at target three. Neither marked deletion is the threshold crossing once the common cut of leaf 5 has already occurred. A separate order-independent distinction appears immediately in the original chart 2's admissible edits. Among the five leaf additions at chart 2, the ones preserving cover four are {1,3,4,6} after the chart-1 cut, versus {1,4,6} after the chart-3 cut. All five are union-preserving additions in both arms. Since every leaf has a single holder here, an additional copy reduces the cover exactly when its prior holder has no other leaf. The original v16.33 exact-profile adjacency and the inverse v16.26 atoms agree. This distinguishes one constraint on local actions without showing that chart 2 reads that constraint or acts on it.

## A forced location and an actual write

Use charts R=0, A=1, B=2, S=3. S holds marked leaves 1 and 2 and its private leaves 3 and 4. A also holds 1 and B also holds 2. R holds private leaves 5 and 6. All charts contain the root. The only two-chart cover is {R,S}. The source S now relinquishes leaf 1 or 2. In either case its unit-grade root goes from 3 to 4. R still has its entire original P1 state (5,1,1). In the two histories the newly necessary third chart is A or B respectively.

| Source event | Unique post-source minimum cover | First forward copy | R's marked set at the one-edit return |
|---|---|---|---|
| S releases leaf 1 | {R,A,S} | R copies leaf 1 from A | {1} |
| S releases leaf 2 | {R,B,S} | R copies leaf 2 from B | {2} |

The common value two was supplied to the existing layers dispatcher in this new input. It agrees with the pre-source cover in both arms. Its ordinary state test is false before the source and true afterward. The two chart choices come from the computed minimum cover in each actual run. The two numerical P1 arrays of R after the write are both (4,1,1,1); the leaf addresses differ. With the target instead set to three, neither packet leg runs on these same post-source states.

**Why every one-edit repair agrees.** Deleting memberships cannot reduce the minimum cover while preserving the union. After a single addition, R and S each still have at least one privately held leaf. Any restored two-chart cover must therefore be {R,S}. Their combined holdings miss exactly the leaf S released. The only two successful additions are returning that leaf to S or giving it to R. Keeping the specified cut excludes the first. This proof does not depend on chart or leaf ordering, a donor scan, a prespecified recipient, or an instruction to copy a particular leaf.

For three initially mandatory charts, put two more private leaves at D=4. The archived M1 target three now agrees with the original pre-cut cover. The two source cuts take it to four. The same unchanged forward loop again copies the released address to R in the displayed ordering. A single addition restoring cover three must still copy that address, but either R or D can receive it while preserving the source cut.

More generally, with q mandatory charts and two contested leaves, let b be the number of nonsource mandatory charts with just one private leaf. Assume each mandatory chart has at least one private leaf. There are exactly q(1+b) one-edit returns after either source cut. In the post-cut state the old q mandatory charts and the helper that now solely holds the released address each have a private witness. A one-edit return must remove the necessity of one of these q+1 charts; the remaining q must form the new cover. Omitting the helper gives q recipients for its sole leaf. Omitting a nonsource mandatory chart with one private leaf gives q recipients for that leaf. An anchor with two private leaves cannot be omitted by one addition. Omitting S leaves at least its private leaf and the other contested leaf uncovered by the remaining q charts since the other helper is absent. Thus S cannot be omitted even when it has just one private leaf. Exactly one successful addition reintroduces the removed incidence at S. Equivalently, the complete one-step return set is obtained by inspecting every q-chart team that currently misses exactly one leaf and adding that leaf at one member. The independent computation uses this latter characterization.

## How strongly the receiver is forced if more edits are allowed

Let R have n private leaves and S have m private leaves, both positive. S initially holds N marked leaves (N at least two). Each mark has its own helper, which initially holds only that mark. R holds no mark. Fix any released mark j. Count single-membership edits after S releases j and keep that incidence absent from S. The minimum number of further edits to first return to cover two with j absent from R is

**d = min(n, m + N − 1).**

The same minimum holds if R is required to make no edit at all. To see the lower bound, the covering pair at such an endpoint cannot be {R,S}. A pair consisting of S and a helper originally misses at least R's n private leaves. A pair consisting of R and a helper misses S's m private leaves and N−1 marks. Two helpers initially miss at least n+m+N−2 leaves. Each distinct missing leaf requires an addition at some member of the eventual pair. Deletions cannot pay two deficits with one edit. These counts refer to the state immediately after the source.

Both upper bounds hold on explicit paths leaving R and S untouched. Copy R's n private leaves to the helper holding j to obtain a cover by that helper and S. Alternatively copy S's m private leaves and the other N−1 marks to the same helper to obtain a cover by it and R. On either path the cover first returns to two on the last copy. The untouched private witnesses in the first construction, or the sole copy of j and R's private witnesses in the second, exclude an earlier return. Picking the shorter path proves equality.

For any positive edit budget L below d, the possible marked sets on R at first return after a cut of j are *exactly* the subsets J containing j with |J| at most L. The distance bound requires j, and each mark added to the previously unmarked R costs one edit. Conversely add any chosen distractor marks in J to R first, then add j. Before j arrives the bound rules out a return, and after it arrives {R,S} covers the star. Hence a realized local record J leaves exactly |J| source alternatives compatible with it in this family. This is a statement about possible histories, with no occurrence probabilities.

For N=3, m=1 and n=3, the bypass distance is three. A first return within one edit identifies the exact source leaf. A return within two edits always rules out at least one of the three source choices. After a release of leaf 1 the possible receiver sets are {1}, {1,2} and {1,3}. With three edits an empty marked receiver is attainable. For two marks a common local record containing both can already be constructed in two edits. In the named two-private example, a different two-edit return leaves R untouched by copying its private leaves 5 and 6 to the surviving helper. These controls distinguish forced presence, exact source identification and complete bypass.

## The order of the repair

There is an important difference between acting on the post-cut state and rewriting a whole path. We gave the original v16.54 peak-removal function the three vertices prior, cut, inverse and the pre-cut cover. It inspects the complete path, replaces each high-cover vertex with its own default packet endpoint, and connects endpoints by doing additions before deletions. In the named two- and three-cover fixtures its entire rebuilt command sequence is

| Order in the rebuilt path | Edit for either released mark j |
|---:|---|
| 1 | R acquires j |
| 2 | S relinquishes j |
| 3 | S reacquires j |
| 4 | R relinquishes j |

Every vertex of the rebuilt path respects the old cover bound. On a procedure that allows the cover to rise first, the forward leg acquires j *after* the source. On the never-exceed path the transfer is prearranged, using the specified future cut when constructing the replacement. The histories have different causal interpretations. The full layers dispatcher also returns a path between its two repaired endpoints. In the named default cases the returned first vertex retains R's new leaf, and the last vertex has restored R's prior membership. A lasting record or a physical chart-local read requires further evidence.

## Scope and reproduction

The original v16.54 M1 generator runs layers at target three on enumerated templates with 4, 5 or 6 labels, one private row per label, and one additional row. We checked its first four-label registered layers input. We also byte-reproduced a complete six-label archived record, line 56,732 of the first shard in validated run 37075311542, including the complete path and its proof data. The six-leaf working star and the new marked families are new applications. The target-two run is outside the original enumerated layers targets. The historical dispatcher reads q from its case input and reads current coverage from its own live state. Its campaign calls it while building certificates. A direct native v16.26-to-v16.54 update that schedules restoration remains open.

The primary evidence covers 1,056 labeled preparations and both legal marked source choices in each. It includes every one- or two-private-leaf assignment and every chart permutation for q=2 and q=3. All 2,112 complete dispatcher paths, both internal legs, actual parent triggers, clipped cycles and one-step restoration sets were independently reconstructed. In 576 arms every one-edit return had to write the released leaf. In 96 arms exactly one one-edit return kept the cut in force. The archived forward policy completed a one-edit return in 1,056 arms and wrote the released leaf directly to the designated R as its entire forward packet in 192. These are labeled case counts.

The budget supplement checks 81 source arms on 27 preparations, including both explicit bypasses, all two-chart deficits and every predicted below-threshold marked set. Two implementations also examined every reached labeled state through three edits for five source arms, with and without freezing R. The ten comparisons contain 25,162 state occurrences across the separate graphs. The raw archive supplies chart/leaf identities, edit sequences, graph states and minimum depths. Twelve deliberately corrupted inputs were rejected. The finite programs and the general combinatorial proofs have separate scopes.

[Main registration](COVER_RETURN_WRITE_PLAN.md) · [Budget registration](COVER_RETURN_BUDGET_PLAN.md) · [Worked traces and counts](cover_return_certificate.json) · [Complete finite evidence](cover_return_universe.json.xz) · [Historical replay](check_cover_return.py) · [Independent reconstruction](verify_cover_return.py)
