# Scientific publication and pending external review

The [proof and finite comparisons](../COVER_RETURN_WRITE.md) are frozen at `f50d0bcd266662a0420b4dca66f0d16cb90f7a2d`. [Run 45495339040](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45495339040) passed the scientific replay and foundational regression. The Gemini generation endpoint returned HTTP 402 before producing a review. The [three original archives and the failure log](first/) preserve that attempt.

[Run 45495892100](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45495892100) used the same research and historical code, and a smaller request to the same Gemini model. Both the first and second model metadata lookups succeeded. Both generation requests returned HTTP 402. The external review job consequently failed in each run. The second workflow separately completed the fresh scientific publication at `6e5c4d85ce36284aa5338a72d216b6a40d4856aa`.

| Second-run archive | Verified contents |
|---|---|
| [Scientific replay](cover-return-replay.zip) | Complete 2,112-arm comparison, 81 supplemental arms, ten bounded first-return graphs, byte-matched v16.54 original record and independent reconstruction. |
| [Foundation](cover-return-foundation.zip) | 21 verified certificates, 22 foundational tests, 15 parent tests and 2 historical tests. |
| [External request](cover-return-review.zip) | Exact compact prompt and request, model metadata, and the recorded generation-stage HTTP 402. The provider returned no model verdict. |
| [Fresh scientific publication](cover-return-publication.zip) | Scientific files independently reproduced from a fresh checkout, complete numerical replay, foundational verdict, and explicit provider failure readback. |

All seven original ZIPs matched their GitHub lengths and SHA-256 digests. Scientific manifests, exact output bytes, raw request identities and the publication job's independent echo of the external status were verified. The two reports of failed generation carry no scientific assessment. The research remains on the draft branch.

[Run metadata](run.json) · [Verified receipt](verified.json) · [Publication status readback](publication_readback.log) · [Primary registration](../COVER_RETURN_WRITE_PLAN.md) · [Budget registration](../COVER_RETURN_BUDGET_PLAN.md) · [Reduced-request record](../COVER_RETURN_REVIEW_RETRY.md)

To verify from a checkout, run

```bash
python ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/cover_return_evidence/audit_publication.py
```
