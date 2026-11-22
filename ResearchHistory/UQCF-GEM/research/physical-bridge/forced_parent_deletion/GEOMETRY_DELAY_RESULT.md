# Delayed recovery changes what the geometry can force

In the same 25-view construction, recovery after the source deletion requires a retained-grade change at some other view, regardless of how many deletions are allowed. The source cannot restore its four original minimum-work comparisons on its own. Their sum increases from 7936 to 7952 and can only rise or stay fixed under further source-only prunings. Any degree-four recovery with the other rows fixed would require the sum to return to 7936. Positive grade also makes the sum of depth times retained grade across all other views strictly decrease on every successful continuation. [Proof](GEOMETRY_DELAY.md)

| Continuation after the source deletion | Geometry | View 12 root grade | Fixed-face invariant |
| --- | --- | ---: | ---: |
| Unique one-deletion recovery | Admitted after one edit by view 12 | 244 | 0 |
| Delayed recovery | Admitted after the 100th edit, with view 12 untouched | 242 | 1/64 |
| Terminal continuation | No admitted prefix through all 31,163 edits | 242 | Geometry unavailable |

View 12's root grade before the source deletion is 242. Its first-path grade increase comes from its own deletion. The other 23 views carry out the delayed path, with both the source and view 12 fixed. The delayed endpoint has the original labeled baseline, direction data and cycles. The geometry evaluator therefore returns the original loop record for any fixed admissible exact field. The source-centered field's 25 loop records match exactly. The aggregate decrease in depth times retained grade is two on the immediate path and 100 on the delayed path. [Finite delayed witness](geometry_delay_witness.json) · [Exact reports and work tables](geometry_delay_evidence/geometry-delay-replay.zip)

In the terminal continuation, two views become root-only. Until then a frozen row precludes the degree-four graph. Afterward the work between those two views stays zero, which precludes admission by the inherited positivity check. The continuation remains legal, preserves view 12, and ends with one holder per nonroot vertex.

## Matched source control

The same one-row argument gives a source-specific admission test under a fixed later schedule on the other views. The two endpoints with and without the source deletion differ in every off-diagonal entry of the source row, by four in absolute value. If both admitted snapshots had degree four, their global minimum and the source's four minimum edges would agree. That contradicts the changed work on every edge of that row. Thus each of the two displayed recovery schedules distinguishes the source deletion through the old global gate. A local exact control restored the deleted leaf's membership in the source view at each recovered endpoint. The immediate control had 50 minimum edges at 1984 and the delayed control had four at 1984. Both failed with the original gate's degree-four error. This control isolates admission at matched endpoints. The loop comparison instead uses the supplied field on admitted snapshots.

## Verification and scope

A local integer search found the finite delayed witness. The frozen replay uses exact memberships and integer work updates. It reconstructs v15.40 work at all three admitted snapshots, invokes the original v15.43 carrier and holonomy routines, and checks representative events with the original v16.26 verifier. The 100 deletions give a feasible schedule. The minimum length for a recovery that preserves view 12 is open. [Verification plan](GEOMETRY_DELAY_CHECK_PLAN.md)

Gemini 3.1 Pro Preview accepted the source-only proof, the delayed witness, the terminal construction, and the grade consequence. The replay and independent readback obtained certificate SHA-256 9568252eb6e4a745a75bc1ecccb8cece1fe2499f43249258064e1cf576239827. The raw review and final audit also match the publication logs. [Verification run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45045697709) · [Worked review](geometry_delay_evidence/review_verdict.json) · [Raw review](geometry_delay_evidence/geometry-delay-review.zip) · [Readback receipt](geometry_delay_evidence/readback.json)

The calculation uses the constructed initial cover and the supplied field for the fixed square. Existing v16.26 laws permit both recovering trajectories and a terminal future without geometric recovery. A source-driven rule that makes recovery happen, selects a receiver, and exposes an accessible physical record remains open.
