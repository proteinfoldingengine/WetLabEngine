# Artifact preservation through v15.20

This archive separates three evidence classes:

1. **Frozen source and historical reports:** pinned at `7b6459f18b0add90a2f88cf9b0a152e2aa5c7647`. The source snapshot contains the existing ResearchHistory/UQCF-GEM tree, including earlier v13/v14/v15 reports. No scientific file, threshold, outcome, or old publication-status statement is rewritten.
2. **Newly reproduced outputs:** the archive workflow runs the 310 selected v15.11-v15.20 research tests, regenerates the nine existing video/HTML demonstrations and numerical exports, and publishes a GitHub prerelease after every release-asset SHA-256 and size agrees with its build. Each per-version ZIP includes source, raw generated outputs, fresh logs, environment, and member hashes. Filenames explicitly say REPRODUCED. New logs do not replace historical RED/GREEN evidence.
3. **Original conversation bytes:** ORIGINAL_DELIVERY_MANIFEST.json identifies 35 mounted artifacts totaling 30,432,032 bytes. Ten original ZIPs contain 450 members, including historical evidence and raw outputs. A separate 21,762,650-byte original-deliverables bundle has been prepared and hash-verified locally. The connector has no local-file upload parameter for release assets, so that original-byte bundle has NOT been uploaded. See ORIGINAL_BUNDLE_RECEIPT.json. Do not call the original archive complete until the actual bundle is present on GitHub and its digest matches.

The original bundle is named `UQCF_GEM_v15_11_to_v15_20_ORIGINAL_DELIVERABLES.zip` and has SHA-256 `8366f1a2e73a9eb90ad5114c1fa28309c4cd01679c6e0c004cab879870a5a690`. It is delivered as a conversation attachment. Uploading that one intact ZIP as a release asset preserves all 35 original artifacts without changing any member bytes.

## Publication and safeguards

The workflow `.github/workflows/uqcf-v1520-artifact-preservation.yml` runs only on the dedicated artifact-preservation branch or explicit workflow dispatch. Its reproduction job has read-only contents permission. Its publication job has repository-scoped contents-write permission for release assets; it does not update any branch. It uses a unique tag per workflow attempt, never replaces an existing asset, and publishes only after successful hash checks. `main` is not merged or advanced.

All rendering uses the existing model and renderer source. No new image synthesis or physics is added. MP4 decoding is checked. HTML is an offline download, not a deployed site. Browser rendering and native iPad/Safari behavior are not re-certified by the archive job. The 310 research tests plus the archive tooling tests are selected checks, not a repository-wide scientific certification.

The eleven archive-tool tests check file/member integrity, deterministic packaging, symlink rejection, remote digest/size requirements, original-byte matching, failure logging, JSON output handling, API host restrictions and honest release notes. Local RED/GREEN evidence precedes publication; exact-head Actions status must be read from the actual run, never inferred from this README.

## Links

- Source collection: https://github.com/proteinfoldingengine/WetLabEngine/tree/research/v15.20-results-archive/ResearchHistory/UQCF-GEM/
- Releases: https://github.com/proteinfoldingengine/WetLabEngine/releases

A published receipt will identify the specific archive release and uploaded assets. Until then this file describes the intended workflow, not a claim that the workflow succeeded.
