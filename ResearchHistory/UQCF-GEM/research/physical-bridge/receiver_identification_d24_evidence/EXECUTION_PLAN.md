# D24 Range-Certificate Regeneration Execution Plan

> For agentic workers: use subagent-driven development for implementation and a fresh static reviewer before publication. Do not perform scientific execution before the prospective publication/readback gate below.

**Goal:** retain independently checkable range certificates for the already accepted D24 finite result, preserving the exact original summaries and all original evidence.

**Architecture:** additive copies export certificates from the unchanged producer/checker mechanisms; a separate stdlib validator reconstructs every class and constraint. One initial Actions job creates certificates, and a later publication-reproduction job regenerates both roles in fresh processes, compares complete bytes, and runs all required controls. Repository publication follows successful original-artifact reconciliation and immutable readback.

**Tech stack:** GitHub Actions ubuntu-24.04, Python 3.12.15, numpy 2.3.5, scipy 1.16.3; rational arithmetic with Fraction; SHA256 and git blob identities. Official actions are pinned to the already used immutable action commits.

**Spec:** ARCHIVE_CONTRACT.md in this directory. The original frozen RESULT/FREEZE and accepted review remain authoritative for the unchanged mathematics.

## Global constraints and status

- Repository proteinfoldingengine/WetLabEngine; only research/uqcf-overlapping-guard-exchange; authenticated author proteinfolding-gpt.
- Admission B: narrow evidence support. No new native construction, access derivation, theorem, domain extension or Gemini rerun.
- Original scientific code SHA 57895f62297c6100c1a4b8f185857a7905da780b; frozen construction 3e6f1cf3042ed3c6cd49b29d396f86cddb7bf9c6; preregistration d567148f8263de96654ea3e9bcc49fd25a0132fc.
- Original accepted run 39300667905 attempt 1; immutable acceptance receipt 5f354b33d708c48e4588215d5fbf576edeb33e9a.
- This plan is prospective for new export bytes and their checks. The mathematics, original scalar answers and prior exploratory work are already known. All five export-package files were prepared and statically reviewed without imports, tests, LPs or enumeration. There is no claim of a RED/GREEN development cycle or runtime correctness before execution.
- The contract's preparation-time local-draft/unexecuted statements describe that preparation state. This companion plan governs the subsequently authorized prospective publication and execution.
- Preserve all frozen files, original ZIPs, logs, failures and receipts. No main merge, force push, deletion, credential change or owner-account use.
- Raw Gemini responses and review ZIP publication are excluded. That separate authorization remains pending.
- One campaign only. No automatic scientific/workflow retries or reruns, expanded domains or parameter repairs after RED. Preserve RED and stop for analysis/coordination. Standard transport behavior internal to pinned official checkout/artifact actions is not a second scientific attempt; no explicit retry loop is added.

## Exact proposed additive files

Seven files are published together before execution:

1. ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_evidence/ARCHIVE_CONTRACT.md
2. ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_evidence/producer_export.py
3. ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_evidence/checker_export.py
4. ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_evidence/verify_archive.py
5. ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_evidence/test_archive_mutations.py
6. ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_evidence/EXECUTION_PLAN.md
7. .github/workflows/uqcf-gem-rid24-certificate-export.yml

The first five retain the reviewed bytes:

| File | SHA256 |
|---|---|
| ARCHIVE_CONTRACT.md | 32ac119faec345e06ccc2c3727d3a0773da93751c97e19d71ca9f59ff2047e48 |
| producer_export.py | bf00f37e603814d2ece28ed8fd5b42dbedc4a29e2fca09a7044077a09ebfba48 |
| checker_export.py | 7547f11ca4e4aa7ec4962e4c1483883aa619a7d44653c86cf2c0c026fba0318d |
| verify_archive.py | 3dede4847c25f0d5c589a32f1286a5cdf5ceb4ab8466abfc85e8a281547f739b |
| test_archive_mutations.py | 92556fb7ff0a922fd5579a63380c1b5aca0adf744b2b4c85058d8ccc7501e961 |

No original file is modified. The workflow and this plan's final hashes are bound by the separately published one-time marker, avoiding a hash self-reference.

After all seven immutable byte readbacks pass, one further commit adds only:
ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_evidence/EXECUTE_ONCE.md

This new marker is the workflow's only push trigger. No schedule or workflow-dispatch trigger is required. Its content is strict JSON with exactly these fields:

