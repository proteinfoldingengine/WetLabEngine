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
