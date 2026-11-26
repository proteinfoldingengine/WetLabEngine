# One quantity in chart 12's neighborhood determines the one-edit response

On the original 25-chart fixture, two preparations can agree on everything in chart 12's retained grade vector, all 24 starting work values incident on 12, the initial minimum graph, and chart 12's four minimum neighbors after the specified source event. One preparation admits a single-edit geometric repair at 12. The other admits no single-edit geometric repair by any chart other than the source. The difference is present before the source acts in a scalar that the original geometry constructor already computes in the neighborhood of chart 12.

## The experiment

**Inherited** are the original named incidence atlas, historical work formula, positive extensive P1, v16.26 same-union withdrawal, v15.42/v15.43 carrier constructor and the 25-chart one-edit geometry search. **Supplied** are the finite carrier, positive rational preparations, identical source command at chart 0 and leaf 1, and the condition of immediate single-edit return to admitted geometry. The original full-table calibration was studied in [RECEIVER_PRIOR_REPAIR.md](https://github.com/proteinfoldingengine/WetLabEngine/blob/fa501b2def6227e8500aa4ebbfeb6bfaaa2b30c6/ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_PRIOR_REPAIR.md). Here we retain only the same initial minimum graph, chart 12's own P1 and its 24 incident starting works. The initial configurations are admitted under the original carrier. The initial work table away from 12 is free subject to these conditions and the fixed atlas.

Chart 12 omits the source leaf. Its original neighbors are N={7,11,13,17}. For a source subtotal s at leaf 1 write q=s². The receiver prior in the archive has Pin grade 242 and candidate grade 2. All preparations below use fine Pin grade 1 and total 3177. The nominal and low preparations are compared within the original scientific engine's post-source search domain. The higher source grade separately checks what happens when that search's minimum-work guard rejects the state.

| Fine grade at source leaf 1 | Starting largest work between two neighbors of 12 | Work from chart 12 to source after the withdrawal | Single edit by another chart restoring geometry |
|---|---:|---:|---|
| 1 | 2010 | 1997 | None |
| 2 | 2004 | 1994 | Chart 12 withdraws from leaf 2 |
| 5/2 | 3999/2 | 7967/4 | None |

Before the source event, the raw 12–0 work is 1998 in all three cases. The four minimum neighbors and their two selected opposite pairs in the initial carrier are identical. In the first two cases the minimum work remains 1984 after the source cut and 12 still has the same four neighbors. The bare 12-at-2 withdrawal is legal in every preparation and would raise its own Pin from 242 to 244 in all three. Only in the middle preparation does that edit restore an admitted geometry.

## Why one pre-event scalar suffices

For each site, form its holder set. Its work contribution is its squared subtree total multiplied by the indicator that exactly one of two chart labels holds it. The P1 prior of chart 12 determines every subtree total at a site that 12 holds. This follows by summing its P1 entries at retained descendants of that site. Every change that matters for work therefore lies at sites missing from 12. Group their square-weight changes by identical holder set.

There are 28 such support types. Write O for the 19 charts outside N and {0,12}, and U for all 24 charts other than 12. The three special support sets are T={0}∪O, R={0}∪N and H={0}. Denote their total squared-weight changes by d,r,h. At T there is just leaf 1, so d=q−4. The other types are U and U without k for each k in U. Denote their changes by b and b_k. On every incident edge 12–i the net work change vanishes. With C=b+Σb_k this says

    b_i = C + d 1_T(i) + r 1_R(i) + h 1_H(i).

For distinct i,j in U the work change is consequently twice C plus twice the sum of d,r,h over the special types containing at least one of i,j. This follows by adding the contributions of b_i and b_j and the three cuts. The old minimum 1984 is fixed because all four original 12-edges still attain the minimum and their works are fixed. The original minimum includes an O–O edge, an O–N edge and a 0–O edge (for example 1–2, 2–7 and 0–1). Their respective equations yield C=−d, r=0 and h=0. Every starting work is therefore unchanged except the six pairs inside N, each of which changes by exactly −2d. This also gives b_k=−d on N, zero outside N, and b=3d. Independent exact rank verification on the archived columns gives ranks 24 and 27 before and after imposing the minimum-edge equations.

In particular, all six absolute neighbor-pair works move by the same amount. The two opposite pairs (7,17) and (11,13) tie at the largest value. Their original work is 2004. For every admitted member of the comparison class the scalar used in the original v15.42 opposite-pair test at label 12 is

    M_12 = 2012 − 2q.

Thus any one of the six absolute pair works among 12's neighbors suffices under this calibration. The order of the six, the two opposite pair identities and their relative differences carry zero information about q on this comparison. The checker attaches a trace to the original construct_operational_complex after maxima are computed at center 12, records the six comparisons, maximum and maximizers, and checks that the instrumented carrier equals the uninstrumented result. All three numerical examples reproduce the formula exactly.

The source update changes the work 12–0 by −q and leaves 12's other 23 works fixed because 12 does not hold the source leaf. This gives a second, post-event comparison. Either sampled scalar decides the same scoped recovery question. Even the difference of the sums of chart 12's incident works suffices to obtain −q after a known single withdrawal by another chart. The pre-event witness above is available from the archived *initial geometry computation* without using a prior–post pair.

## Why recovery is equivalent to q=4

Any admitted initial and one-more-edit endpoint have the same global minimum. Only the source and the second editor may change. Each other chart has four neighbors in both admitted configurations, so some minimum edge in each lies entirely outside the two editors. Its value is unaffected. Comparing both directions gives equality of the minima. This applies also if the source edits twice.

Suppose the second editor differs from the source. The four works from 0 to N after the source deletion all equal 1984−d. If d>0, at least three of those works stay below 1984 after any single edit at another chart. If d<0, chart 0 has **no** minimum edge after its withdrawal. Its four old neighbors hold leaf 1 and their works increase by q. Chart 12 and N are the only nonholders. The initial 0–12 work is 1998, its new value is 1998−q>1984, and the four works to N are 1984−d>1984. Another chart can change at most one incident edge of 0. Consequently 0 cannot have degree four at 1984. These arguments exclude every other editor when d is nonzero. No conclusion about two edits by the source is needed for this theorem.

If d=0, the entire initial work table equals the archived table. The source operation has its nominal grade 2, so the post-source work table is the archived one as well. Its four degree-five charts are exactly N. A candidate outside N must already be adjacent to all four to remove one edge at each of them. Inside N there are no edges between those charts. The common neighbors of the four are exactly 0 and 12. For a deletion at 12, all 24 proposed works depend only on its current incident works and the square of the subtotal at its deleted site. These are fixed by 12's P1 prior and the identical post-source work. Thus its outcomes for every legal leaf agree with the original exhaustive scan. Only deletion at site 2 passes the degree test, and its full work table passes the carrier and baseline construction. This proves sufficiency and uniqueness among all non-source second editors.

## What the historical caller actually consumes

The maximum M_12 is a real intermediate of the v15.42 opposite-pair computation on the initial work. It is compared with the six absolute works to retain the maximizing *pair identities*. Their identities are constant here. The historical repair search uses the global post-source work and a separate array of candidate squares. Its standalone driver also asserts that its initial work matches a fixed 300-entry target. A changed counterfactual can pass the initial carrier while failing that fixture assertion. We invoked the original selector on the counterfactual inputs within its numerical domain and independently checked the entire legal catalogue. Under grade 5/2 its hard-coded post-source minimum test fails before the scan. Each tabulated case was also inspected by a second implementation that recomputes the true minimum and all 25 degrees for each possible edit.

The five-chart A–F edge from PR 163 cannot be passed directly to the certified 25-chart consumer. The v15.43 payload requires a square number of labels. Even at the underlying v15.42 complex level no simple graph on five labels is admitted. Degree four forces K5, in which every four-cycle has a diagonal. The checker submitted all 1,024 simple five-label graphs with representative work tables to the unmodified complex constructor. It returned 1,023 degree failures and one edge-cycle-count failure. We also reproduced the 3→2 and 11→10 A–F work changes.

The numerical source change, prior atlas, operation call and activation of recovery remain supplied. The calculations identify a sufficient raw value at an existing point in the geometry code. Whether chart 12 retains that value, receives the source withdrawal as an event, or initiates a recovery from it remains open. No physical time, fractal scaling, quantum operation or gravitational correspondence is established by these tests.

## Reproduction

Run python3 -B check.py HISTORICAL_CHECKOUT --raw raw.json with a checkout at e61d5b0e827f7b412824ad46021e2ad6cc6f7875 containing the historical sources. result.json reports the checks; raw.json.xz records the grade assignments, changed work entries, constructor traces and exhaustive outcomes. The three grade preparations are supplied exact rational interventions.
