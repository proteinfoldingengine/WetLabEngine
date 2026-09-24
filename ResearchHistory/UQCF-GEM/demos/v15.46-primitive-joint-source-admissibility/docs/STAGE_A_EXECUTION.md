# v15.46 Stage A — evidence preflight execution record

Date: 2026-09-23 (America/Los_Angeles).
Predecessor: `80f6ec8b8b2de882232c061a5c9d1f4aac6d86d1`.
This is a bounded implementation of the evidence/submission part of Stage A in the existing v15.46 design, not completion of its source-admission gate or a new physical result.

## Work performed

The previous inventory was an authored ten-source review. The new `evidence_preflight.py` checks the inventory's exact original Git blob (`fadf983aee8aae196d2e8a960673901d03c994f3`), reads each named source file, and checks its actual bytes against its recorded Git blob. It does not import or execute those source files. Duplicate JSON keys, duplicate sources, malformed pins, path traversal, symlink sources, missing files and altered bytes fail closed.

The separate `SOURCE_INTERFACE_SUBMISSIONS.json` records the witness packets actually submitted to this continuation. Its list is currently empty: no complete native source-interface witness has been supplied by this work. This is NOT an assertion that no joint state or useful record exists anywhere in the repository. The inventory explicitly acknowledges mathematical joint states.

A proposed packet identifies evidence for seven components: joint state, overlap inclusions, logarithmic support domain, occurrence link, coupling law, declared linearity and provenance derivation. A packet with every file present still receives only `EVIDENCE_ATTACHED_SEMANTIC_VALIDATION_REQUIRED`. File hashes and a `native_claim` label cannot certify that the files contain a valid state, native derivation or lawful coupling. State-domain and incidence semantics belong to the later stages and are not implemented by this preflight.

Missing input is not converted into a zero source. No source value, operator logarithm, curvature, coupling choice or physical correspondence is evaluated. Authored inventory conclusions are serialized under `reviewed_claims`, separate from computed byte checks and submission counts. The preflight cannot emit a native-source success outcome.

## TDD and local evidence

Twenty tests were written first. The initial run had exactly 20 assertion failures because the Stage-A implementation was absent. After implementation, all 20 passed under CPython 3.13.5 using actual temporary files. Tests include a fully populated but self-declared native packet which must remain uncertified, and supplied/diagnostic packets which must retain their distinct provenance categories.

The original `exploratory/proof_checks.py` was restored from the attached research package and its Git blob verified as `77df665e59e01c8d1085c6a5a0ed0079d8d50f53`. Its 195-check result was rerun locally and matched the original compressed output byte-for-byte (SHA256 `f686af1a062a92ff64c0de115ae522da17272bf4ec1c182c367e6ea8d3d9fe11`). Compilation passed. The uploaded new implementation and tests have the same Git blobs as the locally executed bytes:

- implementation: `4d2bd6b72d4a170888c60ef71c80c1e55a27465d`
- tests: `afb63044d54f3471ffb0fb67facb6b48fa82969e`

The container cannot clone GitHub in this session. Therefore the local twenty-test fixture run is NOT represented as a full-repository ten-source pin audit. The narrow GitHub workflow performs that actual checkout audit, the full current 28-test v15.46 preflight/exploratory set, both prior proof-output replays, and a canonical Stage-A output replay. Its run/head/conclusion are recorded in PR #57 after execution; this source snapshot does not claim a CI result before one exists.

## Scope and preservation

Only additive v15.46 files and one read-only, branch/path-limited workflow are introduced. The original source screen, eight typing-probe tests, inventory and written design are unchanged. The workflow checks that v15.44 and v15.45 retain their certified directory tree hashes and that the prior v15.46 exploratory directory is unchanged. No older development workflow is broadened or imported into main.

This is author implementation/self-review, not independent peer review, new full-v15.46 certification or a full-repository regression. It is not a prospective holdout experiment. The original conditional mathematical obstructions remain at their stated scopes; the preflight does not strengthen them.

## Next scientific dependency

Supply or derive a specific record with the joint-state/overlap data, oriented occurrence relationship and independently justified coupling evidence. A packet of labels is not that derivation. The next semantic validator must inspect the actual state, inclusions, support and coupling equations rather than turn this inventory into a fabricated source. Until then, report the first unmet input stage and keep geometry-facing execution stopped.

Source correspondence: `NOT_EVALUATED`. Physical source law adopted: false. Pillar 3: OPEN.
