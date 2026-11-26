# Three source-pinned reviews of the four-withdrawal receiver result

The [frozen proof and code](../equal_population_receiver_writes/RESULT.md) are at 59944c623217b7bc4b78573b9b16e3723a10ea25. Every run used the same science files, produced byte-identical results.json and verification.json, and passed the inherited foundation tests and certificate check. Review requests 2 and 3 clarified response formatting. The validator and mathematics stayed the same. Every raw response, including the two rejected by the automated gate, is preserved below.

| Run | What the original response said | Automated gate |
| --- | --- | --- |
| [45905912972](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45905912972) | ACCEPTED, mathematical result DERIVED, native bridge OPEN. [Verbatim](run1/review.txt) | Failed. Two fields required to be arrays were strings. |
| [45906118566](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45906118566) | ACCEPTED, mathematical result DERIVED, native bridge OPEN. [Verbatim](run2/review.txt) | Failed. The model placed five supporting conclusions in the array reserved for unresolved defects; the gate refused the nonempty array. |
| [45906340146](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45906340146) | ACCEPTED, mathematical result DERIVED. The native-bridge field says DERIVED, while its proof checks and limitations explicitly say endogenous scheduling and physical delivery are unestablished. [Verbatim](run3/review.txt) | Both jobs passed, including original-response and source-integrity validation. See [machine receipt](run3/publication_audit.json). |

**Scientific adjudication.** The exact four-withdrawal minimum and the conditional first-gain result are supported by the programs and all three written mathematical assessments. The last response is internally inconsistent on the physical question. Its positive bridge label has no derivation and is rejected. The native bridge remains **OPEN**. The proved source-last collision, supplied cover and invocation, and loss of the distinction by termination are documented in the frozen proof. No new review was solicited to change the label after this discrepancy was identified.

For all six original archives the digests matched GitHub Actions metadata, ZIPs passed their integrity tests, and every available checksum manifest matched. The third review archive includes the full prompt, request, source-bound audit and raw response. The first two review archives retain all evidence the failed jobs actually uploaded.

| Run | Original archive | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| 45905912972 | [receiver-write-review](run1/receiver-write-review.zip) | 69,866 | `4fe2cd2d0bd9d365ce9f1f64eefc27368dda24f6623c59bb4a6935dcf3d88f27` |
| 45905912972 | [receiver-write-foundation](run1/receiver-write-foundation.zip) | 307,064 | `f9bf1bdcd794a78b2a4407f29880609a69f33f428b17e7ac2566d6b676c92342` |
| 45906118566 | [receiver-write-foundation](run2/receiver-write-foundation.zip) | 307,061 | `dbd7ece3914287e8805d1422d8bd55973aaf0fce3ff6408132b8e223d5eb5ac4` |
| 45906118566 | [receiver-write-review](run2/receiver-write-review.zip) | 76,579 | `dc4a99fbf3918ec95ee122ad177c9df5b37ddd48a74b628d328309fad29aa3d9` |
| 45906340146 | [receiver-write-foundation](run3/receiver-write-foundation.zip) | 307,061 | `1d44fc3e24c0e0207e4228d8843380eaeedfd23062fb31a8d412e03ea88ddddc` |
| 45906340146 | [receiver-write-review](run3/receiver-write-review.zip) | 121,394 | `5a11674db8f97a9ea5ed891aebb7d44fd3307c4d400a74966caf16eb7a4ad830` |
