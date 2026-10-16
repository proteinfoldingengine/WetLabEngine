# Stage 2 revision publication-integrity audit

Verdict: PASS for immutable byte integrity and publication boundary only.

Revised scientific commit `f62afaebdba109daad1031005af6c3529283bd24`, tree `89f661ac274bf3c447030657c1d82580de106912`, has sole parent `8f48da3e3c7f3165e27f64262c87f268cea64165`. The prior Stage 2 audit independently established that parent's sole parent as contract commit `cbefdb85f21cd9606d1a9260d38176c2dc068b91`. The published manifest declares exactly this ordered repair chain and the original source parent `1ef7d25cedd5af6be6e72fea4e5963414a92cc0a`.

Complete non-truncated tree descent from the prior scientific root to the revised root proves exactly eight changed paths: the workflow and analytical_repair/EXECUTION_REPAIRS.md, campaign.py, input_manifest.json, publication_manifest.json, publication_readback.py, test_infrastructure.py, test_publication_readback.py. Every fetched tree reproduces its Git object identity. There are no deletions, mode changes, type changes, or other edits. Composing that complete delta with the independently verified contract-to-first-publication boundary gives exactly the revised manifest's 25 cumulative paths.

All eight changed files were independently retrieved at the revised immutable SHA. Their full bytes match the local payload, all computed blob identities match GitHub's returned identities and tree entries. The cumulative publication and frozen-input union contains 46 files: eight fresh readbacks plus 38 unchanged byte objects reused from the prior audit with unchanged tree identity proven. Every frozen input identity matches the revised input manifest. No unchanged source original was downloaded again.

The original continuation-plus-appendix identity and unchanged contract checks inherit from the prior Stage 2 audit through the complete unchanged-file proof; neither path changed in the revision. The original Stage 1 and Stage 2 evidence files remain intact.

Evidence: STAGE2_REVISION_AUDIT_EVIDENCE.json contains fresh/reused file identities, exact comparison checks and cumulative leaf changes. revision_commit.json, revision_tree_evidence.json and revision_fetches.json retain complete connector evidence. Raw revised files are under originals/f62afaebdba109daad1031005af6c3529283bd24/.

This does not accept the whole checkpoint or establish mathematical correctness. Actions, mandatory independent Gemini review, durable execution evidence and final receipt/readback remain separate obligations. No scientific execution or repository mutation occurred during this revision audit.
