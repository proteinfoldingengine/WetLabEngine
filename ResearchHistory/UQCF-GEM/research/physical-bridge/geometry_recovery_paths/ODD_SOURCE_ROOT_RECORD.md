# An odd pruning event fixes a retained root-grade bit at recovery

Begin with the published 25-view preparation. In this preparation a one-unit source deletion, kept as the source's only edit, forces an odd increment of every other view's P1 root grade at every recovered endpoint. An explicit sequence attains recovery after exactly 24 further deletions. For the original two-unit source deletion, holding the source fixed forces the complementary even increment. View 12 starts with the same grade, 242, in both preparations. The two witnessed recoveries give 243 and 244, respectively. The result concerns accepted endpoints. The original one-view deletion also admits a continuation that permanently excludes recovery.

## Objects and provenance

**INHERITED.** Each chart is an ancestor-closed subset $Y_i$ of a common rooted tree. A v16.26 atom removes one nonroot local leaf from one chart and preserves the family union. The fine grade $g_v$ is fixed. P1 assigns each grade to its deepest retained ancestor. Write $R_i$ for its component at the root, $s_v$ for the sum of fine grades in the ambient subtree at $v$, and $M_i$ for the retained grade weighted by retained address depth. The fixture maps each chart to the dual work coordinates $s_v 1_{v\in Y_i}$ for $v\ne0$. The v15.40 constructor then gives
\[
 W_{ij}=\sum_{v\in Y_i\triangle Y_j}s_v^2,\qquad
 M_i=\sum_{v\in Y_i,\ v\ne0}s_v.
\]
For the second identity each fine grade contributes once per retained nonroot ancestor. The v15.43 gate builds a carrier from all global minimum edges and tests the local directions and the flat baseline. Recovery means this full call succeeds.

**SUPPLIED.** Use exactly the initial state of the archived five-by-five periodic grid, its integer grades and fixed chart labels. The source is $A=0$ and the receiver under comparison is $B=12$. The author supplies the event, both continuation schedules, and the conditioning on recovery. The least raw leaf convention fixes the representative on each cut. The grades, chart family and carrier are inherited. The two source choices delete different leaves. The existing two-unit example, including its recovered root grade, is a comparator.

[Original fixture and replay](../forced_parent_deletion/check_geometry_repair.py) · [Previously reviewed parity argument](RECOVERY_WITHOUT_VIEW_12.md) · [Predictions frozen before this replay](ODD_SOURCE_CHECK_PLAN.md)

## Why the receiver's particular coordinate is constrained

As $s_v^2\equiv s_v\pmod2$, $W_{ij}\equiv M_i+M_j\pmod2$. At an admitted state an odd global minimum would make its positive regular minimum graph bipartite on 25 vertices. Summing degrees on each side would give equal part sizes, a contradiction. The even minimum and connectivity force all $M_i$ to have the same parity. Between two admitted endpoints the losses $M_i^{\rm initial}-M_i^{\rm final}$ therefore have common parity.

The fixture has precisely one vertex at depth two, child 4 of vertex 3. Only $A$ holds the child. Preservation of union and monotone deletion keep it at $A$, where it protects its parent. All legal deletions at any reachable state thus remove a child of the root, including deletion of 3 in a chart that lacks 4. Just before such a deletion of $v$ the entire subtotal $s_v$ is assigned to $v$ in that chart because $v$ is a local leaf. The deletion assigns that subtotal to the root. In the edited chart $\Delta R_i=s_v=-\Delta M_i$. Other charts keep their own grades. Consequently, for every recovering continuation from this start,
\[
 R_i^{\rm final}-R_i^{\rm initial} \equiv M_A^{\rm initial}-M_A^{\rm final}\pmod2
 \quad\text{for every }i.
\]
The parity argument for the moment uses odd view count, positive regularity and connectivity. The identification of the root coordinate uses the particular protected tree shape. With persistent odd source loss every one of the other 24 charts must edit. One edit touches one chart. This gives a lower bound of 24 further deletions for that odd case. A second odd edit at the source can clear its odd loss.

## A witness attaining 24 further deletions

Write a label as $i=(x,y)$ modulo five. Put $C_i=\{(x+2,y+1),(x+2,y+2)\}$. Choose the least raw grade-one root leaf $v_i$ initially missing exactly on $C_i$. Each $C_i$ is a different adjacent pair and excludes $i$. In the fixture's ordinary adjacent-pair branch its allocated squared mass is 32 or 38 according to the two ordinary endpoints' $T$ membership. An adjacent pair containing $A$ or $B$ receives 35. The marked labels are nonadjacent. The fixture's greedy rule expands these as $25+7\cdot1$, $36+2\cdot1$, or $25+9+1$, respectively. Thus each cut has the required unit leaf. Initially it belongs to 23 charts. Removing it only in chart $i$ leaves 22 holders. Distinct cuts ensure distinct leaves. The entire 25-edit list consists of legal atoms. Apply $A$'s edit first and the other labels' edits in increasing order.

