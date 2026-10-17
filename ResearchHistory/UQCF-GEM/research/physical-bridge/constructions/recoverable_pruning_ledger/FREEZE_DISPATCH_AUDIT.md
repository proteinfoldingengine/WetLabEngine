# Recoverable-pruning-ledger freeze dispatch audit

Date: 2026-10-17  
Audited branch: `research/uqcf-overlapping-guard-exchange`  
Audited immutable head: `0fbea1c31d1c2c82b9073601ea3e79880c863aa6`  
Prior adverse-review commit: `1e2ac240af79a020810ebb149fe1ed10dcbabfd2`

## Decision

**HOLD DISPATCH.** The freeze is a materially improved, promising conditional
candidate, but it is not yet an independently reviewed result and it is not a
native-event milestone.

This audit is a pre-dispatch process audit. It is not the required independent
whole-argument scientific review.

## Mathematical corrections now present

The freeze directly answers both recorded draft-6 objections:

1. Theorem 13.3(2) now unitalizes the selected generator space,
   `K_j^+ = span{1} + K_j`, so the generated algebra retains the inherited
   `A_j` summand even when `1` was absent from `K_j`.
2. Arbitrary one-step selections are no longer claimed to give multi-step
   monotonicity. Proposition 13.4 adds a hereditary-survivor condition, and the
   stated survivor selection is claimed to satisfy it.

These are the right forms of the repairs identified in
`DRAFT6_ADVERSE_REVIEW.md`. They remove the two specific counterexamples, but
the corrected whole argument still requires an independent reviewer verdict.

## Dispatch blockers

### D1. GitHub Action dependencies are not pinned

The workflow uses floating tags:

- `actions/checkout@v4`
- `actions/setup-python@v5`
- `actions/upload-artifact@v4`
- `actions/download-artifact@v4`

This violates the pinned-dependency requirement in
`ResearchHistory/UQCF-GEM/AGENTS.md`. A reviewer run made from the present
workflow cannot satisfy the frozen-verification contract.

### D2. No prospective GitHub execution exists

At this audit, the workflow has not run for this freeze. The declared workflow
only triggers on `grok/recoverable-pruning-ledger-freeze`; the audited freeze
is at the research-branch SHA above. Before dispatch, the dedicated review
branch must point to the exact frozen tree, and the run must record both the
workflow SHA and scientific SHA.

### D3. Local PASS evidence is not prospective campaign evidence

The preregistration and the committed local producer/checker outputs first
appear together in the same freeze commit. Those local outputs are useful
exploratory evidence and a reconstruction target, but they cannot by
themselves establish a prospectively frozen execution. The first qualifying
execution must occur after the freeze, reconstruct the declared universe from
the exact immutable SHA, exercise every rejecting control, and preserve raw
logs and hashes.

The large enumeration totals are bounded reconstruction coverage only; they
are not independent scientific significance.

### D4. Publication audit and immutable readback are absent

The workflow ends after ephemeral artifact upload. It does not provide the
required separate publication audit or immutable repository readback of:

- raw reviewer request and response;
- reviewer verdict and objection disposition;
- producer and checker logs, summaries, and exact universe hash;
- rejecting-control results;
- workflow/run identifiers and exact SHAs;
- published status language and remaining open obligations.

Ninety-day Actions artifacts are not a substitute for immutable published
evidence.

## Required gate sequence

1. Replace every floating action tag with a verified full commit SHA.
2. Freeze the corrected workflow and record its exact SHA.
3. Dispatch on a branch whose frozen scientific tree is exactly identified;
   do not mutate the frozen argument or preregistration during execution.
4. Require independent producer/checker reconstruction and all declared
   rejecting controls.
5. Obtain an independent Gemini whole-argument verdict over the frozen
   argument, adverse review, response, preregistration, and reconstructed
   evidence.
6. Preserve raw adverse evidence even if the verdict is negative or the API
   fails.
7. Publish raw execution and review evidence in a new immutable commit.
8. Run a separate publication audit and perform immutable readback of every
   cited object before any closure language.

## Scope that remains open

Even a successful conditional review would not derive the native bridge.
Witness D still depends on the stated product/action premise. Native
preparation/source identity, enactment and occurrence order, retention in a
physical carrier, receiver access/readout, and an error contract remain open.
Accordingly, broad C3, C4--C6, gravity, and physical origin remain open.

