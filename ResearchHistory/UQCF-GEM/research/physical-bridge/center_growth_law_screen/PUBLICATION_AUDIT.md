# Source and publication audit — center growth law screen

**Stage 1: PASS (16/16). Stage 2: PASS (7/7). Blocking findings: 0.**

Audit target: scientific head `8667d59b5b067be3d8936794e3d3e167ecf374f7`, tree `3d6c79fa0f816f562a0286d49d13e7ace8d30c65`. Parent `560731329e33ee2ed85b4c38103c3b16ce15353f`. Commit range: 6b311946 (preregistration), 1fbf14fb (note), 8667d59b (review).

Stage 1: each of the 16 source originals was fetched from raw.githubusercontent.com at the parent SHA. Byte count, SHA-256 and computed git blob all match source_identities.json, the blob matches the GitHub contents API at the parent, and the packet content is byte-identical.

Stage 2: the GitHub compare API change boundary is exactly the new files under center_growth_law_screen/ plus the continuation modification. For every changed file, the remote bytes at the head have a git blob equal to the compare entry and are byte-identical to the author's commit. The review's bound SHA-256 hashes for RESULT, INDEX_APPEND, PREREGISTRATION and both packet files equal the published bytes (match). The continuation is exactly the 82085-byte parent followed by the 1652-byte append, 83737 bytes in total.

Limitation (disclosed): this audit was executed by the same agent session as the author and reviewer, using independent retrieval paths (raw by SHA, contents API, compare API). It is not organisational independence. No scientific module, simulation or inherited stack was run. It confers no scientific endorsement and no numbered-stage status. Evidence: PUBLICATION_AUDIT_EVIDENCE.json.
