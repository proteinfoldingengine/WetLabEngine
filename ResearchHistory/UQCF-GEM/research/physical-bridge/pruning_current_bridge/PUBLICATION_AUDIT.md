# Independent publication audit — pruning/current bridge

Verdict: **PASS** for the scientific publication commit identified below. Native milestone: **NOT ACHIEVED**.

Repository: `proteinfoldingengine/WetLabEngine`.
Scientific commit: `2aa29b2dd35e1e84e6e47574de73d9ce7cd9d2c2`.
Scientific tree: `cca68f37c4d24177714ac87798da490aad3fdec8`.
Sole parent: `83026efa321ad148a9ce42151e1006e134d6b4ad`.
Parent tree: `29acc9e4246ea4d35f5e5c5750b5b78ec5613289`.

This is a separate publication and provenance audit under the established self-contained GitHub scientific review workflow. It verifies publication bytes and review bindings; it is not a mathematical re-review, a physical milestone, a main merge audit, numbered-stage closure, or review of any later author receipt publication. No scientific source module was imported or executed. No author scientific file, GitHub resource, or automation was changed by this auditor. Local audit evidence creation used JSON decoding and byte/hash/tree checks only.

## Independent remote readbacks

All eleven source files were independently fetched at the immutable parent with `github_fetch_file`, retaining complete UTF-8 contents and raw tool responses. For each, exact bytes, byte count, SHA-256, recomputed Git blob identity and returned blob SHA match both source_packet.json and source_identities.json. Those independently read parent bytes were reused in this publication audit, rather than treating the author's embedded packet as remote evidence.

All seven publication files were independently fetched at the immutable scientific commit. Their complete UTF-8 bytes equal the frozen publication_bundle.json, and their byte counts, SHA-256, recomputed Git blob SHA-1, returned file SHA, and new-tree blob identities agree. The manifest binds all six payloads, including the full continuation index. Its declared self-exclusion is correct; the manifest itself is independently covered by this seven-file audit.

| Published path relative to physical-bridge/ | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| pruning_current_bridge/RESULT.md | 16820 | `f7f0b01b3032684d24380c9cbc447b1cc9fcdde3dfd2c909c0ad456008f068ee` | `9d5230adcea0290ca2e5e2a66cbe24899f132bc1` |
| pruning_current_bridge/INDEX_APPEND.md | 2501 | `e1738ece85a61210a757d58be5a9925473137eab99b5d54fa2089a73fed3ca6a` | `433be24c44c4b909c3e88d8f2cbde80f5193c676` |
| pruning_current_bridge/source_packet.json | 117682 | `3464c93861ed3f881bfb1c8632880abc717e8f0a87ddcf0da7acac6dd92f024d` | `ba0cb9701293c1fee0ae590599a0946e55e57efb` |
| pruning_current_bridge/source_identities.json | 3167 | `373ac1f6c944341e2a8846f0d426e7ee859c3a7f23adcd67ba9bc012f0e71efe` | `7bb13b290f617b13caa894dafea1fc6d86bcc7df` |
| pruning_current_bridge/ANALYTICAL_REVIEW_RAW.md | 15794 | `ddb2548a1b478a1fea0d64755a49c07fdce00e72289638dd02097e57dfaac414` | `35cac6d7967f2397fac40460affbcc77417570d4` |
| COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md | 55150 | `3d93b145481435d6e6b8e5c8a2aaf91c09dc277966f31f11641bc1a95f10c9df` | `241adc4f744cf5ebde84eefe1bc9625cca1d6ab4` |
| pruning_current_bridge/PUBLICATION_MANIFEST.json | 2736 | `8b3611bd672b7cbf7ab54a69b8f22ceb65e505eab085601a6f4010d270c66a2c` | `5ee9406767682cf076d61395704457c3a76501cd` |

## Parent, tree and complete delta

Git commit readback confirms the exact scientific SHA, tree and sole parent. Nonrecursive tree traversal compared the parent and publication roots, skipped identical subtree objects and read every differing subtree, including the newly added publication directory. All eleven root/intermediate/new-directory tree responses were nontruncated and their Git tree SHA-1 identities were independently reconstructed from their complete entries. This yields the entire changed path set: six additions and one modification, with no deletions, extra files, mode changes or changes in skipped equal subtrees.

- `ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` — modified
- `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_current_bridge/ANALYTICAL_REVIEW_RAW.md` — added
- `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_current_bridge/INDEX_APPEND.md` — added
- `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_current_bridge/PUBLICATION_MANIFEST.json` — added
- `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_current_bridge/RESULT.md` — added
- `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_current_bridge/source_identities.json` — added
- `ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_current_bridge/source_packet.json` — added

## Exact index preservation

The published continuation is exactly the independently fetched 52649-byte parent index followed by the unchanged 2501-byte INDEX_APPEND.md: 55150 bytes total. Prefix equality and complete concatenation equality both hold. Parent index SHA-256 is `3d12848c76bf031558fd0bf5ca8946c967313ca03d9de7ba9dc6af30f6ea4ed4`; append SHA-256 is `e1738ece85a61210a757d58be5a9925473137eab99b5d54fa2089a73fed3ca6a`; full published index SHA-256 is `3d93b145481435d6e6b8e5c8a2aaf91c09dc277966f31f11641bc1a95f10c9df`. Both base and append identities match the manifest's index_update contract.

## Review preservation and exact acceptance binding

The published raw analytical review has SHA-256 `ddb2548a1b478a1fea0d64755a49c07fdce00e72289638dd02097e57dfaac414`. Its initial 13078-byte CHANGES REQUIRED review prefix has SHA-256 `b6dfb0cb563b443342ade8f9c6bc6863462ee5af946ac3c5f4daaf649325280f`, matching the preserved-prefix identity recorded in the final review. The adverse finding remains visible and binds the original report hash `b54e3475a134dab59c013d0c5c5315b04283020c9e5d81cc374df5cb140982c0`.

The appended final targeted review explicitly accepts only the corrected report hash `f7f0b01b3032684d24380c9cbc447b1cc9fcdde3dfd2c909c0ad456008f068ee` and the unchanged append hash, and repeats the unchanged source_packet.json and source_identities.json hashes. All four final bindings match the independently fetched publication files. Reversing only the required report phrase replacement reconstructs the original reviewed report hash, confirming the correction's exact scope. Analytical acceptance therefore does not erase or retroactively accept the adverse original report bytes.

## Disposition and preserved evidence

All ten provenance checks in PUBLICATION_AUDIT_EVIDENCE.json pass. The published manifest and final analytical review retain milestone NOT ACHIEVED. No physical acquisition, scientific execution, historical test-count increase, main merge or numbered-stage certification is established by this audit. The author may publish a separate receipt later; that action and its resulting commit are outside this audit.

Raw remote responses are preserved in audit_work/stage1_raw.json, audit_work/stage2_raw.json and audit_work/stage2_delta_raw.json. Independently fetched bytes are retained under audit_work/independent_parent_sources/ and audit_work/independent_publication_files/. The machine-readable checks, all eleven source identities, seven publication identities and complete tree delta are in PUBLICATION_AUDIT_EVIDENCE.json. The byte/hash/tree verification harness is audit_work/verify_publication.py.
