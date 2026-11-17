# PR147 review-plumbing check

Disposition: **No pre-execution blocker found in the narrow adaptation.** This was an independent static review of the controller, existing rejecting tests, workflow, embedded source packet and reused helpers. No API/model call, scientific program, simulation, or reviewed controller was executed. Hashing and AST parsing below inspected file bytes only. Root remains responsible for running the eight existing rejecting controls and completing the post-response manual gates.

## Scope and verified identities

- The controller differs from the prior quiet-reference-robustness controller only in the review path, packet digest, ordered document IDs, adversarial review prompt and success-message label. All **11 function ASTs** are unchanged after normalizing that label.
- The test file changes only its import target and source-packet path. No existing rejecting check was removed or weakened.
- Source packet SHA-256 is `fe010792b8745124075129802589c5314fbff7d862414a83423a06dca5b1298a`. Its eight embedded document byte counts, SHA-256 values and Git blob hashes match their content. The embedded argument also matches the local frozen argument file.
- The new argument is pinned at `6de0e2c51a7c332adffa2144ee5e7af6baced784`, blob `b2f47d735e30c7ee8ffd5fc1bf859269626fd4d3`. The seven native/benchmark/directive documents are all pinned at `2ab565c3f5bf10305a96ddeef30901de49959ba5`.
- Both helper files are byte-identical to their previously reviewed copies and their locks: `uqcf_preparability_integrity.py` blob `50b1043cda14b18b962f7930cf6a4391067a2a96`; `uqcf_preparability_review.py` blob `4c8029da503ed57f404e4424ecc243eb3c609347`. Their source refs are the same research parent. No remote identity was newly fetched during this static check; the workflow must check all **10** remote source/helper identities.

## Workflow and model boundaries

The push trigger requires branch `gpt/charge-selection-20261113` and a change to `.github/workflows/uqcf-charge-selection-review.yml`. The actions are pinned by commit; permissions are contents/read and actions/read; checkout uses the triggering commit with persisted credentials disabled. There is no research-branch mutation or repository-write command.

Generation is confined to the `review` job at run attempt 1, with a second in-code first-attempt check. The checked-out SHA must match GITHUB_SHA. Reused transport first GETs the exact `gemini-3.1-pro-preview` model endpoint, then performs one generateContent POST with the locked prompt, temperature 0, maxOutputTokens 32768, and JSON response format. There is no retry or fallback. The helper's old prompt/main routine is not used: the new controller passes its own exact prompt to `call_model`.

The independent publication job performs no model call. It re-reads immutable sources, verifies the artifact member set and hashes, reconstructs the exact prompt/request, parses the raw response, compares saved review/verdict bytes, and requires an accepted verdict with `native_bridge_status=NOT_DERIVED`. The receipt records an analytical proof review, not native simulation or inherited-stack recertification.

The new prompt covers arbitrary coherent/rank-deficient bath states, global rather than support-restricted blocks, the all-input effect law, exact-channel controls, equal-charge blankness and empty-class boundary, rank-condition insufficiency, native source types, and the limited comparison with the earlier balance attempt. It keeps explicit new premises separate from a native derivation.

Credentials are passed only to their intended request headers and are not included in stored request bodies, manifests or printed errors. Raw response and model metadata are deliberately preserved as review evidence. No new secret-output path was introduced.

## Required manual post-response gates

These known inherited limitations are unchanged and are not silently waived:

1. Inspect the full raw reasoning. Require a nonempty, substantive `proof_checks` array and a meaningful `next_native_obligation`; the inherited parser does not enforce those fields.
2. Check `manifest.status=ACCEPTED` and agreement between its returned-model field, raw response modelVersion, exact requested-model metadata and publication receipt. The parser accepts the requested model name or a version suffix; confirm the actual returned value explicitly.

The controller is an integrity mechanism, not a mathematical certificate. A successful run alone does not certify the argument, the native bridge, or scientific completion.
