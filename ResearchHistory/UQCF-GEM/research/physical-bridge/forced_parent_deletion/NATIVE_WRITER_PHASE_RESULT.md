# A pruning certificate leaves the historical receiver write undetermined

The archived retained-tree programs make real changes to their indexed views. I checked whether their receiver action is determined by the complete source pruning and the saved cover profile. Two original examples show which additional information the programs use. [Proof and source trace](NATIVE_WRITER_PHASE.md)

| Historical path | What is identical | Receiver on the writing continuation | Receiver on the silent continuation |
| --- | --- | --- | --- |
| v16.53, row 2835 | Same run and preparation, target (2,3), complete source event, and consistency-height rise 2→3 | View 2 acquires vertex 6. Root grade goes 4→3. | View 2 stays at root grade 4. |
| v16.52, rows 5402 and 5403 | Same full event, saved target and whole receiver-local history through the event | View 1 acquires vertex 7. Root grade goes 7→1 at its first write. | View 1 stays at root grade 7. |

In v16.53 the later ten edits repeat the earlier ten edits exactly. At the first rising deletion the outer root-support lift is still pending. At the repeated deletion the lift is finished. The view 2 update belongs to that intervening lift. An adjacent pair of identical height-preserving deletions gives the same result even though the later occurrence still has a subsequent deletion elsewhere.

In v16.52 the receiver's entire own history before and through the source deletion is the same constant mask in both original preparations. One run is moving a role and uses view 1 as a temporary recipient. The other is trimming a holder during child normalization and never changes view 1. The first program returns view 1 to its original state by completion. The contrast occurs at the receiver's first actual change, measured in its own retained record with unit ambient grades. [Original suffixes and complete event certificates](native_writer_phase_evidence/native-writer-phase-replay.zip)

These cases isolate a required distinction beyond the pruning certificate and saved cover profile for replaying the historical receiver response. A native rule would have to carry information equivalent to the relevant execution choice or independently force a receiver change. The archived continuations use incidence additions as well as deletions. The native physical invocation and access to the transient grade remain open.

## Verification

I reconstructed both original GitHub archives from their committed chunk manifests. The copy of the v16.52 certificate inside v16.53 has the same SHA-256 as its member in the original archive. The frozen check verifies the v16.53 archive and all its chunks, reproduces every record in both historical certificates with the original producers, checks the three full paths with the corresponding upstream verifiers, and verifies all six atom occurrences independently. It checks the P1 grades and replays each silent suffix through its original end. All 7,236 v16.52 records and all 2,863 v16.53 records match the archive objects exactly. [Plan and prior explorations](NATIVE_WRITER_PHASE_CHECK_PLAN.md)

Gemini 3.1 Pro Preview accepted the mathematical result and left physical delivery open. Its scope field lists the combined controls. The fixed preparation applies to the v16.53 pair and the matched receiver-local history applies to the v16.52 pair. Both GitHub replays and the independent frozen checkout reproduced certificate SHA-256 88ca4777cb390e7cd400f356b950797adc2726646e0cbb5b3853b5676ceebc23. The raw review and final audit match the publication log. [Verification run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45048629395) · [Worked review](native_writer_phase_evidence/review_verdict.json) · [Raw response, request and prompt](native_writer_phase_evidence/native-writer-phase-review.zip) · [Readback receipt](native_writer_phase_evidence/readback.json)
