# Independent review of the V1712 patch write

Gemini 3.1 Pro Preview accepted the [frozen derivation](V1712_PATCH_WRITE.md) on its first review. The native physical bridge remains open. The reviewer reconstructed the write, the tensor coefficients, the caller medians and the rejecting controls. [GitHub Actions run 44952553649](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44952553649)

## Verified result

The original V1712 caller replaces adjacent patches with a computed patch state and uses the returned state for its next-scale non-metricity calculation. A matched four-patch fixture fixes the left patch and the right-patch total. The old-scale median is 0.3547220179 in both arms. At block size two the baseline is 0.3547220179 and the changed arm is 0.3549475352. An exact rational reconstruction gives a squared Frobenius-norm contrast of \(3201872665419/10^{16}\) in the first written patch. The checker substitutes fixed samples for the Gaussian initialization and executes the archived `Q_at_scale` body. Its replay agrees with the rational reconstruction. [Exact output](evidence/v1712_patch_write/replay.json)

Rotating the right-patch contrast changes the written vector and leaves the scalar norm unchanged between the two orientations. A change parallel to the left patch alters the right-patch total and leaves the written patch unchanged. At zero coupling the two preparations give identical writes and zero tensor. The parallel control distinguishes this patch write from literal P1 addition. A physical event choosing the adjacent pair, a receiver with access to the result and an observable gravitational correspondence still require a producing operation.

## Immutable evidence

The reviewed scientific commit and workflow revision are both `3eed004b75346d34ca6b0698cf27f213da4f6733`. The raw response SHA-256 is `6a0388cea8cb9894ce63486b63bc94e9f8bfa379b028b1eb7859a0c588c4a575`. The replay, argument review and fresh publication replay all passed. All three original ZIPs were downloaded and checked against their GitHub byte counts, SHA-256 values and member CRCs. The local replay, initial GitHub replay and publication replay are byte-identical. The publication log's encoded raw response and audit agree exactly with the extracted ZIP members. [Readback receipt](evidence/v1712_patch_write/readback.json) · [Parsed verdict](evidence/v1712_patch_write/review_verdict.json)

- [Replay archive](evidence/v1712_patch_write/v1712-patch-write-replay.zip)
- [Original independent review and raw response](evidence/v1712_patch_write/v1712-patch-write-review.zip)
- [Fresh replay and publication audit](evidence/v1712_patch_write/v1712-patch-write-publication.zip)
- [Full job logs](evidence/v1712_patch_write/v1712-patch-write-logs.zip)
