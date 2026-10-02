# SDD ledger — plan: ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/PROSPECTIVE_VALIDATION_PLAN.md

Approved: 2026-10-02, plan SHA256 d4d13e0ebb6feb63c0f235ff5c06d7ab36cb9c497f07df988f306e1d683e1d63 at 16b5d9340d29cb29907cee67751e15774694cf14. Native execution.

Ruling: use the existing API-backed isolated branch/source mirror rather than a clone or local worktree — preserves the session's established workflow and GitHub-only scientific execution — wrong source mapping would invalidate provenance, so every published source is byte-checked.
Ruling: add branch-scoped push transport to workflow_dispatch with immutable committed run requests — no dispatch operation is exposed by the connector — wrong SHA selection would invalidate evidence, so workflow and scientific SHAs are separately verified and archived.

Pre-flight shared interfaces:
- Task 1 -> Tasks 2-4: canonical Case identities, generate_cases/reconstruct_cases and verify_universe; JSON parameters and complete multiplicity equality are common contracts.
- Tasks 2-3 -> Task 4: produce/verify_record paths and typed refusals; independent verifier imports no producer logic.
- Task 4 -> Task 5: deterministic scientific files and run-specific provenance are separate; actual-merge replay must bind both source/evidence heads.

Task 1: in progress. Prospective freeze prepared; no scientific execution yet.
Tasks 2-5: pending.

Task 1 RED: GitHub run 37042645917, scientific 5169c010228bbff501de68015fecd7cb98f5fded, workflow 8a9e46a1f0735e8ec4412dac40d7efe047819f29. Observed 8 tests, 7 assertion failures, zero errors. Original artifact 11243275224 downloaded; SHA256 dafd8baccff3c91edc247ba0aeaef95e987255cdee9cd000f8559758199f31f1 verified against API and all internal source hashes.
Ruling: supplement the initial protocol with explicit hashes of all prior independent review files — the approved immutable commit already bound their bytes, but the initial JSON listed proof hashes only — no scientific domain changes; initial RED remains preserved, and subsequent runs bind the completed manifest.
Ruling: keep complete identity sorting on disk using SQLite — the protocol specifies exact lexicographic equality under a 4 GiB limit — database or resource failure makes the campaign INCOMPLETE, never a sampled PASS.
Ruling: M2 element-cover inputs are typed auxiliary blocks, permitting empty bins/capacity k as the approved domain states — native root nonemptiness applies to native-path records, not auxiliary proof objects — conflating these types would invalidate native claims, so the verifier checks them separately.

## Execution checkpoint after source review

Task 1 universe GREEN: run 37044386062; eight tests, zero failures/errors/skips. Downloaded original artifact 11243858633 SHA256 e77367ada320a3f0d37b81966b5c82b89ed509fd1d281be63803f3cd3796c84a verified, as were all archived source hashes. Full independent/producer identity streams have identical uncompressed SHA256 9ab3d0efcf5d3ddd6fd8a320b28f02daa270267759aa89364f4b8d8b0ec503cb. This establishes universe equality, not path validation. Provenance review RED/GREEN and source closure are recorded in INDEPENDENT_IMPLEMENTATION_REVIEW.md.

Task 2 RED: run 37044850393, 18 tests, 17 assertion failures, zero errors. Initial targeted GREEN: run 37046781551, success. Independent review then exposed important verifier and deterministic-order defects; genuine review RED runs 37047482337 and 37055853168 precede corrections. Targeted GREEN was not treated as full-domain acceptance.

Task 3 RED: run 37046939873, seven tests, seven assertion failures, zero errors. Only after inspecting these failures were palette/support transformations and native lifting implemented. Native clearance binds read-only producer.py and feasibility.py bytes to certified parent f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8.

Ruling: the producer model uses immutable support sets and dynamic programming over root-coverage masks, while the independent verifier uses direct active-label subset search. This refines the planned producer representation without changing any protocol case, move, resource limit or mathematical claim. No shared hitting implementation is imported.

