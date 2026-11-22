# Which P1 views can reach the archived square geometry

November 21, 2026 (America/Phoenix). The proof and four cases were frozen at `96692632c89a4caa069e4a815befac2812ec04ac`. The original-code replay, independent Gemini argument review, and publication replay succeeded at that checkout and workflow revision. [Frozen proof](P1_MEET_WORK_CATALOG.md) · [GitHub run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44980778646)

## Production from one grade

Two successive admissible P1 projections produce each of the 25 four-corner grades from one unit grade on a common star. Both orders equal the direct projection, as prescribed by v16.23 O1. The work between any two projected grades is the sum of squared ambient subtree subtotals at the addresses retained by exactly one view. Its dependence on shared addresses comes from the intersection of the two strip masks. The previous loop experiment supplied the four-corner grades separately. This replay supplies a common grade, the periodic strips and labels, and the list available to the comparison. [Previous loop evidence](P1_WORK_CONNECTION_RESULT.md)

| Same ambient grade and original work evaluator | Views | Minimum work | Minimum edges | Original square gate |
| --- | ---: | ---: | ---: | --- |
| Square intersections | 25 | 4 | 50 | Identifies 25 faces and rank two |
| Squares plus their generating strips | 35 | 4 | 50 | Rejects, ten strips have degree zero |
| Squares plus one shared side | 26 | 2 | 2 | Rejects, 23 squares have degree zero |
| All intersections of squares | 101 | 1 | 125 | Rejects, all 25 squares have degree zero |

On the admitted inputs the six local work values between neighboring views are 6, 6, 6, 6, 8, 8 at every vertex. The two values of 8 distinguish the opposite pairs. Each of the 50 shared-side views individually has work 2 to its incident squares, so admitting any one suffices to supersede the work-4 edges.

## Constraint on native availability

With one ambient grade, a catalog closed under pairwise intersections must have comparable minimum-work neighbors. If every vertex has four such neighbors, the lower endpoint of any minimum edge has at least three tied maxima among its six neighbor-pair work values. The original direction gate requires exactly two disjoint maxima. Complementing the active address masks gives the same obstruction for catalogs closed under unions. The proof covers weighted subtotals and makes no periodicity assumption.

The v16.26 atomic transition takes a catalog and an index as inputs. Its leaf-deletion rule checks preservation of the union and computes the hitting profile and trigger from that catalog. The v16.54 floor concerns the number of palette labels held by each root slot in guard repair. Applying it to the number of retained addresses in the work evaluator would require an explicit mapping. These upstream interfaces leave open which projections a retained owner is able to compare. [v16.26 atomic transition](../../../demos/v16.26-consistency-increment-law/engine.py#L24-L26) · [v16.54 validation plan](../../../demos/v16.54-parent-support-connectivity/PROSPECTIVE_VALIDATION_PLAN.md)

For this route, the native delivery question now includes a concrete eligibility condition. An inherited operation would need to give an owner access to the joint projections with the requisite smaller views excluded from the same comparison. The native source-to-receiver relation remains open.

## Verification

The replay verifies both P1 composition orders for all 25 squares, the complete lists of minimum edges in all four catalogs, and every work pair against the exact indicator formula. The local replay from the frozen Git checkout and the downloaded first and second GitHub replays agree byte for byte. Gemini 3.1 Pro accepted the argument with native bridge status **OPEN**. The downloaded review response and publication audit match their exact encodings in the job log. [Exact replay](p1_meet_work_catalog_evidence/replay.json) · [Gemini verdict](p1_meet_work_catalog_evidence/review_verdict.json) · [Publication audit](p1_meet_work_catalog_evidence/publication_audit.json) · [Artifact verification](p1_meet_work_catalog_evidence/readback.json)

The evidence directory preserves the original replay, review, and publication ZIPs, and a ZIP of all three job logs. Their digests are in the artifact verification record.
