# T-235 — Evidence (Actions run 41249635984)

Run: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/41249635984 (attempt 1, push of `a7a6c2ce589a1168fe38e1b61f840a4633c56b9c`, workflow SHA = scientific SHA = `a7a6c2ce`). Started 3:46 PM MST, all five jobs succeeded by 4:01 PM MST. Run 1 of at most 2 allowed by the prereg; no second run was needed. One Gemini request, no retry.

| Job | Result | Logs inspected |
|---|---|---|
| inherited-fcv-stack | success | FCV tests/test_fcv.py: Ran 22 tests OK; `sha256sum -c PUBLICATION_SHA256SUMS`: 58 lines OK; verify_certificates.py ran clean; v15.56 test_pruning_consistency_audit: Ran 15 tests OK (Python 3.11.17, sympy 1.13.3, mpmath 1.3.0) |
| produce | success | certificate.json sha256 `c3a9c6721090c887d3263a7878c4b791faadc6ed9d8f6db25e8ccfe25fab5101` (byte-identical to the disclosed local run) |
| verify | success | verification.json GREEN: 56 P cases, 1440 basis reads, 151 O cases, 1073 carriers, tree counts 1,1,2,4,9,20,48, all 8 scientific gates true; controls.json GREEN: honest accepted, 16/16 tampers rejected |
| publication | success | fresh producer run byte-identical to the producer artifact; fresh verifier output byte-identical; status REPRODUCED |
| argument-review | success | verdict ACCEPTED, findings/missing_assumptions/counterexamples/limitations all empty, native_bridge_status NOT_DERIVED; model gemini-3.1-pro-preview; prompt sha256 `4dea3cbb…e7cc`, response sha256 `b9483bda…ff70` |

Artifacts (GitHub-reported digest = sha256 of the downloaded zip, re-checked on the box):
- pair-delivery-evidence-1 (13060799998) `sha256:815d8daca7338b5c64491c09c86216f5ab305b87a068f58c8303e09e27ee1749`
- pair-delivery-review-1 (13060658830) `sha256:9a1a976ea06b25415f3c7276740453b38800a698876a63ffeaf5c3671ee71e22`
- pair-delivery-produced-1 (13061075901) `sha256:5a9f5720b833f3ca034031ab9379e31dd117d93f34042fa8740491b5d8425515`
- pair-delivery-verified-1 (13061221201) `sha256:ebb1cb2e1b80ae7da4c59a2fd90f6e66b66238b81740af07c225a671fce7549b`

Committed copies: `evidence/actions-41249635984/evidence/` (SHA256SUMS checks OK) and `evidence/actions-41249635984/review/` (artifact_manifest.json checks OK, 8 files). No API key appears in any file.

File digests: certificate.json `c3a9c672…5101`, verification.json `34da4b2a…85c0`, controls.json `da0996e1…7c`, environment.txt `f1cb3836…b7`.

What this evidence is: bounded exact checks of Theorem P, Remark P.2, Props K, N, O on the preregistered universes, plus one external argument review. The general claims rest on the typed proofs in RESULT.md. What is still missing under AGENTS.md: human/agent review on the PR, merge into the research branch, and the post-merge audit of the merge SHA. Until then the stage is not CLOSED or CERTIFIED. Native bridge NOT_DERIVED. scientific_breakthrough false.
