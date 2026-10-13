# Independent publication audit

**Verdict: PASS_PUBLICATION_ONLY. No publication discrepancies or blockers found.**

This audit independently retrieved immutable remote publication and source bytes through the GitHub connector. It did not substitute the author’s local bundle or local readbacks for fresh retrievals. The audit used only text/JSON comparisons, UTF-8 byte lengths, SHA256 and Git blob SHA1 checks. It did not rerun mathematics or execute scientific code.

## Immutable publication and retrieval scope

- Repository: `proteinfoldingengine/WetLabEngine`.
- Declared branch: `research/uqcf-overlapping-guard-exchange`; this audit binds the immutable commit and makes no current branch-head claim.
- Publication commit: `5379f09f94cd176912a806685619ebab593c758a`.
- Publication tree: `8837cb4e41884528538a8abc02a83393a94d8d33`.
- Sole parent: `c96ff8b9ae0d3b3c07d4e56b51c28e4f256f3f5a`.
- Parent tree: `ac5f46694fcaeb427478e5b14e5203659478c5d7`.

The commit endpoint was independently read with `per_page=100&page=1`; its seven returned files are below the page capacity. This complete small changed-file list contains exactly six additions in `ResearchHistory/UQCF-GEM/research/physical-bridge/first_event_separation/` and the one modified parent continuation index. No unrelated path, deletion or rename appears. The parent metadata was fetched independently. All seven publication files and all eleven source records were then freshly fetched at their respective immutable commits using UTF-8 encoding. Retrieval provenance and exact changed paths are in the compact evidence JSON.

## Publication byte identity

All retrieved file blob IDs equal the locally computed Git blob SHA1 and the commit endpoint’s corresponding file blob ID. The six manifest payloads exactly match their declared byte lengths, SHA256 values and Git blob IDs. The self-excluded manifest was independently fetched and hashed as the seventh publication file.

| File | UTF-8 bytes | SHA256 | Git blob SHA1 |
| --- | ---: | --- | --- |
| COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md | 41614 | `de0f6f3e488ec96257448512a0e9f9006137f7ee37bd604113e51e3a79f564b0` | `20933b0db1fd8417d644f5644b3b248811cbedeb` |
| ANALYTICAL_REVIEW.md | 10411 | `a950af927be723c82e6582b40487d5d49db4d18b22e1acb39394a5b73f2a1f68` | `57e7178eb53b9278492cff02670b4bc7897f5233` |
| INDEX_APPEND.md | 2553 | `a325412a711d078dc5c14d08a22425f3d770d16d951b824bfa2665a15e77dfce` | `21e0148757704b366a9350a029ebd4ca5c2f1abf` |
| PUBLICATION_MANIFEST.json | 2750 | `9f31a2ce4f87dcee8d25c5beabedef19642a93dfd434fd0ab2db6c3661a087f3` | `9913aee9c823a495f84efc5f185fcf8bcd3ef9d0` |
| RESULT.md | 20160 | `599ce7940eda4994c82b99ba4b68a8187f301012a430836f4a1c66874918b780` | `6f8defb85c5768f9b06a45dc237db04b3151dd47` |
| SOURCE_READBACKS.json | 3318 | `13c14aef9fe59977891dc5f320f1d6e4238fe0484822720c7128795baa2032aa` | `438dbfb8f3a129deb098a731615ee4d3051d68cd` |
| source_packet.json | 130606 | `d20755e2a6cc3a25caab4bcf2778da16067ec7cf180b2089bc53d1ab6f9e4678` | `e5119a347371175a2faa3d46b933a5123f1573b0` |

The source packet’s ten `files` entries and separate `index_parent` are exactly eleven distinct source records. Fresh remote text and blob IDs match every packet record. Each record also matches its SOURCE_READBACKS length, SHA256 and Git blob identity. Packet, readback and manifest parent/tree provenance agree with independently retrieved parent metadata. The parent continuation index additionally matches the manifest’s separate parent-index record.

The published continuation index is byte-for-byte the immutable parent index followed by INDEX_APPEND.md, with no other alteration: 39061 + 2553 = 41614 UTF-8 bytes. Its updated hash agrees with the manifest and the analytical review.

## Review binding and claim boundaries

The raw ANALYTICAL_REVIEW.md SHA256 is `a950af927be723c82e6582b40487d5d49db4d18b22e1acb39394a5b73f2a1f68`. Its acceptance binds the final RESULT.md SHA256 `599ce7940eda4994c82b99ba4b68a8187f301012a430836f4a1c66874918b780` and INDEX_APPEND.md SHA256 `a325412a711d078dc5c14d08a22425f3d770d16d951b824bfa2665a15e77dfce`, as well as the parent and updated index bytes. These exact accepted bytes are the published bytes. The review explicitly records the decoder addition, identifies the preliminary hashes as an earlier draft rather than a rejected result, and limits its verdict to the revised hashes. It discloses and corrects the reviewer’s preliminary `files[-1]` versus separate `index_parent` packet-key mistake; the fresh source check independently uses the correct separate entry.

Textual inspection of RESULT.md, the append, the raw review and relevant source scope records agrees with the declared conditional claim: for each m>=2 the preparations have matched initial internal records and the same K, differing only in global-leaf incidences of one indexed view. Every proper output satisfying the inherited universal independent-view positive-extension bounds separates R=1[h_p>1]. The equality R=1[Ch_K(p) not subset of Z_a] is explicitly limited to this family. First native atomic deficits are zero versus one; completion, maximal availability of commands and a selected deletion site are not premises.

The limitations remain explicit. Native complete-own-view/current-K availability, physical applicability of the safety contract, proper occurrence and receiver access are unearned. The carrier-safe global-leaf deletion outside that information contract gives source one a zero response; a second step or larger contraction can break the unit band. Identity remains possible. No physical force, native-event milestone achievement, C3 sensor implementation, main merge, numbered-stage CLOSED/CERTIFIED status, numerical campaign or historical test count is asserted. AGENTS.md governs numbered retained-research stages; this publication explicitly claims a conditional analytical result and does not represent that closure chain as performed.

## Limits and evidence

This is a publication-identity and textual claim-scope verdict. Mathematical validity remains the responsibility of the separately preserved independent analytical review. No scientific module, numerical fixture, simulation, state enumeration, historical replay or GitHub Actions campaign was run. No author artifact was edited, no commit or external message was made, and no further agent was spawned. This scope does not certify current branch state, signatures, the whole repository or a recursively enumerated tree. No concrete discrepancy required broadening the audit.

The companion publication_audit_evidence.json records immutable IDs, retrieval provenance, exact changed paths, per-file lengths/hashes/blob IDs, comparison results, verdict and limits without duplicating file contents or unrelated tree inventories. All 111 mechanical comparisons passed. Its SHA256 is `6f6d6c47f7cc509fe645ea4e72ccfc1bd0c785e20f24440d998ee1de61d2fd3e`.
