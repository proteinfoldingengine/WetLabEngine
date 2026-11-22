# A grade-dependent P1 change reaches the archived loop evaluator

November 21, 2026. The [frozen proof and cases](P1_WORK_CONNECTION.md) were replayed at `a7d21ffa55d77d6141a79b9a291a983ff9ddb149`. The [GitHub run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44977844379) passed exact replay, Gemini argument review and an independent publication replay.

Using the same fine tree, both supplied source families start with identical work geometry and the same field on all 25 labeled sites. The same P1 deletion removes the child-edge work term in one family. The resulting 50-edge graph passes the original v15.43 connection builder. The same deletion in the other family leaves 42 edges, which triggers the original degree test. Both post-event trees and their 25-site fields agree. The work table alone determines the difference at the connection entry point.

| Case | Minimum-work edges | Original connection result |
| --- | ---: | --- |
| Before deletion, either family | 42 | Degree-four test fails |
| After deletion, grade contrast on the removed child | 50 | Rank two, flat baseline, one gauge orbit |
| After deletion, grade contrast on the surviving child | 42 | Degree-four test fails |

The original field evaluator produces **17 nonzero differentiated loop invariants across 25 faces** on the admitted carrier. On the fixed square with corners 0, 1, 6 and 5, its invariant is exactly 1. An independent expression in centered differences reproduced all 25 values. A constant field gave 25 zeros. The rejected case stops before loop evaluation. After the second child is removed, the two work tables agree.

For common-background, equal-amplitude single-address probes the work is a tree distance between the retained destinations of the probes. The tree four-point condition excludes the chordless squares required by this particular connection. A five-ray star verifies the distinct issue even with degree four. Its nearest graph is a five-clique and the original constructor rejects it at the square count.

The four-corner preparation and its association to the periodic catalog were supplied for the replay. Its work is a Hamming metric on the multi-address preparations, with one extra binary coordinate when the contrast remains on a child. This specifies the metric type referred to informally as a tree metric in one review check. The four-point condition applies to the single-address theorem. Deriving a native multi-address preparation and showing that a physical receiver owns the loop record remain open.

[Exact replay](p1_work_connection_evidence/replay.json) · [Gemini verdict](p1_work_connection_evidence/review_verdict.json) · [Publication audit](p1_work_connection_evidence/publication_audit.json) · [Artifact verification](p1_work_connection_evidence/readback.json). The archives preserve the twelve pinned source files, raw review and jobs, and the complete per-face invariant table used in this comparison.
