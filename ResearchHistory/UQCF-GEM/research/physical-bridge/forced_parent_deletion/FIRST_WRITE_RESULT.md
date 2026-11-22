# The original writer distinguishes source branches on the receiver's first edit

A two-view preparation on the seven-site tree produces opposite changes in a signed grade at the receiver, using the unmodified v16.45 writer. Source A initially holds the whole fork. C holds both junctions and one marked leaf on each side. Each leaf has one unit of ambient grade. At C, subtract the grade at the left junction from the grade at the right. Both junctions initially hold one unit, and a source deletion leaves C untouched.

| Source action | First C reading when the writer starts at the source event |
| --- | ---: |
| A deletes its copy of the left marked leaf | +1 |
| A deletes its copy of the right marked leaf | −1 |

The signs hold across all 16 distinct inputs from both index orders and all marked-sibling choices. C's first write occurs on global edit one or two. This uses a different preparation from the previous three-view experiment. The earlier transfer-to-exhaustion rule is unnecessary for this particular fresh-start result. [Proof](FIRST_WRITE.md) · [Checker](check_first_write.py)

A separate one-edit theorem establishes how much branch ownership alone determines. After either source event exactly two union-preserving deletions remain immediately legal. The unique one preserving every local cover number is C dropping the opposite leaf. The other is A dropping its other marked leaf. That alternative preserves the global maximum, leaves C unchanged, and gives the identical complete state from either arm. Thus the global maximum cannot select the receiver write. [Exact certificates](first_write_evidence/first-write-replay.zip)

## Test of the proposed physical trigger

A positive global increment is available on the original source certificate. We tested whether an increment actually resets the archived writer. The three-index campaign contains an observed increment from one to two where the source deletes its bare left junction. The initially root-only receiver then acquires the **right** junction in the stored continuation. Starting the original writer afresh at the very same resulting tree with its newly measured profile makes that receiver acquire the **left** junction. The checker enumerates all nine global-rise visits across the two- and three-index seven-site campaign paths. This counterexample rules out universal restart on a global rise for that implementation.

The two-index matched preparation has a related phase dependence. In the primary example both fresh-run signs reverse at completion. In the archived paths that visit the two matching states mid-run, the next receiver signs also reverse. Those visits reached the states by different preceding edits. Native selection of the controller's phase and physical access to C's first write remain open. [Archive witness and replay](first_write_evidence/first-write-replay.zip)

## Verification

The initial review accepted the first-write result. The expanded review also checked the actual three-index event, both subsequent receiver writes and the insufficiency of a global rise as a launch rule. Both Gemini 3.1 Pro Preview reviews returned **ACCEPTED** on the conditional mathematics and **OPEN** on the native bridge. Each raw review and its job logs are preserved. [Initial reviewed run](first_write_evidence/first-reviewed-run.zip) · [Final worked review](first_write_evidence/review_verdict.json) · [Raw final review](first_write_evidence/first-write-review.zip)

The final reviewer uses “inherited invocations” in its last sentence. The historical writer routine is inherited. The fresh invocation in the matched source experiment is supplied. The terminal reversal is established for the primary example in the proof. No frequency estimate for that reversal is claimed. Both final CI executions and the separate frozen-checkout replay returned the identical certificate, SHA-256 `926440a03498375f6c43bd85e6210c68617e26c4944d2c5d360f143d74f38e1a`. [Final verification run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45033686612) · [Byte-level verification receipt](first_write_evidence/readback.json)