Current integrated development source: 8b1e82d96a104482c3f2fb890d049325740aa7dc. Full domains, inherited-stack run, fresh reproduction, publication and actual-merge audit remain outstanding.

Integrated development run 37056199912 passed all 45 then-defined tests, including native lifting and both independent universe streams. Follow-up review required complete canonicalization suffixes, ordered cycle rotation, exact guard boundaries and native clearance events. Run 37056662003 observed eleven assertion failures in twenty-five tests, zero errors: five follow-up trace controls and six prospective campaign-evidence controls. Corrections published at 93a0887adc3d650292ccf08f63a02b755e978388; new integrated GREEN is pending.

Prospective campaign transport ruling: each full-domain launch commit changes only CAMPAIGN_REQUEST.json from its recorded immutable scientific parent; the workflow verifies that exact single-file difference and immediate parent. The immutable GitHub event SHA is the actual scientific checkout for every shard and the inherited stack, and both scientific/workflow fields truthfully record it. This keeps unchanged inherited provenance guards intact, without substituting environment SHA values. Prepared scientific code/protocol bytes are frozen before the launch commit; the request cannot alter them. This replaces the two-checkout development transport for full campaigns only. No domain, resource, mathematical or certification requirement changes.

Campaign shard intervals are eight contiguous intervals of the independently matched sorted universe, with complete membership and hashes frozen before any path production. Local-stage scope is exactly M1–M6; extension-stage scope exactly M7–M9 plus the complete inherited stack; final scope is all families plus the complete inherited stack. A failure retains its case/certificate; unfinished work is INCOMPLETE and never silently sampled.

Second follow-up source reviews accepted M1–M6 and M7–M9 at 93a0887adc3d650292ccf08f63a02b755e978388, contingent on GitHub verification and full-domain execution. Subsequent performance refinement memoizes at most 10,000 exact immutable support tuples in the independent direct-subset hitting search; no case, label, root or path is removed. The producer and verifier still use separate hitting algorithms. The first definitive campaign will cover all M1–M9 together, satisfying both domain obligations at one immutable scientific SHA; it is gated by the complete development suite and followed by the full inherited phase.

Integrated trace GREEN: run 37058127774, scientific 93a0887adc3d650292ccf08f63a02b755e978388, workflow 554965e8e7c1f00ec48a67e297789e15b2d7d907; sixty tests, zero failures/errors/skips. Specific empty-contraction-finite and below-floor-cycle controls also pass, extending the original false-fact/floor rejection coverage. Independent source acceptance remains conditional on complete-domain execution and later closeout gates.

Campaign runner review RED: 37059096994, ten tests, two assertion failures, zero errors. Corrected stale-record retention and added atomic pre-production identity checkpoint. No primary campaign has started before this correction. Its first full campaign development gate must reject any regression before the eight path shards can begin.

First complete campaign launched: scientific/workflow SHA 0ba1284ade581267997882de2d4c723f2b9ee3a4, run 37059520424. The development gate passed and all eight complete-domain shards started. This is an in-progress validation, not a success claim.

Aggregation/reproduction RED run 37059832519: nine tests, seven assertion failures, zero errors. Controls cover absent/duplicated shards, overlapping intervals, mismatched full universe, missing mechanism categories and changed/omitted deterministic files. Aggregation is being implemented while the immutable first campaign runs.

Aggregation initial GREEN run 37060796749 passed nine controls. Independent publication review then required executing-helper/target-run binding, full unchanged inherited-package verification and durable INCOMPLETE status. Genuine review RED run 37061765428 observed thirteen tests, four assertion failures, zero errors. Corrected source e7967c1fbef4b268c11da796ec5633253de54b24 passed all thirteen controls in run 37062080622; independent source rereview accepted all three corrections. Real aggregation, reproduction and actual-merge audit remain outstanding.

