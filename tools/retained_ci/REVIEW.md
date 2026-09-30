# Independent source review and resolution

Reviewed implementation:17f5140de78a04d38b7a6042c2213a150fb4fcfb.
Independent reviewer:retained_ci_review. No numerical execution locally.

Two important integrity findings accepted:
1. The checkout's historical manifests/reference outputs needed anchoring to the immutable verified parent. Preflight now compares the source manifest and all three scientific reference files against git objects at e789ce42bac28e084a4f0264180b738534d69923. A real temporary-Git regression test rejects a coordinated committed reference change.
2. An execution receipt must not claim an actual merge merely because checkout equals run head. Receipt validation now requires target push/workflow identity, merged PR identity, exact expected merge parents and equality with the PR publication tree. Direct pushes and wrong workflow/PR/parents/tree are rejected by controls. Receipt execution is wired after successful actual-merge replay and commits to a separate audit branch.

The reviewer confirmed process-local producer-only deep-copy reuse, original independent verifier calls, exact fixture/test comparisons and fail-closed subprocess behavior. Baseline timing is isolated while optimized timing competes with science; that limitation is preserved. No general speedup guarantee is claimed.

Reviewer declined runtime, performance, artifact/API, PR head, or remote source judgments. Root must resolve those using GitHub execution and independently downloaded artifacts before merge/closure. Historical science files and test bodies are unchanged. Additional safeguard controls were added after review; only the original three infrastructure regressions are claimed as witnessed RED-to-GREEN.
