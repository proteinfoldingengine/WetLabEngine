# PR107 original review evidence

This directory preserves the original evidence for run **39449286888**, attempt **1**, workflow/checkout `9ead84faf9081fc5d22ba24159d2078cc0f73a21`.

The exact target is the clarification at `0eb63cf6c6a5ea74310ea45b689dc4458923342b`, prospectively frozen at `fe57d057aa42ca934d6b29721a7f07f237b9d876`. See [the scoped status receipt](../STATUS.md), especially its visible-review-coverage qualification.

- `original_zips/`: all three exact GitHub artifact ZIPs, checked against service byte counts and SHA256 digests.
- `integrity/`, `review/`, `publication/`: all 13 original extracted members, unchanged, including each artifact manifest.
- `logs/`: decoded GitHub job logs. GitHub masks credential values; no authentication credentials are archived.
- `service_artifacts.json`, `run.json`, `jobs.json`, `branch_runs.json`: public service metadata and identity/readback evidence.
- `MANIFEST.json`: byte counts, SHA256 and Git blob IDs for every archived payload file. The manifest does not include itself.
- `READBACK.json`: added only after the archive's full immutable bytes, author, parent and exact diff are independently read back.

The complete model response includes opaque fields unchanged. They are evidence of original bytes, not additional interpreted proof. The readable verdict is ACCEPTED, with three constructive confirmations and three limitations, and the separate publication audit is PASS. Native bridge status remains NOT_DERIVED.

No model request, numerical campaign, scientific reproduction or retry was performed to create this archive. The original Actions expiry is 2027-01-18; repository preservation is independent of that retention window.