For distinct $i,j$ the completed change in $W_{ij}$ adds $1-2\,1_{j\in C_i}$ for the edit at $i$ and $1-2\,1_{i\in C_j}$ for the edit at $j$. Both exceptional memberships cannot occur since $2\ne-2\bmod 5$. The total change is zero or two. No exceptional pair is a nearest neighbor or a pair of distinct neighbors of one center, since its torus graph distance is at least three. Consequently every old minimum increases by two, and every comparison used to distinguish opposite from transverse neighbors receives that same increment. Old nonneighbors start at least four above the old minimum. The new minimum is 1986, up from 1984, on exactly the original 50 edges. The unchanged adjacency, face cycles and opposite pairs reproduce the directed tangent data. Identity preserves the full work table and satisfies the nonempty automorphism check. Baseline enumeration uses the same directions, cycles and frame actions. The full original gate and an exact comparison of these baseline objects check this argument. Across all 300 pairs the replay finds 250 work entries increasing by two and 50 unchanged.

After each of the first 1 through 24 edits, an edited and an untouched chart have opposite moment parity. Each such prefix necessarily fails admission. At the 25th edit all root grades increase by one. The 24-further-edit lower bound is attained. Edit count denotes order in pruning and carries no physical duration.

## Matched and crossed continuations

Both arms start at the same archived state. The odd source deletes raw leaf 662, absent from views 7 and 12 before that edit. View 12 deletes a different leaf, 1217, on the long schedule. Its own changing scalar therefore cannot be explained by its holding and dropping leaf 662. A downstream schedule is the list of the remaining edits after the named source deletion. The long schedule omits $A$ and the short schedule consists of $B$ deleting the published subtotal-two leaf $U$.

| Source deletion at view 0 | Later schedule | Full carrier | Final root grade at view 12 |
|---|---|---|---:|
| unit leaf $v_0$ | unit leaf at each of the 24 other views | admits | 243 |
| published $T$, subtotal 2 | same 24 unit edits | rejects | 243 |
| unit leaf $v_0$ | $B$ deletes $U$ | rejects | 244 |
| published $T$, subtotal 2 | $B$ deletes $U$ | admits | 244 |

At a fixed schedule, changing only the source leaves the value at $B$ identical. This follows also directly from the local aggregate, which depends only on the fixed fine grades and $B$'s own final membership. Selecting admitted runs makes source parity distinguishable from $B$'s final root parity, including on other successful continuations with frozen source. The numerical root grade itself can depend on the continuation. The comparison assumes knowledge of the common initial grade and selection of a successful run.

After the unit source event, another legal unit deletion at $A$ clears the source parity difference while all other views are untouched. In a second control keep $A$ and $B$ fixed and empty charts 1 and 4 to their roots. The checker validates all 1,299 deletions in chart 1 and 1,298 in chart 4 against the inherited leaf and union predicates. Opposite parities at $A,B$ bar every intermediate recovery. At the end $W_{1,4}=0$ permanently, since root-only views can never lose their root or acquire another vertex under these atoms. The original gate rejects a zero off-diagonal entry on every subsequent continuation, including ones that resume editing $A$ or $B$.

## What operates on the receiver

In the historical v15.43 entry point, acquisition builds work and field payloads for specified response families. The evaluator passes each supplied payload into the carrier constructor, then evaluates the supplied fields. In v16.26 the atom requires the chart and leaf as arguments; its factorization routine takes a target as an argument. In the witness it is the explicitly scheduled local deletion at $B$ that changes $R_B$. The original P1 aggregation reads back that coordinate. These inspected calls leave open a law requiring recovery or initiating an edit at another chart from $A$ alone. Whether a physical receiver can access its root coordinate also remains open.

[Acquisition](../../../demos/v15.43-certified-response-geometry/acquire.py) · [Evaluation](../../../demos/v15.43-certified-response-geometry/evaluate.py) · [Original carrier](../../../demos/v15.43-certified-response-geometry/carriers.py) · [Original atomic update](../../../demos/v16.26-consistency-increment-law/engine.py)

## Replay

The checker verifies the inherited atom and its independent verifier on all 25 designated edits. It compares symmetric-difference work with the original v15.40 dual-coordinate calculation on every pair at the initial, two matched and two crossed endpoints. It compares every component of the original P1 aggregate with direct grade-by-grade parent tracing in those endpoints. It checks the original gate at all odd-path prefixes, the omitted-source and source-correction controls, and the permanently excluded endpoint. Each edit of the two collapse rows is checked independently for legality, with the original atom and verifier also run on the first and last deletions in each row. The deterministic certificate preserves all selected raw sites, root grades, moments and gate outcomes. This is a finite witness and an analytical endpoint theorem, separate from the older two-unit enumeration.

[Executable replay](check_odd_source.py) · [Machine-readable certificate](odd_source_certificate.json)
