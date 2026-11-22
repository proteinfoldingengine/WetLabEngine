# A retained leaf deletion in the archived order-to-curvature calculation

This checkpoint tests the exact mathematical interface between same-Genesis P1 pruning and the Package 17 spatial graph reader. It answers the narrower question of where the **structural** consequence of a specified leaf deletion lands in an existing geometry calculation. The [prior bot entry](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7070952873) controlled the archive's random retention mask. The [V1718 interface result](V1718_P1_INTERFACE.md) addressed the cyclic extensive-grade update. Here the input to the original curvature routines is the already-inherited prefix order itself.

## Inputs and claims

- INHERITED mathematics and code. FCV L1–L4 fix a same-Genesis prefix carrier, its parent-to-child edges and the admissible prefix-closed pruning. The [FCV implementation](https://github.com/proteinfoldingengine/WetLabEngine/blob/64e5a9a12869a2533e4a9274925442f7515a031b/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py) validates both carriers, fixes `ancestor`, and implements exact finite-additive grade pushforward in `aggregate`. Its Git blob is `e95e3e978779164dd91f09b80e3389247e6320c2`.
- INHERITED historical calculation. The [Package 17 spatial reader](https://github.com/proteinfoldingengine/WetLabEngine/blob/64e5a9a12869a2533e4a9274925442f7515a031b/Tmp/TOE/package17_bundle/spatial_graph_curvature_verifier.py) takes a Boolean DAG matrix at `transitive_closure_bool` (lines 69–76), constructs rank slices and cosine-weighted adjacency from closure (79–116), then computes the weighted Forman-like edge proxy (119–133) and the overlap proxy (136–152). Its Git blob is `c8043250f0a61077faabbc029ef7e248905f3f32`. The fixed-total grades are used only in the separate grade control.
- SUPPLIED in the check. One formal fine tree, two matched legal leaf deletions and two positive grade preparations. The archive's neighbor count 7 and minimum slice size 18 are used. Topologically ordering the keys by length and then by address only serializes the inherited incidence. No positions, timestamps, mask seeds, source coordinates or new read function are needed to compute the edge proxy on this interface.
- ACCEPTED INPUT. Actual atemporal occurrence. The calculation is conditional on which admissible P1 map is realized. It earns neither the choice of this event from the grades nor a physical receiver's access. An owner-relative address is identified below by its actual ancestor relation, within the formal carrier.

## Where the original reader changes

Write \(R_X\) for the strict prefix relation on a fine tree \(X\). The closure of the parent-child matrix is exactly \(R_X\), because each directed path appends one address component and every strict prefix pair has the unique intermediate prefix chain. The archive computes rank as depth. Remove a single fine leaf \(u\), form \(Y=X\setminus\{u\}\), and consider a fixed depth \(d\) with \(1\le d<|u|\). The same vertices survive at that depth and all their strict prefix relations with survivors are preserved. Let \(p\) be the unique depth-\(d\) ancestor of \(u\). At \(d=|u|-1\), this is the FCV owner \(r_{XY}(u)\).

The archive's profile for \(v\) concatenates its indicator of strict ancestors and its indicator of strict descendants. In passing from \(X\) to \(Y\), remove the ancestor and descendant entries for address \(u\) in each profile. The ancestor entry is zero across the slice. The descendant entry is 1 exactly in the row for \(p\). Thus the raw profile Gram across these same vertices changes by

\[
G_Y=G_X-e_pe_p^\top.
\]

Every off-diagonal dot product is preserved. The row norm of \(p\) goes from \(\sqrt{d+D}\) to \(\sqrt{d+D-1}\), where \(D\) is its number of strict descendants before deletion. Every normalized off-diagonal similarity touching \(p\) is multiplied by

\[
\kappa=\frac{\sqrt{d+D}+\varepsilon}{\sqrt{d+D-1}+\varepsilon}>1,
\qquad \varepsilon=10^{-12}.
\]

They are positive because every vertex at this depth has the same Genesis root as a strict ancestor. Similarities away from \(p\) are preserved before neighbor selection. For an eligible slice of size at least \(k+2\) with \(k\ge1\), every pair selected after deletion by \(p\)'s own row has strictly larger symmetric output weight than it had before. The post output is the new raw positive similarity, and the pre output was either its smaller raw similarity or zero. A pair selected in both has the stated ratio. This guarantees a change at the ancestor in the actual neighbor calculation without needing a tie convention. It permits changes away from \(p\) due to neighbor competition. The argument uses exact real arithmetic for the code's formulas. The bounded replay checks margins in the explicit fixture through the full original arrays.

The archive's mask at lines 56–66 only controls outgoing arcs. Masking a sink keeps its entire existing row zero and leaves its incoming column present. On this tree the sink-mask operation therefore gives identical input to the reader. Literal P1 pruning removes the vertex from the carrier and removes its ancestor and descendant entries from the profiles. The single deleted bit at depth \(d\) is the structural source of the geometric change.

## Held neighboring edge and two falsifying controls

Take 18 depth-one siblings under the common root. Seven siblings at addresses `(0,)` through `(6,)` have no descendants. Denote this group by \(A\), and fix \(a=(0,)\). The marked branch \(p=(7,)\) has two leaf children. The remote branch \(b=(8,)\) has four, and the other nine siblings each have three. Set \(u=(7,1)\) and \(v=(8,3)\). Compare the original fine tree to its pruning of \(u\), and separately to its pruning of \(v\). In all three the same rank-one slice passes the original 18-vertex guard. The comparison holds the entire initial tree and the observed edge \(p\! -\! a\) fixed.

Every pair in this slice has exactly one shared ancestor and no common descendant. Thus the seven smallest profile norms are exactly those of \(A\). Other vertices always select precisely those seven neighbors. A row of \(A\) selects the other six and then \(p\), which has strictly fewer descendants than any other vertex outside \(A\) under both controls. The symmetric support is therefore a clique on \(A\) joined to every remaining vertex, with no edges between the remaining vertices. It has 98 edges, \(\deg(p)=7\), and \(\deg(a)=17\). It stays identical in the two prunings. The original proxy is \(F_{pa}=(4-\deg(p)-\deg(a))W_{pa}=-20 W_{pa}\) on the held edge. Consequently

| Tree | Existing weight at the held edge | Existing curvature proxy there |
| --- | --- | --- |
| Fine or remote leaf removed | \(1/[(1+\varepsilon)(\sqrt3+\varepsilon)]\) | \(-20/[(1+\varepsilon)(\sqrt3+\varepsilon)]\) |
| Leaf removed at the marked branch | \(1/[(1+\varepsilon)(\sqrt2+\varepsilon)]\) | \(-20/[(1+\varepsilon)(\sqrt2+\varepsilon)]\) |

Exactly the seven edges incident to \(p\) change in the local deletion. The overlap proxy uses only support and stays fixed. The scalar slice assembly from line 182 therefore changes by \(-20\cdot7\,\Delta W_{pa}/[98(98+\varepsilon)]\). The replay checks these statements for the existing original readers and reconstructs the full rank-one support and curvature table independently. This scope is one structural slice of the archived calculation.

For a grade control, keep the very same local deletion for both preparations. Let the fine grade be 2 at every address in the first preparation and add \(e_u-e_v\) in the second. Both are positive, have equal totals, and start with grade 2 at \(p\). The actual inherited `Pruning.aggregate` gives grade 4 or 5 at \(p\) after deletion. The reader takes the same retained carrier in these two cases, and every numeric geometry output in the comparison is identical. More generally, its entire read factors through the Boolean order and is insensitive to grade differences on an identical retained carrier. A dependency of the chosen carrier on source is a separate event premise.

## Frozen procedure and scientific boundary

The algebra, proposed input trees, two event controls, grade preparations and expected geometric differences were derived by inspection before freezing. The original graph reader and exact P1 module are pin-checked before execution. The checker takes the existing address incidence to the original closure, rank, profile, Forman-like and overlap routines. It independently verifies the strict prefix closure, expected depth, full weight matrix and edge table. Inspect the retained address and full support identities across all variants, and compare the scalar proxy at the common rank. Local and remote contrasts, the sink-mask control and the same-event grade control are kept together. Execute just these frozen cases, review the mathematical argument, and reconstruct the identical evidence bytes in a clean publication job.

The structural direction `specified retained-tree deletion → surviving ancestor profile → existing edge curvature proxy` is fixed in this interface by the same-Genesis order. It supplies a source-side geometric consequence tied to the formal owner address. Under the matched grade preparations, the unweighted order interface cannot see the amount that P1 delivered there. The selection of the actual event, any native grade-sensitive geometric coupling and physical receiver access remain open. The result makes no joint-realization or physical gravity claim.
