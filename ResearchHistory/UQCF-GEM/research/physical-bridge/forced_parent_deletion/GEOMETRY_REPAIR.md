# The geometry gate can force a specific receiver edit on recovery

Take a fixed common ambient retained tree and one extensive grade on it. A deletion in a single indexed view changes only that view's comparisons with the others. In the original v15.43 geometry, a single deletion with a positive squared subtree grade takes an already accepted carrier out of the degree-four class. If two positive-weight deletions at distinct views restore an admitted carrier, the two views must have been at least three edges apart in the original neighbor graph. A constructed 25-view case has exactly one legal next deletion that restores geometry. The condition identifies the receiving index and its address without supplying either to a scheduler.

## Work and the original admission conditions

**INHERITED.** FCV P1 aggregates removed grades to the nearest retained ancestor. For a retained nonroot vertex $v$, its subtotal over all descendants is the same as the ambient subtree subtotal $c_v$. For a discarded vertex the corresponding edge coordinate in the ambient zero extension vanishes. Use the v16.22 unit Green inverse in the dual edge coordinates of its T1 and T4. A centered source then has edge amplitudes $c_v$ and its paired response has the same edge amplitudes. The v15.40 work pairing between indexed views $Y_i$ and $Y_j$ is
$$
W_{ij}=\sum_{v\in Y_i\triangle Y_j}c_v^2.
$$
This is the previously verified common-grade comparison. An elementary deletion at $i$ of $t$ changes $W_{ij}$ by $+c_t^2$ when $j$ holds $t$ and by its negative otherwise. Other rows and columns off $i$ are unaffected. This formula also applies when $t$ is an internal ambient vertex that is a leaf of the edited view.

The original v15.43 `carriers.build_carrier` requires the complete graph of minimum off-diagonal work pairs and calls the v15.42 operational complex. Each label must have degree four. At each center two disjoint neighbor pairs must give the two and only two maximum pair works. Further gates check the cycles, tangent rank and baseline. The original v16.26 `atomic` deletes a leaf of one view and preserves the global union. The event records provide independent verification of the two actual transitions in the replay.

**SUPPLIED.** Use the prepared grade, carrier and original work/geometry catalog on the same 25 indexed views. Compare continuations that recover an admitted geometry after exactly one further v16.26 deletion. The gate determines which realized continuation would qualify. No inherited rule for immediate recovery, physical enactment or receiver access is assumed. A fixed centered field is a separate supplied input to the loop evaluator.

## One changed view and two changed views

Let the minimum work before and after two admitted configurations be $\mu_0$ and $\mu_1$. If at most two indexed views changed, any unchanged off-row pair has its original work. Every degree-four graph on this fixed set has an edge disjoint from the changed views. An untouched vertex has at most two possible changed neighbors and needs four neighbors. An unchanged edge of either admitted graph gives an upper bound on the minimum of the other. Therefore $\mu_0=\mu_1$.

When only one row changes, every untouched vertex's degree-four constraint determines whether it is joined to that changed vertex from its fixed degree among untouched vertices. The minimum graph is consequently identical across the two admissions. A single deletion with $c_t^2>0$ changes every work entry of that row off the diagonal, so all old minimum edges at this vertex leave the minimum. This contradicts identical graphs. In particular the single deletion fails the original degree-four test. The proof allows a change of the minimum at a rejected intermediate state.

For two positive-weight deletions at distinct views A and B, each edge from either changed view to an untouched view changes work by a nonzero amount. If any untouched view originally borders both A and B, it loses both edges. It cannot replace them because its edges to untouched views are fixed. Thus the changed views have no common original neighbor. If A and B are adjacent originally, each has three other neighbors and their sets are disjoint. At fixed minimum all three A neighbors other than B must move to B, and conversely. The edge between A and B must stay to give degree four. For every one of the other three neighbors $j$ of A, (W_{Bj}) must fall to $\mu_0$ by exactly the square corresponding to B's single deleted site. It follows that the three pairs ({B,j}) have equal pre-event work. At center A one of those pairs must be among the two disjoint maxima, and equality then forces all three to be maxima. Contradiction. The two changed views therefore have original graph distance at least three. This is a statement about order of deletion and the work graph. No physical propagation speed follows.

## A recovery with one legal choice

Use the periodic square graph on coordinates modulo five, labels $x+5y$. Source A is 0, and B is 12. Their graph distance is four. Define the minimum $\mu=1984$. Write $N(A)$, $N(B)$ for their original neighbor sets. Within the pair, A holds leaf $t$, and B holds leaf $u$, both of grade 2. Every other view has a bit $e_j$, zero on $N(B)$ and one elsewhere. It holds $t$ when $e_j=1$ and $u$ when $e_j=0$.

The fixture in `fixture()` implements the following work values on the same common tree.

