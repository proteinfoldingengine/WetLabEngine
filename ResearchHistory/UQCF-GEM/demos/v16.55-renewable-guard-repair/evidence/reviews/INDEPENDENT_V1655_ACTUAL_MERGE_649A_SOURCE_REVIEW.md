# Independent v16.55 actual-merge split source review

Reviewer: independent Codex agent `/root/v1655_implementation_review`.
Date: 2026-10-04 UTC.
Exact head: 649a2c96ed7775bc13d80bb1f9e3dee0b135096d.
Decision: CHANGES REQUIRED. No merge, execution or certification approval.

Read exact actual-merge adapter blob6c4faff932ac01720ca67ca4706fb5d2a5a4bf76, workflow06193b60eefe1844b5901a875c4076a1f27fb4f2, transport, recovery helper, tests and base-to-head delta. No local scientific execution or tests performed.

## Important blockers

1. `package()` sets archive = scratch / "originals" / (<id> + ".zip") but never creates scratch/originals. `publish.download()` opens that destination for writing without creating its parent. The first original transport therefore fails with FileNotFoundError. Create the parent and add a real orchestration fixture covering initially absent transport directories.

2. Component admission checks a self-authored metadata manifest but lacks exact per-component metadata filename inventories. It does not consume/validate FULL_CONTROLS.json, verify complete ORIGINAL_MEMBER_MANIFESTS.json role coverage, or compare those rows to the raw originals downloaded during packaging. A consistently edited manifest can omit these required metadata or retain substituted member maps and pass existing selected summary/status gates. Require exact metadata inventories, source-derived scientific and mechanical control ID multiplicities, exact ledger/member-map identities, and stream-check original ZIP member maps while packaging already downloaded originals. Reject duplicate ZIP member names before extraction can collapse them.

Exact metadata sets: common eight names are STATUS.json, ORIGINAL_RUN.json, ORIGINAL_ARTIFACTS.json, PRODUCING_JOBS.json, EXECUTABLE_SOURCE_BINDING.json, ORIGINAL_ARCHIVE_AUDIT.json, ORIGINAL_MEMBER_MANIFESTS.json, MANIFEST.json. Primary adds AGGREGATE.json, SCIENTIFIC_BYTES.json and FULL_CONTROLS.json (11 total); reproduction adds AGGREGATE.json and SCIENTIFIC_BYTES.json (10); inherited adds INHERITED_AGGREGATE.json and FULL_CONTROLS.json (10). Required original ledger roles are nine primary (eight plus controls), eight reproduction, eleven inherited (development/eight domains/foundation/controls). Shared control identity must agree exactly. The unique union is exactly27. Member maps must cover each declared original ID, with unique complete name/length/digest rows; compare to actual original ZIP members, not just another self-authored summary.

## Sound portions and required follow-up

The topology retains all primary/reproduction/inherited scientific work and separates full expensive audits into parallel jobs; the metadata join avoids sequential full path replay. Actual context requires integration ref/two-parent merge, HEAD/event/workflow equality, explicit current provenance and exact producing jobs. Real GitHub raw job metadata independently confirmed run_attempt exists. Seven external executable workflow/helper/test roles are mandatory in source closure, with exact regular blob selection. Merge parent, preregistration, source inventory and reporting exclusion gates remain explicit. Per-component source/provenance/full identity/record/resource checks, 83 inherited controls and77 certified hashes are reused without GitHub environment spoofing. Temporary extraction stays outside published output; originals split once; Git publication uses an absent-ref lease and a fresh isolated evidence branch. Mathematical producers, verifier, floors and domains are unchanged in the inspected delta.

Operational limitation: validating every artifact in the whole run against the current attempt rejects older-attempt artifacts on reruns. It fails safely, but if reruns are intended, filter exact current-attempt required artifacts and continue rejecting stale evidence at selection. Do not weaken selected artifact provenance.

Add real rejecting controls for missing/extra component roles, omitted/duplicated/wrong full control IDs, missing/extra member-map IDs, changed member names/hashes/lengths, duplicate ZIP names and cross-component original substitution, plus the absent transport parent fixture. Preserve prior RED history. Prefinal GREEN37209718372 was independently observed terminal SUCCESS; it precedes the final workflow edit and does not replace fresh exact final-source GREEN/review. Return corrected frozen source for follow-up. Actual merge contract, full replay evidence, immutable publication and independent final whole-argument review remain later gates.
