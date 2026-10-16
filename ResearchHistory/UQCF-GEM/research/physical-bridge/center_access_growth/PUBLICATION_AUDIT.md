# Source and publication audit — center access growth

**Stage 1: PASS (9/9). Stage 2: PASS (7/7). Blocking findings: 0.**

Audit target: scientific head `e3e156d63c0fa505d36c4d2eba7e62fcac124784`, tree `dcf03090bdf8518192ec4fb1142c0c6bd66db875`. Parent `d63aea606eb9e73bab812aef2934f799f3bb281a`. The commit range contains exactly four commits: 5944d8f (preregistration), aa0b68e (note), 2b49c65 (review revision), e3e156d (review).

Stage 1: each of the nine source originals was fetched from raw.githubusercontent.com at the parent SHA. Byte count, SHA-256 and computed git blob all match source_identities.json, the blob matches the GitHub contents API at the parent, and the packet content is byte-identical.

Stage 2: the GitHub compare API change boundary is exactly six new files under center_access_growth/ plus the continuation modification. For every changed file, the remote bytes at the head have a git blob equal to the compare entry and are byte-identical to the author's commit. The review's bound SHA-256 hashes for RESULT, INDEX_APPEND, PREREGISTRATION and both packet files equal the published bytes (match). The continuation is exactly the 80,735-byte parent followed by the 1,350-byte append, 82,085 bytes in total.

Limitation (disclosed): this audit was executed by the same agent session as the author and reviewer, using independent retrieval paths (raw by SHA, contents API, compare API). It is not organisational independence. No scientific module, simulation or inherited stack was run. It confers no scientific endorsement and no numbered-stage status. Evidence: PUBLICATION_AUDIT_EVIDENCE.json.
