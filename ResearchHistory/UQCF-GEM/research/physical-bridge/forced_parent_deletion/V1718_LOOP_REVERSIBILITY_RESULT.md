# V1718 source-to-loop result

November 21, 2026. The [frozen argument and reconstruction](V1718_LOOP_REVERSIBILITY.md) were exercised at commit `498a08fd3619b755aab1543f65810904d8218438`. The [GitHub run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44960357330) passed the original-source replay, independent Gemini argument review, and byte-for-byte publication replay.

| Comparison | Result |
| --- | --- |
| Two source states with the same total on the same three-edge loop | Full loop determinants 0.6889 and 0.66. The historical reader returned norms 0.83 and 1.00 on the same vector. |
| Historical reverse attempt at equal endpoints | Error 0.3111 after two applications of the forward map. |
| Inverse of the actual forward map | Reconstruction error 0 in the matched example. |
| Orthogonal control around the same loop | Norm 1 with a Euclidean displacement of 0.084974413769. |
| Separately chosen rank-loss control | Rank 7 in dimension 8. The full-cycle determinant control yielded −1. |
| Symmetric moment control and analytic independent-draw model | The one-step squared-norm factor was 1.0578. The analytic three-step factor is 1.183615620552. |

Both fixed-total loop operators are invertible. Their different determinants survive any common basis change at the base vertex. The loop response uses actual source numbers through the carried vector. The reverse test repeats a forward update, and the orthogonal control can preserve the norm while rotating the vector. The exact expected squared-norm growth comes from the independent draws and the update formula. These distinctions resolve what these particular tests show about reversibility and loop response.

The inputs in the replay are controlled toy preparations. In its normal run, the historical routine draws its source states independently and updates an eight-dimensional vector. Identifying a genuine P1 event output with a state or edge input and establishing a retained receiver's access to the resulting contrast remain necessary for a native signal claim.

[Replay and exact matrices](v1718_loop_evidence/replay.json), [Gemini verdict](v1718_loop_evidence/review_verdict.json), [publication replay](v1718_loop_evidence/publication_audit.json), and [artifact and log verification](v1718_loop_evidence/readback.json). The archives alongside these files contain the original source, raw argument review, fresh replay, and complete logs. GitHub issued a runtime deprecation warning for the pinned Actions helpers and ran them on Node.js 24.
