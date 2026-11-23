# Independent review and exact readback

The frozen [proof and review workflow](https://github.com/proteinfoldingengine/WetLabEngine/commit/311ea4c696ac3147d8f91d3930753c8a438c1b53) were checked in [run 45108722361](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45108722361). Gemini 3.1 Pro Preview independently reconstructed all five requested calculations. The verdict was ACCEPTED with the native bridge OPEN. The publication job rebuilt the prompt and verified the request, returned response, and audit bytes on the same head.

The original downloaded archives matched the GitHub Actions SHA-256 digests. The response and publication audit also matched the independent workflow log readback byte-for-byte.

| Archive | Artifact ID | SHA-256 |
|---|---:|---|
| [depth-two-publication-audit.zip](depth-two-publication-audit.zip) | 14788249007 | `84497ffaa53631aecbbfb31e2356a571be0a10472a2cf2fd4ecd0d527ebee7fa` |
| [depth-two-review.zip](depth-two-review.zip) | 14788138242 | `0aa9a7260248f4b4098bcc06aa1754a06b6b8d267bb425c0eaf6093a134e14d9` |

The review addresses the analytical two-edit proof. The preregistered numerical enumeration is a separate deliverable. Physical receiver access and recovery enforcement remain open.
