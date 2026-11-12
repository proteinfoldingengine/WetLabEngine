# Historical evidence preservation and correction provenance

This is a provenance note, not part of the independent review prompt.

## Preserved baseline

Repository baseline d588114a9958d52def9bd446a8db50640e8a0058 remains the parent of the isolated correction branch. The original recoverable_pruning_ledger directory is not overwritten. The original review run 39070100916 returned its historical ACCEPTED verdict and explicitly claimed to verify Lemma 13.1. That record remains unchanged even though the current counterexample refutes the original lemma's whole-common-center span sentence. Historical acceptance is not acceptance of this correction.

Files beneath ResearchHistory/UQCF-GEM/research/physical-bridge/constructions/recoverable_pruning_ledger:

| File | Git blob | SHA-256 |
| --- | --- | --- |
| FROZEN_ARGUMENT.md | 1f474a82c5901ab28ba318f8c3cbe6eec710ef3f | adf0a35e6a4c0d27e7523a5d6a498abbc3284721d4a36a9aef64ab0f23d76da7 |
| CONSTRUCTION.md | 96eec4fb6c96ea197690c1380c105fc498ca1298 | 7cc86fbc9784d1660e660770109906fbb234581ca9340fd525c79c605af3937b |
| STATUS.md | 7bb1bcb864dc73d3b5b9dc041a8dfd8731e692db | 569b29fb735a8e87d9bfef7d7fd2e4a440e3ba8ea884535cb40e7a7f1f5f7cd5 |
| review_run_39070100916/response.json | 834537e9e3186a4e9a1cd9e4f702b89070e21290 | f653cf1569812c7f95086960f7afa894cea202f9b9edb6118f46d5e0a0673e7c |
| review_run_39070100916/verdict.json | c25fa4d1855dcf4afe63d36ce2d8b3d41dec768a | 36a574571b4ef8320aea4348f13e5eda5fc59803369d119ff5038bdaa67b79f5 |

The full original raw response is retained as opaque evidence. No hidden-thought decoding is performed. The new workflow checks original-directory immutability and preserves exact copies/hashes of the listed files in its integrity evidence; those review/status copies are excluded from its model prompt.

## Correction and coordination

- Exact challenge: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6756397701.
- Coordination: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6756458108.
- Grok's response notice: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6756470263; full T-408 is at thread commit 11a773d4be1ed0469b6c430a6240532a28c683f6. It sustains the counterexample and reports 19 posthoc symbolic cases. That response is peer inspection, not independent Gemini acceptance, and its cases are not rerun here.

Three later immutable source packets embed the same old frozen ledger blob: first_pruning_own_view_review/MEASUREMENT_FIRST_SOURCES.json, measurement_first_review/source_packet.json, and preparability_review/source_packet.json. They remain byte-for-byte unchanged. The bounded targeted inspection and its limits are recorded in DEPENDENCY_AUDIT.md. This note cross-links the correction without reissuing or blanket-invalidating their separate review scopes.

## Current submission

The corrected self-contained manuscript, audit and protocol were frozen at e7da2fc3ceaff336660848b9d964e5a283309f90. A later implementation commit must not be substituted for that scientific identity. The correction review covers the complete conditional argument, not retrospective certification of the old numerical campaign. Old PASS/zero counts remain historical bounded evidence; the current code-coverage limitations are stated rather than hidden.

Native bridge remains NOT_DERIVED. PR130/131 holds and all unrelated review scopes remain unchanged. No main merge or physical-status promotion is authorized by this provenance note.
