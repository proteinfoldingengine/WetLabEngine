# P1 leaf removal produces a structural curvature response

November 21, 2026. The [frozen proof and replay specification](P1_ORDER_CURVATURE.md) were verified at `7545053edc9418848231635b7717aca46928d003`. The [GitHub run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44973935842) passed the original-source replay, independent Gemini review and clean publication replay.

One formal 52-address tree, two legal leaf removals and one fixed surviving edge were used. The replay invokes the archived Package 17 graph reader on the parent-to-child order of the retained keys. The observed edge links the marked parent to the same depth-one neighbor in all three cases.

| Carrier used by the original reader | Weight at the same edge | Weighted Forman-like proxy there | Scalar slice proxy |
| --- | ---: | ---: | ---: |
| Fine tree | 0.577350269189 | −11.547005383774 | 0.306250283800 |
| Leaf removed under the marked parent | 0.707106781185 | −14.142135623707 | 0.304358789456 |
| Leaf removed under the remote parent | 0.577350269189 | −11.547005383774 | 0.305480802685 |

Each comparison uses the same 18 surviving vertices and 98 spatial edges at depth one. The local deletion changes exactly seven curvature values, all incident to the marked parent. The remote deletion also changes seven edge values, accounted for by the remote branch. At any eligible depth above a deleted leaf, the proof locates the changed profile row at its unique ancestor at that depth. At the parent's depth this address is the P1 owner. An outgoing-mask edit on the sink already has zero effect, since the sink has no outgoing arcs.

This is an order-only geometric consequence of the specified formal deletion. In the matched grade test the same P1 event brings grade 4 or 5 to that parent from an identical starting grade of 2. The original geometry calculation reads the same order and yields identical arrays for the two grades. An actual source-selected event, a grade-sensitive geometric coupling and physical receiver access remain unresolved.

[Replay summary](p1_order_curvature_evidence/replay.json) · [Gemini review](p1_order_curvature_evidence/review_verdict.json) · [Publication audit](p1_order_curvature_evidence/publication_audit.json) · [Artifact verification](p1_order_curvature_evidence/readback.json). The replay archive includes the two pinned sources and all 98 weight and curvature records for each carrier. The companion archives preserve the raw review, original publication artifacts and job logs.
