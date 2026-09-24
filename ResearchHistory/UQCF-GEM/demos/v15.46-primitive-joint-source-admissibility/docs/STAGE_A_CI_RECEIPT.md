# v15.46 evidence-preflight CI receipt

Evidence checks passed; native source admission remains unresolved.

- Exact executed head: `885cc796e48b9d07fae8095e5733f4c5da530d6d`.
- [GitHub Actions run 35945673712](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/35945673712), job `107462930892`: completed SUCCESS.
- CPython 3.13.5; 28/28 tests passed in 1.117 seconds (20 new preflight tests plus the 8 preserved typing-probe tests). Zero failed, errored, skipped or expected-failure tests were accepted.
- The actual repository checkout verified all ten inventory source files against their pinned Git blobs. Source artifacts were read as bytes, not executed by the preflight.
- The Stage-A result replayed byte-for-byte. SHA256: `2768cbcc51325f251f1814dd53bd76e9d02de062359b6c054638c1fddc5e6bb8`; Git blob: `12fb7baa8d909625b1c778ef32357cf45f9b0309`.
- The original 195-check proof output and the original typing-probe result both replayed byte-for-byte.
- Compilation, no tracked-file mutation, both certified predecessor directory hashes and exact checkout identity passed.
- The runner emitted `V1546_STAGE_A_VERIFIED_HEAD 885cc796e48b9d07fae8095e5733f4c5da530d6d`.

`STAGE_A_RESULTS.json` was recovered from the complete emitted CI output. Its local SHA256 was checked against the runner's printed SHA256 before committing this receipt and the result. This later commit adds documentation/result bytes only; it is not represented as a new CI-tested scientific head. The source and test blobs remain those executed above.

## Interpretation

Computed status: `EVIDENCE_PINS_VERIFIED_NO_COMPLETE_WITNESS_SUBMITTED`.
First unmet admission stage: `A_NATIVE_INPUT_WITNESS`.
Submitted complete witness packets: zero. Source value: `NOT_EVALUATED`.

This count describes this study's explicitly submitted packet, not an exhaustive proof of absence from every archive. Mathematical joint states are present in the reviewed sources. Their existence and verified file identity do not establish primitive provenance, state-to-occurrence addressing or a physical coupling law. Even a complete set of file references is deliberately not accepted as native-source certification.

This is a verified evidence preflight and replay of existing mathematical controls, not a new gravity result, a complete v15.46 source-admission certificate, an independent review, or a full-repository regression. Later state/support/coupling stages remain unexecuted on a native candidate. No source law is adopted. Pillar 3 remains OPEN.

v15.44 and v15.45 remain published on main through PR #58; their scientific snapshots are unchanged. v15.46 remains on research PR #57 and is not newly merged into main by this receipt.
