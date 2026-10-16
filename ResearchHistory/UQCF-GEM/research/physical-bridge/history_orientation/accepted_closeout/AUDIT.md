# Independent accepted-checkpoint publication audit

**EVIDENCE_INTEGRITY_PASS_WITH_RECEIPT_QUALIFICATIONS.** Scientific disposition: **ACCEPTED_CONDITIONAL_ANALYTICAL_SCREEN**. The audit verifies the retained Gemini acceptance of the frozen argument and the later durable publication. It does not constitute another mathematical review or scientific execution.

Fresh GitHub retrieval bound all 14 files added by `7d1f528dbd807ed39bb41bb36a221b084d5f9f52` to their git blobs and verified its parent `07bccacc3f17f97e3cd9cc9fe486a47cb04c9faa`. The publication author and committer are proteinfolding-grokbot; the exact reviewed source remains GPT-authored `a42ca9e248c438081f31dcaba2ba5c6ffb36cec0`. Run `38927950314`, attempt `3`, completed successfully with integrity job `117160704838`, review job `117160867575`, and publication job `117161256836`.

## Verified evidence

| Original Actions artifact | ID | Bytes | SHA-256 |
| --- | --- | --- | --- |
| history-integrity-3.zip | 12069514455 | 128796 | fb9e3e2b5c4dbe09122bd42d4b686809113f4e94d8835229e48827cd26d9dcfb |
| history-review-3.zip | 12070469282 | 110662 | b0d138ba85391fa6b570aa2e7a4554a06faf625dfa5208b815ce414485180308 |
| history-publication-3.zip | 12070158866 | 4283 | 34f503584d128e255e552521f3181ac3f89a95bbaa976c8fda5cd9f9babd64d6 |

All three archives were downloaded afresh from Actions and match the committed original ZIPs byte for byte, their independently fetched artifact sizes and SHA-256 digests, and the published git blobs. All members and file manifests pass exact membership, duplicate/path traversal/symlink, byte-length and hash checks. Published run, jobs and artifact JSON match fresh API responses. The attempt-specific API and current-run API have distinct creation fields; both are retained.

The 13 frozen inputs plus their manifest and all 19 original source paths were fetched afresh at their declared immutable commits (33 paths total). Source packet content, source identities, input manifest, integrity snapshot and source ancestry match exactly. Full review instructions, identity, contract, result and source packet reconstruct the entire retained prompt. No scientific module was imported or executed.

The raw generation response has one model candidate with STOP completion; extraction of its non-thought text exactly reproduces review.txt. Parsed review and verdict agree: ACCEPTED with no findings, missing assumptions or counterexamples and five explicit limitations. The review manifest binds the complete prompt, raw API response, extracted review, 13 inputs, source/workflow SHA and attempt identity. The separately published copies match the review archive.

The Actions publication archive reports exactly the same 33 source identities and review manifest independently reconstructed here. Its scope is source and reviewed-byte consistency, **not independent mathematical reconstruction or native-mechanism certification**. Its source tree, author, ancestry and cumulative changed paths match fresh GitHub metadata. This Actions job predates the durable evidence commit; the present audit supplies the later publication check.

The complete per-job endpoints contain 346 integrity, 398 review and 274 publication lines (1,018 total). The committed combined log contains every message in the same per-job order. Equality is established after removing the combined log's job/step prefixes and timestamp tokens: the two GitHub log representations differ slightly in timestamps, so raw byte equality is not claimed. Exact independently fetched endpoint logs and their hashes are retained in AUDIT_RAW_ACTIONS.zip and AUDIT.json.

## Receipt qualifications

1. The original receipt asserts `07bccacc` was live before the rerun. The attempt-specific API records start `2026-10-16T19:39:35Z` and creation `19:39:36Z`; `07bccacc` has committer timestamp `19:40:46Z`. The assertion is unsupported by the recorded chronology and must not be used as evidence. Commit timestamps alone do not reconstruct historical branch-ref state; that exact state is not established here. The evidence commit is a verified child of `07bccacc`, and the frozen workflow/source binding to `a42ca9e` is unaffected.
2. The generation response's modelVersion is `gemini-3.1-pro-preview`. The separate availability response's version is `3.1-pro-preview-01-2026`. They are distinct fields, not interchangeable generation-version claims.
3. The receipt's quota-top-up explanation is attributed to Aaron's report. This audit does not independently authenticate the chat authorization or establish the service-side cause of earlier HTTP429 failures.

Preserve the historical receipt and govern its interpretation with these qualifications. The root's reviewed stabilization drafts correctly retain the conditional result, the model/chronology qualifications and the open native obligations.

## Reproduction and boundary

Run `python audit_accepted.py` with AUDIT_RAW_PUBLICATION.zip, AUDIT_RAW_SOURCES.zip and AUDIT_RAW_ACTIONS.zip adjacent. The checker uses only Python's standard library, rejects optimized execution, validates every retained evidence-archive seal, and reconstructs AUDIT.json. The raw archives are self-contained (329100, 321417 and 434919 bytes respectively); no network, credentials or original scientific code execution is required. Temporary download URLs are excluded from retained evidence.

The accepted result concerns only the supplied prefix-preserving, cylinder-generated covariant history interface. Its five reviewer limitations remain binding. Native interaction and broad C3/C4–C6 remain **OPEN**. No inherited numerical replay, empirical validation, general physical impossibility theorem, native mechanism, main merge or numbered-stage CLOSED/CERTIFIED claim follows. No further review retry or research stage is started. Immutable readback of the forthcoming stabilization commit is a separate required final step.