- schema: uqcf-rid24-execute-once-v1
- campaign: uqcf-rid24-certificate-export-20261019
- evidence_kind: regenerated
- prepared_commit: full 40-character lowercase prospective baseline SHA, freshly read back before trigger
- expected_files: exactly the seven repository paths above mapped to their full SHA256 values
- original_run: integer 39300667905
- max_attempt: integer 1

The runtime gate requires the named repository, exact branch, push event, authenticated triggering actor proteinfolding-gpt, attempt 1, a single-parent trigger commit, and a diff containing only this newly added marker. The marker must be absent in the parent and occur only once in the full branch history, at the trigger commit. Checkout uses full history; the gate verifies prepared_commit is an ancestor and all seven corresponding blobs at that prepared commit match the marker hashes. All seven current file hashes must also match; the five package hashes and eight original frozen source hashes are separately pinned. Later marker edits, delete/re-add attempts on normal history, or workflow reruns fail before scientific work. The publishing agent independently verifies the prepared baseline's ancestry and identical bytes before adding the marker, preserving any concurrent owner commits.

## Frozen finite output and controls

The original domain is unchanged: 30 classes; 80 primary systems; 1,030 ranges and 2,060 endpoint certificates per role, plus the separate diagnostic. Complete canonical carrier and row identities are retained. The producer uses its original LP settings and exact rational certificate checks. The checker uses its independent original proof combinations and attaining tables. They run in separate processes and import neither each other nor the independent validator.

Every new certificate archive says regenerated and carries original-contract provenance. New run ID, attempt, scientific commit, workflow SHA, prepared baseline, code/contract/plan hashes and environment are bound by outer manifests. Newly generated files never impersonate original-run certificates.

The independent validator must verify full identities, rational primal/dual feasibility, objective reconstruction, zero gap and exact agreement with the original summary bytes. It must reject invalid provenance and missing/extra/duplicated/substituted records, including count-preserving substitutions. The checker diagnostic remains attainment-only.

All 43 authored tests must execute with zero failures, zero errors and zero skips. Required environment paths are D24_PRODUCER_ARCHIVE, D24_CHECKER_ARCHIVE, D24_ORIGINAL_PRODUCER_JSON, D24_ORIGINAL_CHECKER_JSON, D24_FRESH_PRODUCER_ARCHIVE and D24_FRESH_CHECKER_ARCHIVE; D24_EXPORTER_EXECUTION_AUTHORIZED=yes enables the explicitly authorized exporter guard controls. Environment switches do not authorize execution independently of this approved campaign.

## Original input preservation

Download only original verification artifact 12211286997 from run 39300667905. Its original ZIP length is 13,890 bytes and SHA256 is 215496706fcb15cb10c5f70f46d14cabbeccbfd0bde0b3d4e6b3e18be6ffb181. Retain that exact ZIP. Verify the ZIP hash before extraction, reject duplicate/traversal/member mismatches, and extract only its six original members: SHA256SUMS, checker.json, compare.json, env.json, producer.json and producer_repro.json.

Original summary SHA256 values:
- producer.json: 04be86d04551748dca905eb2aa2cac74977d86d7edd8f2aaa5d7db9ee411a9f9
- checker.json: 9bace24c70c57cd2c62a47e1f15ce1f01977a1c86e1ba3be9f752daa384a7572
- compare.json: e2d741a54f05899075dbf6c94e3c700095506231042fe0b3a18601d17e45849e

The ephemeral Actions token is used only for authorized read access to that artifact; it is neither logged nor retained. No Gemini secret is used. No original review artifact is downloaded by this workflow.

## Resources and stopping rules

- Two sequential jobs on ubuntu-24.04, each timeout 60 minutes.
- Each job's combined scientific stage has a 45-minute timeout; the remaining job budget allows setup, environment recording and failure-artifact upload.
- The internal deadline is the earlier of 2,640 seconds (44 minutes) of combined subprocess time or 50 minutes since the first job step, reserving time for evidence finalization. Child processes have a 6 GiB address-space cap, a 1 GiB per-file cap and zero core-dump allowance; OpenMP/OpenBLAS/MKL thread settings are 1. These are resource limits, with original LP options unchanged.
- Python 3.12.15, numpy 2.3.5 and scipy 1.16.3 are exact versions. Actions checkout/setup/download/upload references use immutable known SHAs.
- Standard hosted-runner CPU/memory limits apply; no additional machines or parallel scientific jobs. No change to original LP options, rational denominator limit or finite domains.
- Unique campaign concurrency group with cancel-in-progress=false. Parent verifies live owner workflow state before trigger; no overlapping duplicate execution.
- No scientific/workflow retries. A timeout, dependency failure, missing/invalid artifact, failed certificate, mismatch, failed/errored/skipped test, or nondeterministic byte comparison is retained RED. Successful workflow status alone is insufficient.

