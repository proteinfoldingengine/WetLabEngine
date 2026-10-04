# Independent publication consistency review — A11.X35

**Verdict: CHANGES REQUIRED for exact reporting candidate `b535eb93ce38f56d6e6f6149102e7b61ef0bf453`.**

Reviewer: independent Codex agent `/root/x35_whole_argument_review`, the attributable agent that independently reviewed the frozen mathematical candidate. Review date: 2026-10-04. This is a limited publication/reporting consistency review, not a new mathematical review, human peer review, scientific execution, numerical certification or recertification of inherited sources.

## Exact boundary and method

Repository: `proteinfoldingengine/WetLabEngine`. Subtree: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/`.

- Analytical baseline: `a287ed73db909eaf254ceece2d3d0cbb736b105e`.
- Accepted frozen mathematical candidate: `974d0356b78c294804c3db49686e1e0f32dcd90a`.
- Reviewed reporting candidate: `b535eb93ce38f56d6e6f6149102e7b61ef0bf453`.

I fetched all eight exact reporting files through read-only GitHub connector operations. I compared complete old/new reporting texts and parsed STATUS metadata with the analytical baseline, inspected the complete GitHub compare file lists from both baseline and mathematical candidate, checked the proof/scope hashes, and compared the published whole review both to the full original local text and to its Git blob hash. These are document/provenance checks, not scientific tests or enumeration. I performed no GitHub mutation, workflow, scientific execution or implementation change.

## Required correction

The new X35 sections in `KNOWN_RESULTS.md`, `NEXT_OBLIGATION.md` and `A11_PROGRESS.md` each contain:

> X35 derives weaker availability than X34's GLOBAL count.

The accepted theorem proves availability under weaker sufficient conditions, giving a stronger availability interface. The present sentence says that the availability itself is weaker, reversing the direction of the accepted advance. Replace all three occurrences with:

> X35 derives availability under weaker sufficient conditions than X34's GLOBAL count.

This is a reporting wording issue. It does not require changing the mathematical proof, scope, whole review, closeout, STATUS metadata or prior reports. No other change is required by this review. A final acceptance must refer to a separately frozen amended reporting candidate.

## Exact reviewed blobs

| File | Git blob at the reporting candidate |
|---|---|
| `A11_X35_SCOPE.md` | `4f4a6520391de7b6cc56901919b12037aeb33bf2` |
| `A11_X35_COMPONENT_WITNESS_RENEWAL.md` | `d180465540c1fcc4abb282cfc386933f9515caf6` |
| `INDEPENDENT_A11_X35_WHOLE_REVIEW.md` | `f8fb1f11d98e4ed5744cbcd0cb3e415faf04108a` |
| `A11_X35_CLOSEOUT.md` | `01037b363cdf99b55889d20ab817a446d8b18103` |
| `STATUS.json` | `c3409182b59c63b245070bbf54c5394f00ff87e0` |
| `KNOWN_RESULTS.md` | `65257508a55c614c7872b1e9d8bbac1de3d0f38d` |
| `NEXT_OBLIGATION.md` | `7b28f66fafa2f9586eacd995ef7fca41869ac71f` |
| `A11_PROGRESS.md` | `9b452afc1f4e64d1a6a4ccf50994609d30003e19` |

The proof and scope are unchanged from their accepted frozen identities. The proof's historical candidate header is retained, with its acceptance supplied by the subsequent attributable whole review and closeout. The published whole review is exactly equal to the original local review text, and its blob exactly equals the original file's Git blob hash. Its attribution, full verdict, mathematical reasoning, dependency anchors and qualifications are unchanged.

## Other reporting claims are consistent

The closeout and new X35 summaries correctly describe actual root-index interaction components, common-index protection during changing unions, exact local count below one, deterministic conditional averaging, eligible next-root choice, and complete labelled/noncompact restoration on the original positive-floor carrier. They account for shared roots and explicitly avoid treating each component as a standalone three-guard. They correctly say that no global count below one is required.

The infinite even-m control is reported with original floors m-1/m, exact-four endpoints, distinct events, global count m/6 and local weight 1/3. Background and full endpoint union have tau2. The critical combined tau3 state, neither side independently protecting with background in both, literal primitive continuation, and complete repeated assignment sorting agree with the accepted proof.

Novelty is otherwise stated accurately as a stronger DERIVED sufficient test and renewable handover interface. The control is expressly already symmetry-connected by accepted permitted-root-permutation M; the packet does not claim a new connectivity classification outside every older result.

Band conversion is conditioned on a complete lower path with exact-four outer ends. The prose and `a11_x35_band_conversion` metadata preserve the qualification that A guarantees outer endpoints while it need not preserve inexact internal waypoints, schedule or length. Separate conversion of completed exact-four adjacent segments is correctly allowed.

The prose explicitly preserves one-active-root limitations, sufficient-not-necessary count status, and the distinction between failure of a count, failure of whole-root ordering and native disconnection. Unrestricted mixed-floor, directed, higher-target and nested questions remain open; genuinely interleaved/repeated handovers remain a next obligation. No new numerical scope, execution, scientific certification, implementation, benchmark, integration merge or physical claim is asserted.

## Full old text and metadata preservation

`KNOWN_RESULTS.md` and `A11_PROGRESS.md` retain their entire baseline text as an exactly unchanged prefix. Removing the single inserted X35 section from `NEXT_OBLIGATION.md` reconstructs its complete baseline text exactly. The insertion sits before the retained X34 section; no historical section is removed or rewritten.

All 427 pre-existing `a11_*` metadata fields and all 18 pre-existing `v16_*` fields retain the same parsed values. This includes the nested bounded v16.55 certificate, evidence, execution and historical records, and the certified v16.54 fields. The accepted-candidate list retains its complete old prefix and appends only `974d0356b78c294804c3db49686e1e0f32dcd90a`.

The existing `scientific_sha` and `workflow_sha` remain `3183c29896ebb47c320fa46a67ca2dd0696702fc`; `baseline_sha`, existing `scope_sha`, last verified scientific event, run attempt, implementation status, engineering status/anchors/review and measured-speedup field are unchanged. `active_run_id` and `pending_execution` remain null. The historical pending-execution snapshot is unchanged. No new run is implied.

Current analytical phase/status, review gate, analytical source anchor, current blocker/next direction and mathematical summary update from accepted X34 to accepted X35, while the prior mathematical-summary text is retained as a prefix. The `analytical_scientific_sha` update to the accepted X35 mathematical candidate is an analytical anchor update, distinct from the unchanged scientific/workflow execution anchors. Newly appended `a11_x35_*` fields accurately record the accepted source, component condition, restoration, renewal, conversion qualifications, control and limits.

## Complete tree delta

The untruncated baseline-to-reporting GitHub comparison is ahead by three commits and lists exactly eight changed files: four report modifications (`STATUS.json`, `KNOWN_RESULTS.md`, `NEXT_OBLIGATION.md`, `A11_PROGRESS.md`) and four additions (`A11_X35_SCOPE.md`, `A11_X35_COMPONENT_WITNESS_RENEWAL.md`, `INDEPENDENT_A11_X35_WHOLE_REVIEW.md`, `A11_X35_CLOSEOUT.md`). There are no other changed paths, deletions or renames. All changes are in the specified research subtree.

The mathematical-candidate-to-reporting comparison is ahead by one commit and lists only the four report modifications and the two whole-review/closeout additions. The proof and scope are consequently unchanged at the tree level as well as by their immutable blobs.

This confirms preservation of scientific code, workflows, original evidence, v16.55/v16.54 source/certificate trees, all older frozen sources and concurrent work by this reporting delta. It is not a fresh execution or re-audit of their unchanged scientific contents.

The sole required correction is the three occurrences of the reversed availability wording identified above. The accepted mathematical verdict remains intact. This exact reporting candidate is not accepted until that correction is frozen and independently checked.