- At each $j\in N(A)$, $W_{Aj}=\mu, W_{Bj}=\mu+4$. At $j\in N(B)$ these values are reversed.
- For any other $j$ outside A and B, $W_{Aj}=\mu+d_j+4(1-e_j)$ and $W_{Bj}=\mu+d_j+4e_j$. Here $d_j=20$ if $j$ is an opposite two-step neighbor of either changed view, and $8$ otherwise. Neither changed view is an opposite two-step neighbor of the other. The mixed two-step opposite and perpendicular sets do not overlap across A and B on this placement.
- Among untouched views an edge has work $\mu$. Each straight two-step pair has work $\mu+20$ unless its perpendicular opposite pair at the same center contains A or B. In that case set the works equal. Every other pair has work $\mu+8$. Opposite work exceeds perpendicular work at every center. Work between A and B is $\mu+14$.

To realize these values by P1, add an ambient vertex $r$ of subtotal 2 held by A and the other views with $e_j=0$, plus a grade-1 child of $r$ held only by A. The grade on $r$ itself is 1. A cannot delete the child because its union ownership is unique, and cannot delete $r$ while retaining the child. A separate grade-1 root leaf is held only by B. The three membership bits at $t,u,r$ by role are $(1,0,1)$ for A, $(0,1,0)$ for B, and $(e_j,1-e_j,1-e_j)$ for each untouched view. These bits and the two private leaves give the required A/B row difference while giving a mutual work contribution of 14. Each other added leaf is a cut, implemented by membership in the complement of the cut, with no grade-2 leaf.

For clarity, subtract the special-feature contributions from the desired table. The residual is $\mu+b_{ij}$ off diagonal. Let $\epsilon_i$ be 1 for A and B, 0 otherwise. Then $b_{ij}-\epsilon_i-\epsilon_j$ is even. Use cut weights
$$
w_{ij}=32-\frac{b_{ij}-\epsilon_i-\epsilon_j}{2},\qquad w_i=1024-\sum_{j\ne i}w_{ij}+\epsilon_i.
$$
All weights are positive on the specified fixture. The cuts ({i,j}) and ({i}) contribute $2(1024)+\epsilon_i+\epsilon_j-2w_{ij}=\mu+b_{ij}$ to pair $i,j$. Each positive integer cut weight is split into squares of positive integers excluding the square of 2. The greedy implementation uses the largest available square and substitutes ones for a remainder whose largest square is 4. This realizes the table as weighted work from one actual common grade. The construction supplies the geometry fixture. Physical preparation remains open.

The source deletion of $t$ from A raises the work on $N(A)$ by 4 and lowers the work on $N(B)$ by 4. Thus each vertex of $N(A)$ has degree three and each of $N(B)$ has degree five. Consider any one following deletion.

1. A further deletion at A alone would have to restore the original graph by the one-row result. Restoring an edge from A to $N(A)$ requires deleting subtotal 2. The only remaining subtotal-2 vertex in A is $r$, protected by the child just described.
2. An edit at $j\notin\{A,B\}$ must remove an edge to each degree-five vertex of $N(B)$ other than $j$ itself. If $j\in N(B)$, these vertices have no edges between them. If $j\notin N(B)$, it would have to be originally adjacent to all of $N(B)$. The only such vertex in this torus is B, as can already be seen by intersecting the neighborhoods of the two vertical neighbors of B. Any admitted work after the two edits has the original minimum by the two-row result.
3. The remaining index is B. It must acquire four minimum edges to $N(A)$, currently of work $\mu+4$, so it must delete a leaf of subtotal 2. Only $u$ meets that condition in B. Its deletion is lawful because the four views in $N(B)$ still hold $u$. After the deletion the minimum graph is exactly the original graph with A and B interchanged. All off-diagonal works follow the same transposition except their mutual work, which falls from $\mu+14$ to $\mu+6$ and is still nonminimal. No neighborhood contains both A and B. Thus the pair's change does not affect the opposite-direction criterion. The original carrier accepts the repaired state.

The solver finds exactly this one action among 32,575 legal next deletions. Additional source-only deletions were legal and failed the gate. Recovery in one further deletion is an explicit condition.

## Retained record and loop calculation

B's root grade is 242 after the source event and becomes 244 on the forced recovery. Exact P1 aggregation achieves that value while preserving total grade, and the original atom's receiver result is independently verified. The recipient is identifiable from the degree deficits and excesses even if the particular labels are renamed before the comparison.

For the existing v15.43 field evaluator use $f_i=\delta_{i,A}-1/25$ on both accepted states. Read the same four labels $(3,4,9,8)$, whose face is present at both ends. In the before-state stencil only the $x$-derivative at the label 4 contributes, with value $1/2$ in the chosen orientation. The loop's squared invariant is $1/64$. After A and B exchange neighborhoods there is no neighbor of A in this face's four stencils. The derivatives are zero there and the invariant is zero. The code compares the original transport and four-factor holonomy with an independently evaluated signed centered-difference expression. A constant field gives zero on every face at both accepted endpoints.

The grade change is in B's own projected record. The fixed-face read is a formal output of a separate existing field evaluator. The calculation derives the alternative actions excluded by observed one-deletion geometric recovery. It leaves open why a physical history uses this gate, completes in that number of operations, prepares this carrier, or gives access to the receiver's grade or loop field.
