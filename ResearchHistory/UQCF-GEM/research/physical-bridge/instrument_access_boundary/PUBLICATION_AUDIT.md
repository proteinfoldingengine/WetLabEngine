# Independent publication and provenance audit

**Verdict: ACCEPTED_PUBLICATION_PROVENANCE.** All 66 identity and placement checks passed; no discrepancies or read failures were observed.

Auditor: Codex agent `/root/instrument_access_publication_audit`, separate from the scientific author and analytical reviewer. Date: 2026-10-14 UTC. This is an agent-authored audit, not a human review or signer-authentication claim.

Repository: `proteinfoldingengine/WetLabEngine`. Branch observed at readback: `research/uqcf-overlapping-guard-exchange`.

| Binding | Independently observed value |
|---|---|
| Scientific commit | `2e6ccdf23832342be02bd7e2b4dad440fc2ec6df` |
| Scientific tree | `28d6794ec51242a7421d028f39c7e0319a6b43e9` |
| Sole parent | `b498bb1e4e610cfc68c0b630db75498029c002fe` |
| Parent tree | `fb6a3ed2dc89493327fa1220b37934af1a56f743` |

The audit independently fetched seven published files at the scientific commit and six original source files at the parent through GitHub. Base64-decoded bytes were checked with SHA-256 and Git blob SHA-1 (`blob <byte-length>\0` plus the bytes). All seven match the exact publication bundle; all six bound payloads match the self-excluded manifest. Each retrieved blob identity also matches GitHub's returned blob SHA. The manifest itself matches the bundle identity.

The source packet contains the exact bytes of all six independently fetched originals. Their paths, immutable-parent URLs, byte lengths, SHA-256 values and Git blob identities match `source_identities.json`. Both source objects and the manifest declare the verified parent/tree.

The continuation is exactly the 45,992 parent bytes followed by the 2,254 bytes of `INDEX_APPEND.md`, totaling 48,246 bytes. GitHub's parent-to-publication comparison reports exactly six new files under `instrument_access_boundary/` and the continuation modified, with no other changed paths. The comparison is one commit forward; commit metadata confirms the sole parent and tree. No unrelated repository tree was reconstructed.

| Review binding | SHA-256 |
|---|---|
| Initial report, bound by original review | `4e477d218cc217940e9430a645d74ff57ac4ece2ba5c26da31f57036f72cbfe9` |
| Final published report, bound by addendum | `fa665b14f19204a8615a4cd6ddc7655ff91d64687ee339116d5a6cb6293721f7` |
| Unchanged index append | `b29520172b653935a3389e53008563ca25b2523355bd5bb974ce741d382d35f5` |
| Original 9,302-byte review prefix | `517db7b73c5342c0b91d0ae18aaaf7cf5f4d5feee6bb652c3b8f5a1b419f61b2` |
| Full published review with addendum | `0fc8ad841ed305fb26e2846361e53ca239d2de86277acd3ff14c8147454b6be6` |

The original review survives verbatim as the verified 9,302-byte prefix. The final acceptance addendum explicitly binds the actual final report and unchanged index append. Removing only its identified clarification paragraph from the final report restores the initial accepted report hash. These are byte/provenance checks, not a new mathematical assessment.

All 17 GitHub reads succeeded without a retry or truncation. Raw commit, comparison and branch findings, file-response metadata, computed identities, individual checks and the complete final addendum are preserved in `PUBLICATION_AUDIT_EVIDENCE.json` (SHA-256 `4078fffffdc60ca6ea17801c33e4395aa86902de032d6ab075bd1312fb192e77`). GitHub reports the commits unsigned; acceptance concerns content provenance, not authenticated authorship.

Scope: conditional analysis only. No scientific module was imported or run, and no numerical evidence, native physical milestone, numbered-stage closure, main-branch certification or merge is certified. The published `NOT_ACHIEVED` milestone disclosure is retained. This audit does not certify its own later publication, the author's receipt, or terminal receipt readback; those are subsequent author steps.

Signed in text: `/root/instrument_access_publication_audit` — 2026-10-14 UTC.
