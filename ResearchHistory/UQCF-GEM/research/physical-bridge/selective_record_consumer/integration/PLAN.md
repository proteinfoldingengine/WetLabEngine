# PR117 Integration Implementation Plan

> For agentic workers: execute this approved integration inline; review and byte verification precede merging.

**Goal:** Put the already reviewed record-access correction and evidence on the shared research branch without changing accepted science.
**Architecture:** Preserve all 13 PR117 changed-file blobs from e5012ee19ade0a5700c789553b903494fdaaeff0, merge the current shared baseline, and add an isolated integrity workflow. Audit both candidate and actual merge.
**Tech stack:** Python standard library, Git, pinned GitHub Actions.
**Spec:** Aaron's approved next step, PR117 REVIEW_STATUS.md, UQCF-GEM AGENTS.md and STANDING_DIRECTIVE.md.

## Constraints and scope

Shared baseline d83e51a38eb47ce1acdaaa6ad08f01e7f5ff1bb9. Preserve original review and every scope limit. No model call, scientific execution, new proof, main merge, branch deletion or scientific status upgrade. This is integration infrastructure, not a numbered scientific stage. The full scientific simulation suite is not rerun; exact source preservation and the existing six-source integrity audit are the relevant inherited checks.

## Review focus

Reject changed/missing proof and archive files; extra/missing/duplicate archive members; swapped evidence identities; unrelated integration paths; concurrent target changes. Candidate and actual merge must have the same tree.

## Execution

- [x] Inspect accepted freeze, raw review, publication receipt and current target.
- [x] Write rejecting integrity tests; observe missing-implementation RED before code.
- [ ] Implement .github/scripts/uqcf_record_integration_audit.py and companion tests; freeze exact paths in CONTRACT.json.
- [ ] Run the full integration test suite and preserve RED/GREEN output.
- [ ] Commit the candidate on gpt/selective-record-consumer; run pinned Actions archive and inherited source-integrity checks.
- [ ] Inspect complete successful logs and artifacts; mark PR117 ready and merge the verified head into the research branch.
- [ ] Inspect the actual-merge audit, archive both original audit ZIPs and logs, publish a receipt, and update PR/team communication.

The manifest is prospective for these new integration checks. The analytical and archival findings described in REVIEW_STATUS.md predate it and are not relabelled preregistered science.
