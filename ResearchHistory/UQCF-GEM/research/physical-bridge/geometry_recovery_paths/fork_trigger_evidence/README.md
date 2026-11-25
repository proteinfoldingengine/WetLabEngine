# Fork-trigger verification

The [proof and controls](../FORK_TRIGGER.md) are frozen at `c5e0fe3798a2a069610826aeade206b5cae1924c`. The [GitHub run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45505283081) completed the native replay, independent reconstruction, all 21 foundational certificates and a fresh publication. The independent implementation rebuilt 912 complete histories and the historical caller's full paths for all three target choices on 168 source arms. The Gemini generation endpoint returned HTTP 402 before providing a verdict. Its failed job is recorded independently of the completed scientific publication.

| Original archive | Verified contents |
|---|---|
| [Scientific replay](fork-trigger-replay.zip) | Registrations, proof, method, full native graphs and labeled histories, complete caller paths, independent outputs and checksums |
| [Foundational regression](fork-trigger-foundation.zip) | 21 verified certificates, 22 foundation tests, 15 parent tests and two historical tests |
| [External review request](fork-trigger-review.zip) | Exact prompt and request, model identity and provider status |
| [Fresh scientific publication](fork-trigger-publication.zip) | Newly reproduced scientific outputs, independent logs, foundational verdict and exact external status readback |

All original archive lengths and SHA-256 digests matched GitHub. [Run identities](run.json) · [Verified receipt](verified.json) · [Publication markers](publication_readback.log) · [First local verifier and original failure trace](initial/).

To repeat the archive checks from the containing scientific directory, run `python fork_trigger_evidence/audit_publication.py`.
