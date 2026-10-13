# Independent publication audit: completed-pruning saturation

Audited: 2026-10-13 UTC.

**Verdict: PASS_PUBLICATION_ONLY.** No publication discrepancy or remaining required-retrieval blocker was found. This verdict verifies the fixed publication and its preserved conditional analytical acceptance. The native-event milestone remains **OPEN / NOT ACHIEVED**.

## Immutable target and independent retrieval

Repository: `proteinfoldingengine/WetLabEngine`. Branch context: `research/uqcf-overlapping-guard-exchange`.

| Object | Immutable identity |
| --- | --- |
| Publication commit | `cbeb3c7f4ab59e4c2b30a90a063d2cee3472a099` |
| Publication tree | `969ae0d24fd1f96ea91daa6f2376badb1b8ec86e` |
| Sole parent | `3b3b1e2d97c0381a05625fff8851cc813e8e2a24` |
| Parent source tree | `879d72682033b776b9fe20ae67baa2ace2d435c2` |

I freshly retrieved the commit endpoint, both immutable Git commit records, all nine publication files at the publication SHA, and all ten source records at the parent SHA using the GitHub connector. The author-local packet and prior author readbacks were comparison objects, not retrieval authority.

The commit file list reports exactly nine changed paths: eight additions under `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_saturation/` and one modified continuation index. A separate tree comparison corroborated the entire changed-path set. Two optional recursive-tree reads returned `Transport closed`; I replaced them with eleven untruncated nonrecursive tree reads, descending through every differing subtree and confirming identical sibling objects. Each tree response was serialized as a Git tree object and independently hashed to its reported tree ID. No other changed file, deletion, rename, or mode change was found. No required retrieval remains blocked.

## Exact publication bytes

Every UTF-8 readback was hashed as raw encoded bytes. Recomputed Git blob IDs match the file connector, commit file list, and corresponding tree entries. Every manifest-listed SHA256 and byte length matches the fresh remote bytes. The manifest deliberately excludes itself; its independently computed identity is recorded below and agrees with the immutable tree.

The first eight rows are in `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_saturation/`. The last row is the continuation index in its parent directory.

| File | Bytes | SHA256 | Git blob ID |
| --- | ---: | --- | --- |
| `RESULT.md` | 17456 | `6dd8af20413df9f7a00406bc16af4867169ff2efd57b0f5d4a2edad7ef8bed25` | `fd5a8d17871466da323e8fa28318252906e5e403` |
| `INDEX_APPEND.md` | 2037 | `1841e7409a16148464e81759959de4aa261e20b223773f78584ab8312ed56c1d` | `0d987b99129200af9b7df1e5ab8759a30efccc81` |
| `source_packet.json` | 112559 | `b4b2573697dc1c7318dd8dfba3163556e9ed627bc6de9b5ee7e78dae19fdfdb4` | `063c542004688409c086463e254b19e0a5a4ea9a` |
| `SOURCE_READBACKS.json` | 2983 | `d93ca4d2d5d2db21a1cfdacc3c20eb6e749a1beb8662a1f65596879ba37cc0a3` | `c8f351e19518e3453d5f4949ffdb6631b36fc532` |
| `ANALYTICAL_REVIEW.md` | 8678 | `c082ee243e2a96f2d250a0ebb3e456e9e5596ddf4900fbec37f451d20e4292f2` | `b4136a0f7f06b52627a99dc4ff8299a16bc2811c` |
| `ANALYTICAL_REREVIEW.md` | 4624 | `075f41672475500e03cacf39b6f06b4f4a91782b686e068db829233a42cbbf0a` | `1ecf7bbbf8e3ec92220bdde4dda6f72c1bb2bcdf` |
| `RECONCILIATION.md` | 2799 | `b78464f59172ef359e7d7786a38b1dcfbb8cc6ba49455b8d8dd456303c853549` | `24d009b91954a805fe21f53ad996e48e779e9360` |
| `PUBLICATION_MANIFEST.json` | 3435 | `f17b770ba3a93da48587f97f6fea75d1a986c4b6fdb09fc359033c096ec40703` | `a1e351944815ab3711eb9224b3fb0c275a59eed0` |
| `COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` | 39061 | `5f54bd3ff1496158c10f927e7bd023c16f753ee677b2adbd45f02b66e23a8619` | `21df254de68842f8f6018f93728885319a5ed344` |

