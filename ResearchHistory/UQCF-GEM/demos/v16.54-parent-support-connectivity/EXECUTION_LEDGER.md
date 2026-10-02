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
