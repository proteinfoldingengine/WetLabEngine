# A same-union prune constrains the other owner's next action at the same parent

November 21, 2026 (America/Phoenix). Research parent `302f938125fc4625f33c525479e780a6e0d1c951`. The proof and exact fixture expectations were developed before execution. The test is a scoped Path-A continuation.

## Inherited transition and held initial state

**INHERITED.** The v16.26 `engine.atomic` transition deletes one nonroot leaf of one indexed prefix view while preserving the union of all views. It returns the updated views and a parent-local cover certificate. For a parent $p$, $\tau_p$ is the minimum number of views covering all retained children of $p$. Its `trigger` is true when every previously minimum cover is destroyed. P1 is the underlying ancestor aggregation of the extensive grade on each indexed view.

**SUPPLIED.** Fix a parent $p$ with exactly two terminal children $t,u$. In a common initial state both children are held by exactly the two indices $a,b$. Both source alternatives start at this same state. Compare the inherited source deletion at $t$ in $a$ with the inherited source deletion at $u$ in $a$. Here $a$ and $b$ are roles of the actual two covering indices. The child addresses and overlap pattern are preparation data. Other indices and branches may exist.

## Forced part of the owner response

Write $s$ for the child deleted by the source and $\bar s$ for the other child.

1. The source deletion is allowed because $b$ still covers $s$. Immediately afterward, $s$ is held only by $b$ and $\bar s$ is held by both. The own view of $b$ is unchanged. In the same-parent command domain, $b$ may delete $\bar s$. Deleting $s$ in $b$ would remove $s$ from the union, so that command is forbidden. The surviving holder is determined by the incidence state.
2. Through any further sequence of inherited same-union deletions, the sole incidence at $s$ stays with $b$. There are exactly three possible local support states after the source. The child $\bar s$ remains shared, becomes held only by $b$, or becomes held only by $a$. All three are reachable via the empty continuation, a further deletion by $a$, or a deletion by $b$, respectively. Operations elsewhere preserve this classification. Any two-owner cover of these two children has $\tau_p\le2$.
3. In the first two local states, $b$ covers both children and $\tau_p=1$. In the third state the children have distinct sole owners, so $\tau_p=2$. Thus in this refinement class a source-independent endpoint condition $\tau_p=2$ is equivalent to $b$ retaining exactly $s$ at this parent. Every realized refinement to that endpoint contains the forced $b$ deletion of $\bar s$. This deletion takes $\tau_p$ from 1 to 2 and sets the original local trigger; the first source deletion leaves $\tau_p=1$. The address in $b$ separates the source choices even though the trigger values agree across the two histories. No reconstruction from an exported source log is involved in the membership statement.
4. A second deletion by $a$ of $\bar s$ is also lawful. The two source histories then coalesce to the same local state with both leaves held by $b$. This exact control shows that even completing two deletions at $p$ does not force the $\tau_p=2$ endpoint. In the deletion-only relation $b$ then has no further leaf deletion at $p$. A common action elsewhere can also leave $b$ unchanged at $p$.

The event therefore produces a change in an inherited action domain for the surviving holder. The monotone endpoint statement forces its address-bearing own view across all realizations of the specified refinement. The endpoint and its physical occurrence or enforcement remain supplied. A formal read of $b$'s own membership would distinguish the alternatives. Establishing physical access to that membership is a separate obligation. An observation-blind W_E can still choose a source-only path or withhold physical access. An implementation that reaches the same $\tau_p=2$ endpoint cannot keep the two mathematical $b$-views identical. Correlations alone provide neither the transition nor the access premise.

## Frozen exact replay of the same event in the archived geometry comparison

**SUPPLIED.** Use the previous periodic 25-label association with labels $i=x+5y$ and its ordinary square-corner incidences. Each carrier has one root, five shared parents for the rows of corner leaves, one shared parent for complement leaves, and the shared parent $p$ for $t,u$. Every view keeps the root and all seven parents. A corner leaf stays in its four original square views and has ambient grade 1. Each edge $e$ of the prescribed 50-edge periodic square catalog has one leaf under the complement parent, retained by all labels except the two endpoints of $e$. Fix $a=0,b=1$. Complement leaves have grade 3, except the leaf for $\{a,b\}$ which has grade 1. The two children of $p$ have grade 2 each and are initially held by exactly $a,b$. The shared root and parent grades are 1. Source and receiver arguments in the numerical fixture use this same carrier and the same 25 indices throughout.

By the reviewed common-grade work rule, common parent subtotals cancel even though their own grades aggregate their omitted children. The twin contributions and the special complement leaf give squared weight $4+4+1=9$ on the single edge cut $\{a,b\}$. Every other edge cut also has weight 9. Complementing a cut leaves its work unchanged. Each label has four incident edge cuts, so any two distinct labels differ on six such cuts if adjacent and eight otherwise. The ordinary corner work adds 4 for neighbors, 6 for diagonal-adjacent views and 8 for disjoint views. The original nearest work is 58, and the local perpendicular and opposite works are 78 and 80. This augmentation is a prepared control and uses the declared periodic edges.

For a source deletion of one twin, only its work row and column change. Work increases by 4 to $b$ and decreases by 4 to all other labels. The minimum is 54 on the three other original neighbors of $a$. For the forced receiver deletion of the other twin, the minimum is 54 on the six original edges incident to $a$ or $b$ with their mutual edge omitted. The $a,b$ work changes from 58 to 62 to 66. Swapping the two equal grades under the same parent preserves the complete corresponding work tables across the source alternatives.

Each ordinary row parent has cover number three because a single view covers at most two of its five leaves and suitable choices with first coordinates 0, 2 and 4 cover all five. The cover number of the complement parent is two: a nonadjacent pair of labels covers every complement leaf, and each label omits its incident-edge leaves. Every view has all the root children. Thus the global $h$ is 3 throughout the fixed primary comparison, including the two receiver paths and the coalescing controls. For the actual $p$-events the certificate should read as follows.

| Event | Local cover $\tau_p$ | Original trigger | Receiver children at $p$ |
| --- | --- | --- | --- |
| $a$ deletes $t$ | 1 to 1 | false | $t,u$ |
| $a$ deletes $u$ | 1 to 1 | false | $t,u$ |
| After $a$ deletes $t$, $b$ deletes $u$ | 1 to 2 | true | $t$ |
| After $a$ deletes $u$, $b$ deletes $t$ | 1 to 2 | true | $u$ |
| After either source deletion, $a$ deletes the other child | 1 to 1 | false | $t,u$ |

The archived work and geometry tests cover the common initial state and the two source and two responsive endpoints. Require exact equality of the matched work tables, the complete predicted nearest-pair sets, and original archived gate outcomes. Inspect the original leaf rejections for $b$ attempting the sole-held leaf, both coalescing controls, and one common admitted $b$ action away from $p$ in both histories. Run the original event verifier on all successful records. A flipped trigger must fail that verifier. Independently reconstruct the entire local deletion state space after each source choice by enumerating the possible membership subsets.

## Scope

These checks attach real inherited action availability and a forced address to an already specified two-child refinement. They use original event and geometry implementations on the same mathematical states. Periodic preparation and its work-comparison list are supplied, so the replay leaves Dot's catalog selection obstruction intact. The physical issue is whether an actual episode realizes the strict local completion and exposes the surviving address at the receiving holder.
