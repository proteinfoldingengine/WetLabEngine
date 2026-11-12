# Durable publication audit

Date: 2026-10-17 UTC. Evidence commit: 5cde4a9b0cdd6deea3a34c40718615af80cff3fa.

The immutable subtree was read independently through GitHub's Git tree API. It was not truncated. All 18 EVIDENCE_MANIFEST.json paths matched their declared Git blob identity and byte length. All 15 UTF-8 evidence files were additionally fetched from their immutable raw URLs and matched the retained exact content. The three binary ZIPs cannot be returned as bytes through this connector's UTF-8-only fetch endpoint; their published Git blob identities and lengths match the downloaded original bytes. Before publication, original download sizes and SHA-256 digests matched GitHub artifact metadata and every ZIP passed CRC and extracted-member byte equality checks. No second binary download from the repository is claimed.

The separate Actions publication audit passed 17 immutable original/current/frozen source readbacks and independently reconstructed prompt, raw response/verdict, model and workflow/run identities. All three jobs in run 39036030658, attempt 1, completed successfully. This durable audit verifies publication identity; it is not a new scientific review or test.

Verified durable evidence:

- evidence/artifacts/transport-integrity-1.zip: c4d153b0d312abd16dbd23f80aa42052cdc1395d, 2200 bytes.
- evidence/artifacts/transport-publication-1.zip: 10fa90e62e4d48116238ff810258a4ed399c2bcf, 3184 bytes.
- evidence/artifacts/transport-review-1.zip: 11e56ca74a2e04095a5ed05f330a7b284d2f397c, 53294 bytes.
- evidence/integrity/input_manifest.json: 47468240b4af98a30dac3146d7cf6a80b299223e, 2224 bytes.
- evidence/integrity/integrity.json: 66faa811633c00eab35985013790e001ad3976cb, 563 bytes.
- evidence/integrity/source_manifest.json: 4f10cfea185bb63ae0aae7ffbc1e6efe5daf313a, 1424 bytes.
- evidence/logs/argument-review.log: 2dcab2e6932924cf4a4402ffdf732e1f8495fd0a, 17981 bytes.
- evidence/logs/integrity.log: a208eb0aa0daf5e37b749340edc249786ca649f1, 27595 bytes.
- evidence/logs/publication-audit.log: 5e71da34e9a1a988374d4424e63ac4498f69674a, 20154 bytes.
- evidence/publication/remote_readback.json: e0c5009a0b025c8bac75cc3b7897f4c1a8f70c92, 12815 bytes.
- evidence/review/input_manifest.json: 47468240b4af98a30dac3146d7cf6a80b299223e, 2224 bytes.
- evidence/review/manifest.json: cf25c159e6cf6aa98636dba81e80511dcc798c1e, 1310 bytes.
- evidence/review/model_metadata.json: 928720139032813386b0cf0819cb291a2846a468, 459 bytes.
- evidence/review/prompt.txt: 55ef3b62aa0c31dd721d12cdbc2b9818e80551cd, 50712 bytes.
- evidence/review/request.json: 639a64ba661933ca98b22ff1ccd127ea4ca292c4, 52151 bytes.
- evidence/review/response.json: 7f1264bfc053cd60dcda762c15d350d880457a46, 16699 bytes.
- evidence/review/review.txt: 7508be30a3c16a6ec763863fa0457ecebd32fa03, 729 bytes.
- evidence/review/verdict.json: ef0f18a4766d1e58400822624c7b0ea6ebb128d7, 730 bytes.

Gemini ACCEPTED the frozen argument with no findings, missing assumptions or counterexamples. The bounded mathematical correction and category-C/native-promotion STOP are unchanged. No physical reversibility, native-event derivation, accessible-record origin, numbered closure or main merge is claimed. Final immutable readback of this audit follows.