The parent index is 37024 bytes, SHA256 `fe01d65a5ec2c272717a9fd1d899854c8ca767f2784fce0d0ae16736c7a141b2`, Git blob `0f2685578e9a822caeed7fda3bc21d2291fe7572`. The published index is byte-for-byte this independently retrieved parent followed by the independently retrieved 2037-byte `INDEX_APPEND.md`. Prior index content is intact.

## Source and review preservation

All nine `source_packet.json` file contents and its `index_parent` content equal the independently retrieved parent bytes exactly. Their ten Git blob IDs, SHA256 digests, and lengths match `SOURCE_READBACKS.json`. Packet and manifest parent/tree identities match the immutable commit metadata. The evidence JSON records every source path, exact identity, and comparison result, including `AGENTS.md`, the physical-frontier/gate/milestone records, v16.25, v16.26, v16.53, and the pruning-record and view-local source documents.

The initial analytical review remains at the assigned raw-review hash and retains **CHANGES_REQUESTED** against initial manuscript SHA256 `abadf8f6d094cfda2f658a242042336e9117a487564cdde08d56f4fcb70b5b50`. Its singleton non-cover counterexample and Important source-scope objection remain visible. It has not been retrospectively marked accepted.

The separate correction review states **ACCEPTED AS A CONDITIONAL ANALYTICAL RESULT** and binds the exact final manuscript hash, unchanged append hash, and preserved initial-review hash shown above. Its own bytes match the assigned correction-review hash. `RECONCILIATION.md` accurately describes this sequence and records all four bindings.

The source view-local classification explicitly assumes `|P| >= 2`. The corrected manuscript section 4 restores `|P|>=2` for that inherited classification and separately explains that an actual singleton cover is the whole tree, so its support state is unique, `S0=W`, and the hull interval is trivial. It expressly avoids a pointwise classification on non-cover singleton inputs. The reconciliation and re-review accurately reflect the correction; the index does not revive the rejected assertion.

## Claim boundary and provenance limits

The published theorem retains its conditional class: the same-carrier interval `[W,S0]`, exact initial profile `q=h(S0)`, nonnegative integer total budget `B`, and every budget-admitted native atomic interval deletion. Its terminal quantifier is over unextendible paths in that graph. The manuscript and index consistently state `D_q(endpoint)=min(B,D_q(W))`, allow differing terminal states/local allocations, and disclose the completion and envelope controls. They do not turn admissible paths or a computable profile into a derived native action, enforced band, actual continuation, or accessible receiver output.

The source milestone permits a common or probabilistic accessible consequence without selecting all microscopic details. The publication preserves that criterion and identifies the still-supplied action/access premises. It does not claim the milestone achieved, reopen stopped source-to-GR routes, or certify broad C3/C4-C6, a physical force, a fundamental clock, or archive-wide novelty. `AGENTS.md` governs numbered-stage closure; this audit establishes no numerical campaign, test-count increase, full foundational replay, main merge, or CLOSED/CERTIFIED status.

This audit used proof-first reading and mechanical UTF-8, JSON, length, SHA256, Git blob and Git tree checks only. I did not import scientific modules, execute scientific code or simulations, enumerate a scientific state universe, rerun tests or historical campaigns, edit author files, make commits, send external messages, or spawn agents. Repository writes beyond the fixed publication are not part of this verdict.

These are connector-provided remote text readbacks at immutable refs. GitHub reports the commits unsigned; hashes do not establish signed authorship or reviewer identity. The original draft bytes were not provided for independent reconstruction, so preservation of its rejected hash and objection is verified through the exact assigned review text. No claim of independent numerical reproduction or physical validation is made.

The accompanying `publication_audit_evidence.json` contains the immutable metadata, exact changed-file records, complete relevant tree readbacks and their recomputed identities, all nineteen file identity checks, accepted review bindings, retrieval limitations, and the publication-only disposition.
