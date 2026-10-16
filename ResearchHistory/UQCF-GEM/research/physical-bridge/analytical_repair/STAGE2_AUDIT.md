# Stage 2 independent publication-integrity audit

Verdict: PASS for exact publication bytes and repository change boundary only.

Scientific commit: `8f48da3e3c7f3165e27f64262c87f268cea64165`.
Scientific tree: `acdfd9ca7167138d73d5547e6c070270283f6441`.
Sole parent and contract commit: `cbefdb85f21cd9606d1a9260d38176c2dc068b91`.
Original source parent: `1ef7d25cedd5af6be6e72fea4e5963414a92cc0a`.

All 24 expected changed paths were independently fetched at the scientific commit. Including unchanged frozen inputs, 45 immutable file readbacks were performed. All remote bytes equal the supplied local files, all computed Git blob identities equal GitHub's returned identities, and all input_manifest entries match fresh byte counts and SHA-256 computations. The publication manifest's source_parent, contract_commit, parent and exact changed path set agree.

The complete change boundary was reconstructed by descending every differing tree from the parent and scientific roots and pruning only identical entries. All 26 fetched, non-truncated Git tree objects reproduce their Git object hashes. The resulting leaf set is exactly the 24 manifest paths (19 added, 5 modified); there are no other edits, deletions, mode changes, or type changes. Each changed leaf blob matches the separately fetched published bytes. The API commit metadata confirms the scientific SHA, tree and sole parent independently.

The continuation is exactly the independently retrieved original 1ef7d25 bytes followed by the published analytical_repair/INDEX_APPEND.md bytes, with no other modification. CONTRACT.md at the scientific commit is byte-identical to the independently fetched cbefdb85 parent original. Earlier source-audit raw evidence remains intact under originals/ and stage1_* files.

Evidence: STAGE2_AUDIT_EVIDENCE.json contains the per-file identity checks and summary checks; stage2_tree_evidence.json retains complete tree entries and the full leaf difference; stage2_fetches.json, stage2_commits.json, and stage2_contract_parent.json retain original connector responses. Raw scientific bytes are under originals/8f48da3e3c7f3165e27f64262c87f268cea64165/.

This audit does not claim the whole checkpoint is accepted. Actions verification, mandatory independent Gemini mathematical review, workflow publication audit, durable execution evidence, and receipt/final readback remain separate obligations. No scientific execution or repository mutation was performed during this Stage 2 audit.
