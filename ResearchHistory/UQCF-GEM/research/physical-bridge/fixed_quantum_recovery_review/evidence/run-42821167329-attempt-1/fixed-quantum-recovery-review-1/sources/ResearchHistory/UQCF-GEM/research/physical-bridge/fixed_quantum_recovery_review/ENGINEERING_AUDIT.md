# Review pipeline engineering audit

Scientific freeze: 02f6504bb4fe026557fbcef97fb12cc0775c82d9.

Independent Fraction and SymPy implementations were written without executing mathematics before the scientific freeze. After immutable full freeze readback, both local runs exited zero and yielded equal complete semantic JSON. This is a supporting author-side check, not Gemini acceptance. GitHub will run both from the committed implementation and run the unchanged inherited stack.

A separate read-only engineering audit identified four weaknesses before dispatch: latest-attempt-only generation history, incomplete request reconstruction, missing partial response-read failures, and unsupported archival retry after a prior archive commit. The implemented corrections are all-attempt paginated generation history, full deterministic request bytes/configuration and model metadata checking, preservation of HTTP bodies and available partial-read bytes without retries, and explicit attempt-one-only jobs. Any later repair must use a separate non-generating publication process. No automatic retry is authorized.

Thirteen local protocol tests pass. Genuine failing-before-fix logs are preserved for HTTP failure-body handling, all-attempt generation history, and partial response-read handling. Tests also cover mutated artifact membership/bytes/lengths/hashes, source provenance, identity mismatches, contradictory verdicts, empty reconstruction, preserved adverse verdicts and native labels, thought text exclusion, and exact request/config/model metadata mutations.

No request headers, credentials, credential-bearing URLs, or exception messages are archived by the transport wrapper. Successful raw responses and opaque fields remain unchanged. The inherited model helper/parser and inherited regression stack remain unchanged.
