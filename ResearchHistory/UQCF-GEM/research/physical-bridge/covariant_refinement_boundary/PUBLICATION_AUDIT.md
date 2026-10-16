# Source and publication audit — covariant refinement boundary

**Stage 1: PASS (8/8). Stage 2: PASS (8/8). Blocking findings: 0.**

Audit target: scientific head `5f318b99d86fea2a9b1c09432705941a9edd188c`, tree `d2e16c6ded7f0ecc1356d98041ae146702be6469`. Parent `b20429c2e692d3ea219ab44404366cdfa3a5b119`. Commit range: 0243bcbb (preregistration), bce117d1 (note), 5f318b99 (review).

Stage 1: each of the 8 bound sources was fetched raw from the GitHub contents API at the parent SHA. Byte count, SHA-256 and recomputed git blob match source_identities.json; the blob equals the contents-API sha at the parent; the packet content is byte-identical.

Stage 2: the GitHub compare API (status ahead, ahead_by 3) shows the change boundary is exactly the six new files under covariant_refinement_boundary/ plus the continuation modification. For each changed file, the remote bytes at the head have a git blob equal to the compare entry and are byte-identical to the frozen local bytes.

Evidence: PUBLICATION_AUDIT_EVIDENCE.json. This audit verifies source binding and publication integrity only; it is not a scientific review, does not run any module, and confers no CLOSED/CERTIFIED status.
