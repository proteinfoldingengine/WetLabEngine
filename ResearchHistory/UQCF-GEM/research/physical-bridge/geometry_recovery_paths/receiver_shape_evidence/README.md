# Receiver shape verification

Science revision `27790d4ee92a79196dfd7f2ed001ab9cb0bcbe25`. Historical algorithms and foundation revision `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`. The preregistrations were committed at `1b138d7c0cefde8e613179050fb7752c6b32447f` and `5b266b4d34515ed12787cbac0594274f8056cec2`, before experimental execution.

| GitHub job | Disposition |
|---|---|
| Scientific replay | Passed. All 5,184 executions matched the independent reconstruction. All 12 deliberately corrupted inputs were rejected. |
| Foundational regression | Passed. All 21 certificates verified. The three inherited test suites passed 22, 15 and 2 tests. |
| Fresh publication | Passed. A second checkout reproduced both scientific outputs byte for byte and read back the provider disposition. |
| External review | Gemini model metadata succeeded. The generation request returned HTTP 402. No model verdict was returned. GitHub marks the overall workflow as failed. |

The four ZIPs are the original downloads from GitHub Actions. Their API artifact identifiers, sizes and SHA-256 digests appear in `run.json`. The verifier checks the ZIPs, internal manifests, frozen request, logs, marker bytes, scientific files and foundational certificates. `publication_readback.log` contains the two exact marker payloads retrieved from the job log. The local preflight pin correction is recorded separately. Run `python receiver_shape_evidence/audit_publication.py` from the geometry_recovery_paths directory to reproduce `verified.json`.

The result remains on draft PR 156. It establishes use of the fork's holder data by the invoked constructor. Physical receiver access and a rule forcing invocation are open.

[Scientific workflow and job logs](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45536467507) · [Proof at the tested revision](https://github.com/proteinfoldingengine/WetLabEngine/blob/27790d4ee92a79196dfd7f2ed001ab9cb0bcbe25/ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_SHAPE_CALLER.md)
