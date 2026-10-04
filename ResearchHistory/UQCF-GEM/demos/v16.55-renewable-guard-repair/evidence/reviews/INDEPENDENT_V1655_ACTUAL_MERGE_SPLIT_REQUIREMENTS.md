# Independent v16.55 actual-merge audit split requirements

Reviewer: independent Codex agent `/root/v1655_implementation_review`.
Date: 2026-10-04 UTC.
Assessment only: no implementation, execution, merge approval or certification.

Inspected candidate fcf6c9299ca8502152aa560231dbd41e01310e85: transport.py blob 0f620df98a9eae550cb5913c38fef0209ce7480f; full validation workflow blob 13a88b1ee8ad3016864f5ce7659d5c5472192098; current publication.py and inherited_aggregate.py. The existing final publication job performs primary and reproduction full independent verification sequentially, then inherited verification. Original run 37180275767 timed out after its first complete new-domain aggregate, before terminal publication. It cannot be treated as an adequate actual-merge closure topology unchanged.

## Minimal architecture

Retain the current fresh scientific execution jobs and their declared eight-shard/full-domain identities. Replace the final monolithic audit with three parallel audit jobs, each <=60 minutes and <=4 GiB:

1. Primary audit: independently download/hash/reconstruct all eight current-run primary artifacts and the full new control artifact; verify every input, identity, record/path, domain freeze, source inventory, potential/diagnostic/resource counter and full exact control membership.
2. Reproduction audit: independently download/hash/reconstruct all eight current-run reproduction artifacts and verify the same entire domain; emit complete deterministic scientific file hashes and aggregate.
3. Inherited audit: independently download/hash/reconstruct current-run development, eight inherited-domain and foundation artifacts; verify complete streams, source manifests, provenance, the exact 83 frozen inherited control IDs with multiplicity/no skips, all 77 certified baseline scientific hashes, and the full foundation stack and metadata.

A packaging-only join downloads the three component audit artifacts, independently binds their metadata/digests and exact current run/SHA/attempt/workflow, requires terminal PASS, checks primary/reproduction complete scientific file equality and aggregate equality, exact required diagnostic coverage, ledger cardinalities and no missing or ambiguous original artifacts. It publishes complete manifests/provenance with certification explicitly pending whole-evidence review and actual-merge audit. It must not repeat the expensive full path verifications sequentially. Component outputs require complete verified evidence/ledgers, not unbound summaries. Retain incomplete output through if:always on failure; no package PASS if any prerequisite failed/timed out.

## Context and source contract

All producer and inherited jobs must actually execute at the two-parent integration merge: HEAD = GITHUB_SHA = GITHUB_WORKFLOW_SHA. Keep existing native primitives, supports, floors, palette, domains, resource limits and frozen inherited checks. Use the actual current run/attempt for artifact names and provenance. Earlier original60c/recoverya75 artifacts remain evidence of earlier executions and cannot substitute for actual-merge replay.

Do not directly invoke the existing recovery adapter with its hardcoded original-cancelled and recovery tuples; factor/reuse its independently reviewed validation logic with an explicit current-run context. An in-progress current run cannot be required to have terminal overall SUCCESS before its audit jobs finish; require its exact identity and successful producing-job outcomes, then assess final run conclusion after packaging. Do not spoof GitHub environment to make prior-run provenance match.

The validation workflow belongs to transport.scientific_inventory. Changing it therefore changes the admitted source contract. Freeze and review a new exact source inventory before composing MERGE_CONTRACT; retain the already accepted mathematical source/domain and identify the mechanical audit delta. Explicitly bind every new audit/package script, test and workflow in the executable dependency closure, including scripts outside the demo directory if used. Do not silently rely on the current selector to cover new .github/scripts files. MERGE_CONTRACT must continue to bind exact preregistration, authorized first integration parent, reviewed-source ancestry of second parent, exact membership/blobs at reviewed source and actual merge, fixed reporting exclusions, and certified parent ancestry. This topology change is mechanical execution repair within the existing per-job/domain protocol; no new scientific domain or resource expansion is proposed.

## Required rejecting controls and review gates

- Reject nonmerge/one-parent/wrong-first-parent events, unreviewed second-parent lineage, modified workflow/helper/source blobs, partial inventory and expanded reporting exclusions.
- Reject wrong current run/SHA/attempt/workflow or artifacts from a prior successful run; reject ambiguous/missing/expired artifact names, wrong external lengths/digests and malformed ledgers.
- Reject omitted/repeated shard/identity, changed scientific bytes, incomplete/failed/skipped controls, missing pair/path/progress evidence, inaccurate counters/resources and typed outcomes substituted for successful paths.
- Reject inherited domain source membership/hash substitutions, foundation metadata mismatch, missing/duplicate control IDs and any of the 77 baseline hash changes.
- Reject a component with INCOMPLETE despite partial successful contents, missing join component, substituted component artifact, primary/reproduction mismatch, and premature numbered certification. Test the parameterized current-run context without environment spoofing.
- Demonstrate source-review acceptance and real GitHub RED/GREEN controls before merge. Freeze exact executable source and review MERGE_CONTRACT/merge candidate before performing the two-parent merge.
- After actual-merge execution: audit exact GitHub merge tuple, all new/reproduction/inherited original archives, three audits and join, preserved failures, durable evidence reconstruction and complete immutable source readback. Only a fresh independent whole-evidence actual-merge acceptance can support closure.

No broad campaign redesign, producer algorithm changes, relaxed verifier checks or scientific rerun before the actual-merge replay is needed for this mechanical split.