First complete campaign checkpoint: all eight M1–M9 domain shards passed in run 37059520424; the full inherited job is running. This is not aggregate certification: original artifacts and mechanism diagnostics still require complete aggregation.

Reproduction transport ruling: subsequent campaign artifacts include the GitHub run-attempt suffix. This preserves both original and fresh-run artifacts without deletion or name collisions; it changes neither scientific files nor frozen domains/resources.

Task 4 checkpoint: first full campaign37059520424 completed successfully, including all8 complete domains and unchanged full inherited stack. Aggregation37063427057 at3c7490fd4121708d329ce5d057ac95082b619aa1 completed successfully; inherited package verification reported2049 source members. Complete mechanism diagnostics and independent identity-stream equality passed. Fresh reproduction and actual-merge replay remain pending.

Actual-merge binding RED37062647557:15tests2assertion failures0errors. GREEN37062979456 passed. Independent transport review accepted corrected routing at8376b663b74825f58cf6dffe82ea65e18a233b10: contract-only feature pushes skip scientific jobs; integration merge runs all8shards and inherited; requested/event SHA equality is checked before routing.

Ruling: publish large original campaign ZIPs as ordered16MiB binary parts with per-part hashes, original archive SHA/length and verified exact reconstruction — the inherited original is114,011,453bytes, beyond the local32MiB transfer and Git100MiB blob bounds — wrong reconstruction invalidates evidence, so byte equality is checked before publication. The aggregate transfer wrapper duplicates the originals; its API digest/length are verified and retained in the receipt, while the8 original domain ZIPs and original inherited ZIP are preserved in full. No scientific domain, resource bound or successful-result criterion changes.

Ruling: use a GitHub-only evidence packaging job to push only the verified evidence prefix to a fresh isolated evidence branch, then integrate its exact blobs through the existing API — avoids local scientific execution and oversized tool payloads — incorrect source/destination binding would invalidate publication, so the request, aggregate run, original digests and isolated branch are enforced and independently reviewed before launch.

Archive preservation RED37067368613 observed17tests2assertion failures0errors. Corrected exact-byte splitting and publication transport are under GitHub GREEN/source review. Universal higher-floor connectivity remains OPEN.

The evidence packaging stage consumes the already RED/GREEN-tested compare_reproduction contract when an explicit published run/attempt reference is supplied. It loads that deterministic manifest directly from the executing Git HEAD and requires exact nonempty membership/hash equality, recording both manifest digests and the immutable reference blob. This is the execution wiring for Task4's predeclared byte-equality gate, not a new scientific domain or weaker reproduction criterion.

Complete development GREEN37068234545 passed81tests in274.257seconds, zero failures/errors/skips. Archive write-boundary RED37068025565 had19tests2assertion failures0errors; corrections at06532593be7b1c6bb75473ae702a9cba58303c17 were independently accepted. Evidence branch creation now has an atomic absent-ref lease and cannot update any pre-existing branch.

Reproduction integration review identified explicit-null comparison bypass and an overly broad equality type. Genuine RED37068702175 reproduced both (21tests2assertion failures0errors). Corrected source287227a0abaf271fa1e842c859abbc76f2d27a30 validates requested reference before any I/O and requires nonempty dictionary equality. Independent review accepted the corrections, with targeted GitHub GREEN pending before launch.

Premerge/actual-merge external exact-object gate: after complete reproduction/publication review, capture the exact reviewed PR head, integrated base head and their trees. Invoke merge with expected_head_sha and merge method merge. Before closure, require the returned actual merge commit's ordered parents to equal exactly [captured base, reviewed PR head], and verify source/evidence tree bindings plus the complete replay. Record those exact objects in the durable audit receipt. The in-workflow bind_actual_merge scientific parity/ancestry check supplements this external gate; it does not replace exact reviewed-head/base verification. Any concurrent base/head movement is detected and cannot silently certify a different object.
