# Approved C3 evidence recovery and publication repair

Date: 2026-10-08. Verified integrated parent: cac8f8888e329e1bdee25f8a6bce39e83f8363b2.
Status: ENGINEERING EXECUTION SCOPE, not mathematical review or scientific closure.

## Fixed objective and evidence

Recover the entire ZIP archives and all members from failed runs 37832509819/1 and 37832751396/1 into durable GitHub evidence, repair automatic evidence publication, and verify exact immutable readback. The user approved this operational next step. Do not modify the C3 theorem, its finite domain, historical run outcomes, authentication permissions, branch protections, or mathematical acceptance requirements.

Pinned archives already downloaded and freshly hashed before this scope:
- Artifact 11574560540, run 37832509819/1, scientific SHA 6a4ba75ca3a1ce332e6481e383bfecf6046f31b9, 11406 ZIP bytes, five members, SHA-256 c2b4645fa1c066b3c606c80f55a112e35d67cef5177edbff8644e8b978344312.
- Artifact 11574595760, run 37832751396/1, scientific SHA ad42d751f69c6fba7af585e6ba15b00941bc201f, 18798 ZIP bytes, twelve members, SHA-256 d04fda1889c362d3ed590cf953bf3e42bf9e0625a0bd4f8788589201ad244246.

The first run has eight expected RED C3 contract failures; the second passes scientific checks but its evidence push fails. Both overall GitHub conclusions remain FAILURE regardless of recovery.

## Diagnosed boundary and testable repair

The captured failures occur at server-side acceptance of git push creating a new evidence reference; uploads and ordinary repository contents writes succeed. The exact diagnostic is a workflow-change permission-check timeout, not sufficient evidence that the configured token lacks the necessary permission. GitHub first-party repository reports describe the same timeout even with workflows-write permission (cli/cli issue 13635). The underlying server implementation is not inspectable here.

Test a bounded alternate publication transaction using the documented Git Database API with the SAME GITHUB_TOKEN and existing contents:write/actions:read permissions. First seed the unique evidence reference at the already published scientific SHA. Then construct a single-parent commit that adds ONLY evidence paths and update that reference without force. Before and after reference update require the exact added-path/blob set; verify all immutable blob bytes. Do not grant workflows-write, edit scientific outputs, suppress failures, or relabel a failed run green. A rejected API authorization or unexpected ref must fail closed.

Use a dedicated stable archive reference for the two pinned historical archives. Subsequent workflows may reuse it only after validating its immutable manifest and every referenced blob; this avoids depending on expiring Actions artifacts. Preserve original ZIP bytes, all seventeen extracted member files including empty logs, source/run metadata, and SHA-256 plus Git-blob identities. ZIP traversal, duplicates, symlinks, wrong digest/source/count and over-budget data must be rejected.

## Tests and execution

Write publication contract tests first and preserve actual pre-implementation RED output. Test archive fidelity, malformed archives, evidence-only paths, exact readback, source-reference collision, non-force updates, and denied API operations. Keep science and publication tests distinct.

Only change the existing workflow's publication integration and add publication safety tests; retain its pinned Actions, contents/actions permissions, scientific commands, failure propagation, and 2 MiB output budget. Run the existing eighteen verification contracts and A12 bounded primary/reproduction gates on GitHub again. Download and hash the final run artifact and verify exact evidence commits through the connector.

Bounded resources: Python standard library; two small pinned archives; at most 2 MiB per publication payload; no numerical domain enlargement; no external-AI review or polling. The current C3 checker and all original proofs remain untouched.

## Required reporting

Separate historical execution failure, recovered archival integrity, new publication success, mathematical acceptance, and physical interpretation. Report exact workflow/scientific SHAs, run/job/artifact IDs, archive digests, evidence commits, and any remaining failure. Native observer access/progress, independent mathematical review and its subsequent publication audit, and broader C3/C4-C6 remain OPEN. No main merge or numbered-stage certification is authorized by this repair.
