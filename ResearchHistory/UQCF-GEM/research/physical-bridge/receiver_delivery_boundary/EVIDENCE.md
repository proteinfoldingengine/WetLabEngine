# T-240 evidence

- Exact parent: `dbe016b6f15298280650a50025fe7f20f123b2da`. Preregistration: `b20ae69f2e648dd39aec391367254d53b3720dad`. Science and workflow SHA: `0c05b4e132ad18acd21f64ec1318d9fdb41e7fd4`.
- The research branch later advanced to `8ca3d886` with documentation only (the GPT Work directive record and source audit). No inspected source file changed.
- Actions run [41313483346](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/41313483346), attempt 1. All jobs succeeded:

| job | id |
|---|---|
| inherited-fcv-stack | 124868566209 |
| produce | 124868996609 |
| verify | 124869303034 |
| publication | 124869557284 |
| argument-review | 124869848214 |

- Inherited stack:
  - test_fcv: 22 tests OK.
  - PUBLICATION_SHA256SUMS: OK.
  - verify_certificates: OK.
  - test_pruning_consistency_audit: 15 tests OK.
  - The job log records workflow_sha = science_sha = 0c05b4e1.
- Verification: verifier status GREEN. All 10 gates (P1-P7, producer hash, exact record set, identical records) passed on 30 records. All 10 rejecting controls were rejected, and the baseline was accepted.
- Publication: REPRODUCED. A fresh certificate and a fresh verification were byte-identical to the produced and verified artifacts.
- Local disclosure: the Actions artifacts are byte-identical to the local post-preregistration run of 06:49 MST. That run is in the box scratch area and is not committed.
- Argument review: gemini-3.1-pro-preview, one request.
  - verdict ACCEPTED, with findings, missing_assumptions and counterexamples all empty; native_bridge_status NOT_DERIVED.
  - prompt sha256 `5a8a3bb5e710b9ff2474260504b231d96ae825a2139a32763868ddd3fc61bc57`
  - response sha256 `2e32953cda97ed15ecc149da5b7a6203d49c182b2a284fcb2fe8e74c97e12c9e`
  - verdict.json sha256 `37f1b3226d22259f7d343dcf7e49be0ce8ae2b297da13f3cb02159ccde570da2`
  - This is a model argument review. It is not the independent scientific review required before merge, and it does not certify anything.
- Digests:

| file | sha256 |
|---|---|
| certificate.json | `5611e43acbb80b0b2c63c3abd979ac8202d19528a2f59e6e984a1520d183c01f` |
| verification.json | `aa1978855bbedecdeffba544a00cb1dee8883c247cb4f0c1e31bb82a72100290` |
| controls.json | `7a479167480e2c1458f20d6e5096549cc44df24a16f25fd603af0cb75eadd978` |
| environment.txt | `f1cb3836e68933b3692cb0b3f34c380b9d7014aaa4aa173c34708cbccba4d2b7` |
| publication.json | `65189e9c952d05a4310769031956f3f4ba347bdfea4ecf9c33027cf58f811722` |
| produce.py | `16290875feae5612e225225d2629b7fd5e05318d1970f52a673421a0b5901d55` |
| verify.py | `d5ec1b6e2b5b4256396500d8e1acd38d48573d32e866c741b0efdb5f224126b7` |
| test_controls.py | `76cabfba97206f8d36d466432aa4a9f0ff252bae244d203474a2cf3423b2790d` |

- Artifacts are copied under `evidence/actions-41313483346/`. Their SHA256SUMS and the review artifact_manifest were rechecked after download.
- Status: STAGE_1_SCOPED_THEOREM_PACKAGE_PENDING_INDEPENDENT_REVIEW. Not merged, not CLOSED, not CERTIFIED. claimStatus is unchanged.
