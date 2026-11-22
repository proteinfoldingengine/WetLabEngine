# Grade-sensitive work under the same retained-tree pruning

The [order-curvature result](P1_ORDER_CURVATURE_RESULT.md) tests a reader whose entire input is the retained prefix order. We now apply the archived v15.40 work-geometry evaluator to the exact v16.22 grounded-tree response. This uses the grade pushforward itself. For a fixed leaf deletion and two preparations with the same initial work geometry, the existing evaluator can produce different post-pruning work and different nearest pairs on the very same retained carrier.

## Source and scope

- INHERITED P1: [the foundational carrier and exact `Pruning.aggregate`](https://github.com/proteinfoldingengine/WetLabEngine/blob/216340bbb20e7ff6ffa59053fa2b4ccc33dab85a/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py), blob `e95e3e978779164dd91f09b80e3389247e6320c2`.
- INHERITED retained response: [v16.22 `root_laplacian` and its Green inverse](https://github.com/proteinfoldingengine/WetLabEngine/blob/216340bbb20e7ff6ffa59053fa2b4ccc33dab85a/ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py#L130-L155), blob `9b71ce47bbef83132f00270f8a9a19e7721864d6`. This is the existing unit-edge diagnostic. Its mathematical selection uses the inverse equation. Its selection by physical dynamics remains open.
- INHERITED read: [v15.40 `construct_response_geometry`](https://github.com/proteinfoldingengine/WetLabEngine/blob/216340bbb20e7ff6ffa59053fa2b4ccc33dab85a/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py#L41-L69), blob `9128c24b695c1b539ac60dc93aeaf0bd4795c57b`. It accepts exact source and response vectors in matching coordinates, computes the pair work table, and emits all pairs at its minimum off-diagonal value. The original v15.40 prepared families used a different carrier. The replay binds their existing evaluator interface to the exact graded-tree response.
- SUPPLIED for the check: a formal six-address tree, two legal deletion targets, matched exact positive grade preparations, and a common reference grade. An ancestor-first serialization and the common root-zero representative place those inherited types in the evaluator's vector arguments. Actual atemporal occurrence is ACCEPTED INPUT. In the model the pruning is the stipulated operation; its selection and the availability of an actual receiver's work read remain open.

## Exact amount of work removed by P1

Fix a finite rooted prefix tree \(X\) with root \(o\) and a root-containing prefix subset \(Y\). For each pair of equal-total source preparations \(g_i,g_j\), let \(z=g_i-g_j\). The signed contrast is balanced. Use \(G_X\) for the unit-tree Green response on balanced sources, in the root-zero representative. The evaluator's work on this pair is

\[
D_X(i,j)=\langle z,G_Xz\rangle.
\]

Writing \(c_v(z)\) for the sum over the subtree at \(v\), the root-zero potential \(\phi=G_Xz\) satisfies \(\phi(v)-\phi(\operatorname{parent}(v))=c_v(z)\). Sum the node equations in the subtree to get the first equality of the drops. Pairing the balance equation with \(\phi\) then gives \(D_X(i,j)=\sum_{v\ne o}c_v(z)^2\). On \(Y\), P1 sums the retraction fibers. The inherited subtree identity gives \(c_v(P_{XY}z)=c_v(z)\) for every surviving vertex \(v\). Therefore the actual work functions before and after the event satisfy

\[
D_X(i,j)-D_Y(i,j)=\sum_{v\in X\setminus Y}c_v(g_i-g_j)^2,
\qquad D_Y(i,j)=\langle P_{XY}z,G_YP_{XY}z\rangle.
\]

This uses the reference unit-edge diagnostic and its source state. The formulas use only the inherited order and its grades. Calibration to physical quantities would require a further result. The v16.22 depth-diagonal family sets the edge drop to \(a_{|v|}c_v(z)\). Summation by parts then gives the same decrement with multiplier \(a_{|v|}\) on each term, since depth survives P1 at every retained vertex. For positive multipliers every term has the same sign as in the unit-edge case. The replay is pinned to the original unit-edge inverse.

For a single deleted leaf \(u\), the measured decrease in pair work is exactly \((g_i(u)-g_j(u))^2\). The signed contrast in the amount added at its retained parent \(p\) is \(g_i(u)-g_j(u)\) by the stipulated P1 transfer. Thus the pre/post work difference mathematically determines the magnitude of that transfer contrast. The sign is a separate input. More generally the decrement table for a family is the squared-distance table of the vectors \((c_v(g_i))_{v\in X\setminus Y}\). Its double-centered Gram has rank at most the number of removed vertices. In a sequence, each removed edge contributes once, and the cumulative decrement depends only on the endpoints and the original grades. Surviving potential drops obey the previous common-port result; work additionally pairs the source and response over the whole carrier of each evaluation.

## Matched work families and a fixed event

Use root \(o\), branches \(o-p-u\) and \(o-r-v\), and a third leaf \(w\) attached to \(o\). Let \(b=2\mathbf 1\) on the six vertices. Put \(g_0=b\) and \(g_2=b+\tfrac54(e_w-e_o)\) in both families. In family L set \(g_1=b+e_u-e_o\); in family R set \(g_1=b+e_v-e_o\). All preparations have total 12 and strictly positive entries. Supply the very same event in the primary comparison, deletion of \(u\), so \(p\) is the same surviving owner in both families. Its grade in preparation 1 starts at 2 in both. It ends at 5 in L and 4 in R.

With observations ordered as pairs 01, 02, 12, the existing work evaluator produces these exact values in the unit-edge convention.

| Carrier and family | Work 01 | Work 02 | Work 12 | Unique nearest pair |
| --- | ---: | ---: | ---: | --- |
| Fine tree, L or R | 2 | 25/16 | 57/16 | 02 |
| Same retained tree after removing \(u\), L | 1 | 25/16 | 41/16 | 01 |
| Same retained tree after removing \(u\), R | 2 | 25/16 | 57/16 | 02 |

The changing probe has a unit contrast in both edges of its fine arm. The \(5/4\) probe uses the disjoint edge at \(w\). Work 12 is the sum of the other two works because the path supports are disjoint. The full initial work geometry agrees across the two families, including its minimum and nearest pair. Thus a fixed formal P1 event separates outputs that agree before the event at every port of this evaluator. This is a claim about the existing work outputs. A receiver with access to a full fine state, or to all fixed old-tree edge drops, has a different interface and can already distinguish this preparation pair.

For the remote deletion of \(v\), the contrast is interchanged across L and R. Removing both leaves through the two possible orders gives the same terminal pair-work geometry, with work 01 equal to 1 in both families. A separate within-fiber control uses \(b+e_u-e_p\) compared to \(b\). Its work of 1 becomes zero upon deletion of \(u\) since the two P1 outputs coincide. The v15.40 `separated` flag should therefore be false for this coarse control, even though the original routine still returns numbers.

## Frozen check and current boundary

The algebra, source dependencies and exact predictions precede the freeze. Replay the pinned FCV aggregation, v16.22 inverse and v15.40 work evaluator with exact arithmetic on these fixtures. Independently reconstruct the full work table from subtree sums and every work difference from deleted-edge sums. Verify both pruning orders and the complete-collapse control. The original evaluator's metric and minimum-neighbor fields are checked alongside its full numerical tables. A clean publication job repeats the frozen replay and compares evidence bytes. The scope is this construction and algebraic theorem, rather than the historical v15.40 periodic campaign.

This gives a grade-sensitive geometric consequence at identical retained order. The exact decrease in work determines the magnitude of the single-leaf transfer contrast in the unit-edge model. The existing geometry call is a software evaluation on the exact grade family. A native process binding those inputs and the before/after work read to a physical retained receiver remains open, as does source-based event selection.
