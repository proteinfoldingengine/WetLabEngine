# Two further prunings cannot recover the 25-view geometry

This is a proof for the fixed GEOMETRY_DELAY preparation and its original source deletion. It answers the first-actor question in [Q536(b)](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/PREREG_Q536b.md) analytically. The proof covers all legal continuations in the stated domain. The preregistered production and verification enumeration is a separate deliverable.

## Inputs

- **SUPPLIED.** Use the 25 indexed views, the positive integer grades, and the prepared cover in [`fixture()`](https://github.com/proteinfoldingengine/WetLabEngine/blob/4538a663258f169ad60c252daef11fe1a1447e13/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py). Set $A=0$, $B=12$, $T=1$, $U=2$, $R=3$ and $\mu=1984$. The source deletes $T$ from $A$. Call the resulting state $S_1$. Let $D=N(A)=\{1,4,5,20\}$ and $E=N(B)=\{7,11,13,17\}$ in the original periodic grid.
- **INHERITED.** The [v16.26 atom](https://github.com/proteinfoldingengine/WetLabEngine/blob/4538a663258f169ad60c252daef11fe1a1447e13/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py) deletes one nonroot leaf in one view and preserves the union. In the [inherited work construction](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_REPAIR.md), deleting $v$ from view $i$ changes work against any untouched view $j$ by $+s_v^2$ if $j$ holds $v$ and $-s_v^2$ otherwise. Here $s_v$ is the positive integer ambient subtree subtotal. A snapshot admits the original geometry only if its graph of all minimum off-diagonal work pairs is four-regular. The original carrier runs further tests after this necessary gate.
- **ACCEPTED-CONDITIONAL.** The [one-edit result and delayed proof](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_DELAY.md) give exactly one legal one-edit recovery, $B$ deleting $U$, and independently verify a 100-edit continuation that recovers while leaving $B$ untouched. The first result also establishes that only $(B,U)$ passes the four-regular gate at depth one.

## The recovery minimum is fixed while at most twelve views have changed

Compare any candidate with the original four-regular graph at $\mu$. If at most twelve indexed views differ, any four-regular graph on these 25 labels has a minimum edge with both endpoints untouched. It has 50 edges, and at most 48 can meet the changed labels. Such an edge in the original graph bounds the candidate minimum above by $\mu$. Such an edge in the candidate graph bounds it below by $\mu$. Thus four-regularity forces the old minimum even if the test does not prescribe it. This applies through two further deletions, which change at most three labels including the source.

The original minimum can rise only if changed views cover every original minimum edge. Each of the five horizontal five-cycles can have at most two untouched vertices in an independent set. Therefore a higher minimum requires at least fifteen changed views including $A$, hence at least fourteen distinct other views to have pruned after the source event. This applies to the longer recovered witness, which has minimum 1988. The lower bound does not establish the exact shortest recovery with a changed minimum.

## The work table at the source boundary

At $S_1$, the $A$ and $B$ entries against every other view are equal and follow the original $B$ entries. The $A$–$B$ entry is $\mu+10$. In the minimum graph the source row has dropped its four edges to $D$ and gained four to $E$. The labels in $D$ have degree three, those in $E$ have degree five, and every other label has degree four. These statements follow from `contains_t`, `mixed`, and `target` in the pinned fixture. Every off-diagonal excess above $\mu$ lies in $\{0,4,8,10,12,20,24\}$.

Two further details follow directly from the fixture:

1. Every label in $D$ holds $T$ and holds neither $U$ nor $R$. Outside $A,B$, the holders of $U$ and $R$ are exactly $E$. The only subtotal-2 features are $T,U,R$. The child of $R$ makes its subtotal 2 and is an exclusive holding of $A$. Thus $A$ cannot delete $R$ in its first further action, and $A$ never holds $U$.
2. For $i\in E$ and $j\in D$, the excess cannot be 4. The sole mechanism for such an excess among views other than $A,B$ is an opposite pair at a common grid center whose perpendicular pair contains $A$ or $B$. If it contains $A$, the center and $j$ would be adjacent members of $N(A)$. If it contains $B$, the center and $i$ would be adjacent members of $N(B)$. Both neighbor sets are independent in the periodic grid.

## Two deletions in the same view

If the sole further editor $i$ differs from $A$ and $B$, each unedited surplus label in $E$ must lose a minimum edge to $i$, since no other edge incident to it can change. Among labels apart from $A,B$, such edges are original grid edges. If $i\in E$, it has no edge to the other members of $E$. If $i\notin E$, the opposite horizontal pair $11,13$ in $E$ shares only $B$ as a grid neighbor. So $i$ cannot remove the required surplus. This excludes a single further editor other than $A,B$ at any depth.

If the editor is $A$ or $B$, every label in $D$ must gain an edge to that editor. At $S_1$ each such work value is $\mu+4$. Two deletions would have to contribute two signed positive integer squares with sum $-4$. A sum of two positive squares cannot be 4. A difference of positive squares cannot be 4 either, since $(m-n)(m+n)=4$ has no solution with positive integers $m>n$. This excludes two deletions by one editor.

## Two deletions in different views

1. Each deletion must have even subtotal. If one has odd subtotal, its editor's work against every untouched view becomes odd. Its only possible minimum edge at the even level $\mu$ is then to the other editor, which cannot give degree four.
2. At least two labels in $D$ are untouched and each needs an added minimum edge to an editor. For such an edge the excess at $S_1$ must equal the deleting feature's positive square. The only possible nonzero even square in the table is 4. Deleting $T$ raises work against a label in $D$. Among the holders of $U$ and $R$, the members of $E$ have no work excess 4 against $D$, and $A$ cannot delete $R$. The only remaining deletion that can supply an edge is $(B,U)$.
3. Consider the established one-edit recovery $(B,U)$ as a comparison state. The final cover of the proposed two-edit path differs from this state by one deletion at the other editor. This comparison is about snapshots even if we make no assumption about swapped execution order. Off this one editor's row, the minimum-edge graph is fixed. With degree four and the same minimum at both endpoints, the degrees at untouched views force the same edges to that row. The deletion changes every off-diagonal work entry of the row by a nonzero square. Its original minimum edges therefore cannot stay. This contradicts four-regularity.

## Consequences and limits

There are zero depth-two recoveries for either the fixed-minimum gate $G$ or the degree-only diagnostic $G'$. For the preregistered bound $K=2$, the only recovering first actor is 12, the only recovering first move is $(12,2)$, and its minimum depth is one. There are no depth-two completion records. Thus recovery avoiding view 12 takes at least three further deletions. It also needs more than one further editor. The single-editor argument excludes every such editor apart from $A$ and $B$, and the accepted source-only proof excludes $A$.

Deletion count refers to order in this retained-tree model. The preparation and the decision to condition on geometry recovery are supplied. This result leaves recovery enforcement, physical receiver access, and the physical gravity correspondence open.