Static inspection cannot guarantee that the full mutation suite finishes within this budget. A timeout is a failed bounded attempt, not permission to increase resources or silently rerun.

Always-run finalization/upload is a preservation attempt, not a guarantee against manual cancellation, runner loss or a platform-level hard kill. In those cases retain all available Actions logs/partial artifacts and report the precise evidence gap. The bounded original-download bytes are saved before ZIP verification, so an invalid payload remains RED evidence and is never parsed as a trusted archive.

## Task 1: prospective publication and readback

- [ ] Freshly verify proteinfolding-gpt, live branch head, governing records, continuation and concurrent ownership/workflows.
- [ ] Obtain fresh independent static review of this exact plan/workflow and five-file package. Resolve substantive code objections before publication.
- [ ] Create one current-head append-only commit containing exactly the seven files. Preserve all existing files; use expected-head compare-and-swap without force.
- [ ] Read all seven files back at the immutable commit; compare every byte, length, SHA256 and git blob identity. Verify authorship, parent and exact added-only diff.
- [ ] Recheck current head/concurrency. If owner changes conflict, pause and coordinate; never overwrite them. If later baseline contains unchanged seven files, reverify all seven there and its ancestry before choosing prepared_commit.
- [ ] Add only the one-time marker as the execution commit, then verify its immutable bytes, author, parent, only-file diff and associated workflow run. Never duplicate an uncertain trigger.

## Task 2: initial certificate generation

- [ ] Gate marker/provenance, verify all eight frozen original source hashes, and install pinned environment.
- [ ] Download and hash-check the original verification ZIP; preserve it and its six members.
- [ ] Run producer_export.py and checker_export.py sequentially in separate processes from repository root, with new output paths only.
- [ ] Validate the complete first pair against original summaries; retain its report. Any RED stops downstream scientific work.
- [ ] Always retain complete new summaries/certificates, exact stdout/stderr logs, source copies, marker, original input ZIP, environment, exit statuses, manifests and checksums in an execution artifact, including failures.

## Task 3: fresh publication reproduction and controls

- [ ] A second job depends on initial success, downloads its exact artifact and retains it without modification.
- [ ] Reverify inputs/source identities and regenerate both exporters in fresh separate processes under the same pinned environment.
- [ ] Validate both complete archive pairs and compare each role's entire certificate bytes and original-format summary bytes. Matching only scalar answers is insufficient.
- [ ] Run all 43 tests with a runner that fails on skips/count mismatch as well as failures/errors. Preserve full output and machine-readable test results.
- [ ] Always upload fresh bytes, validation reports, test results, logs, source/manifest/environment records and checksums, including partial RED evidence.

## Task 4: exact reconciliation and durable publication

- [ ] Read actual job logs, reports, complete test outcomes and run metadata. Obtain original initial/publication artifact ZIPs, hash them and inspect their complete file manifests.
- [ ] Reconcile both independently generated archive pairs, original summaries and frozen source identities. Distinguish original ZIPs from regenerated objects in every manifest.
- [ ] On RED, preserve originals and report the exact failure; do not retry or alter scientific assumptions.
- [ ] On success, publish only the permitted new certificate-support artifacts and an additive receipt/readback manifest on the same branch, preserving concurrent work. Exclude all raw Gemini review response/archive files.
- [ ] Verify immutable full-byte GitHub readback, artifact digests, source/commit relationships, authorship and intended-only diff before reporting archival support verified.

## Review focus and remaining limits

1. A count-preserving substituted universe must fail full identity reconstruction, not pass a digest/count shortcut.
2. A supplied-domain/hash override must not weaken the validator's public provenance or completeness checks.
3. A later marker edit, rerun, foreign actor, changed code or ambiguous first trigger must not produce a second scientific execution.
4. A skipped integration test or merely different path must not be reported as verified full controls or independent fresh reproduction.
5. A failed/partial job must retain evidence rather than emit a successful receipt or be silently retried.

The archive support does not derive native access, event occurrence, available physical reading, actual preparation or common read-family applicability. It preserves the accepted D24 conditional scope, full K_B^(m) domain, cumulative-A and universal-over-tables qualifications, fixed-zero exception, typed-climb premise and finite horizon. It does not provide the full inherited foundational stack, every original witness evaluation transcript, raw public Gemini archive, default-branch merge or post-merge audit. No CLOSED/CERTIFIED stage claim follows.
