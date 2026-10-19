# D24 range-certificate export contract (draft, unexecuted)

Author: proteinfolding-gpt. Preparation date: 2026-10-19.
Status: LOCAL DRAFT FOR REVIEW. No new scientific execution or external publication has taken place under this contract. Commit the reviewed contract before any later authorized regeneration.

## Purpose and claim boundary

Preserve independently checkable certificates for the exact finite range results already accepted in receiver-identification draft 24. This is archival support for that accepted conditional result, not native informational progress, a new theorem campaign, a new Gemini review, or recovery of the original run's discarded memory.

The original four Actions ZIPs preserve all files actually emitted by the original runs. Primal/dual vectors, proof multipliers and complete carrier/row sets were not emitted. Newly produced certificate objects must be labelled **regenerated** and attributed to their new execution. The original scientific source, code, preregistration, failures, review response and receipts remain immutable.

This narrow contract exports complete certificates for the 80 primary systems and 1,030 primary ranges, their complete carrier/constraint domains, and the original diagnostic with its asymmetric verification scope. The old witness/control summaries must still reproduce byte-for-byte. It does not expand every old witness Boolean into an evaluation transcript, rerun the inherited foundational stack or complete every governing closure obligation. Public raw-review archive publication remains a separate permission gate.

## Fixed original identities

- Repository: proteinfoldingengine/WetLabEngine
- Branch: research/uqcf-overlapping-guard-exchange
- Frozen construction: 3e6f1cf3042ed3c6cd49b29d396f86cddb7bf9c6
- Preregistration: d567148f8263de96654ea3e9bcc49fd25a0132fc
- Scientific/workflow code: 57895f62297c6100c1a4b8f185857a7905da780b
- Original review run: 39300667905, attempt 1
- Original push verification run: 39300628093
- RESULT.md SHA256: 7600ad3708baa287ac877afa582d83073a02f0ec72bf11d6ddcfbeb091ba43cc
- FREEZE.md SHA256: a0bc94537c4dd008fd0e4349e7bfbc9b154707a63a67f6e8a7f9d5e5f3f4ebf1
- Original producer source SHA256: 942ea9de0835849973046f0e6c079acb5c7e73fa04524eca289d7546bfd5d004
- Original checker source SHA256: 2f7789a70113a08eaab4d9ce159245813bb1e982dd1971e8f646d999ea44dc2c
- Original producer.json SHA256: 04be86d04551748dca905eb2aa2cac74977d86d7edd8f2aaa5d7db9ee411a9f9
- Original checker.json SHA256: 9bace24c70c57cd2c62a47e1f15ce1f01977a1c86e1ba3be9f752daa384a7572
- Original compare.json SHA256: e2d741a54f05899075dbf6c94e3c700095506231042fe0b3a18601d17e45849e
- Acceptance receipt: 5f354b33d708c48e4588215d5fbf576edeb33e9a/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_review/STATUS.md

Original artifact identities are recorded separately in the verified original evidence manifest; no raw review archive is included in this code-preparation package.

## Exact finite scope

Use the original FREEZE.md, without changing its domain:
- BIN_N, N=5,6,7,8, D=1,...,N-1: 22 systems.
- ALL_7 and ALL_8, D=1,...,N-1: 13 systems.
- CH_7, D=1,...,6: 6 systems.
- COMB_D, D=1,...,4: 4 systems.
- One-tooth-removed COMB_D-k, k=0,...,D-1: 10 systems.
- K_2,m, m=0,...,4, D=m+1,...,5: 15 systems.
- K_3,m, m=0,...,3, D=m+1,...,4: 10 systems.
- A separate no-blindness diagnostic on BIN_7, target A(1,0).

Every primary system includes all A(j,i), 0<=i<=j<=D, with both endpoints: 1,030 targets and 2,060 endpoint certificates per exporter. The normalization is kappa=1. The original separate zero/negative-kappa witnesses remain in legacy summaries; these normalized finite ranges do not prove the fixed-zero necessity direction.

The full K_B^(m) comparison class, rather than an upper branching cap alone, supports the general residual bound. The finite K systems are exactly the restricted U7 classes in the original freeze. Cumulative A columns, universal-over-tables necessity and the internal-vertex depth horizon retain their original precise meanings.

## Export format

Each exporter writes two new files: an original-format legacy summary and a deterministic certificate archive. Both refuse to overwrite any existing output. The archive is UTF-8 JSON, sorted object keys, indent 2, ensure_ascii=False, trailing newline. Its deterministic content contains no new timestamp or new run ID. A later execution manifest must bind these separately to the new workflow SHA, contract SHA, exporter hashes and environment.

All object key sets are strict. Duplicate JSON keys, missing keys and extra keys are rejected. All integers exclude booleans. All rational values are canonical strings exactly equal to str(Fraction(value)); floats and alternative spellings are rejected.

Top-level archive keys:
- schema_version: uqcf-rid24-range-certificates-v1
- evidence_kind: regenerated
- role: producer or checker
- basis: nu for producer, A for checker
- origin: code_sha, result_sha256, freeze_sha256, run_id, attempt, source_sha256 and summary_sha256, exactly matching the fixed original identities
- exporter_sha256: hash of the additive exporter file actually used
- classes: complete class dictionary
- systems: exact dictionary of 80 primary systems
- diagnostic: scoped diagnostic record
- legacy_summary_sha256: hash of the original-format emitted summary, equal to its pinned original hash

A class contains exactly:
- carriers: complete sorted canonical rooted-tree strings, without duplicates
- keys: ordered variable pairs [k,i], all 0<=i<=k<=K for the class maximum depth K
- pos_rows: complete distinct nonzero sparse holding rows, sorted lexicographically

A sparse row is an ordered list [k,i,integer_coefficient], with no repeated variable or zero coefficient. The producer and checker rows use their own declared coordinate bases. The full carrier and row identities are retained, not digest-only.

A primary system contains exactly class_id, D, blind, targets, equalities and endpoints. Targets are ordered by j then i. Equalities start with normalization, then the D consecutive diagonal differences. Each equality contains row and rhs.

Every endpoint contains exactly target, sense, value, primal, ineq_multipliers and eq_multipliers:
- sense=1 minimizes A(j,i); sense=-1 minimizes -A(j,i).
- value is the actual unsigned range endpoint, not the signed optimization objective.
- primal is dense in the class variable order.
- Inequality multipliers are dense in the class POS-row order.
- Equality multipliers are dense in the system equality order.

The independent validator checks exact feasibility, nonnegative inequality multipliers, objective reconstruction and zero duality gap. If c is the signed target objective, x the primal point, R the POS rows and E,b the equalities, it verifies:
R*x>=0; E*x=b; lambda>=0;
c=lambda*R+mu*E;
c*x=mu*b;
value=sense*(c*x).

The producer diagnostic uses the same full system/certificate format with D=0, blind=false, target [1,0]. The checker diagnostic contains exactly kind=attainment_only, class_id=BIN_7, target=[1,0], value=1/2 and its dense primal table. It remains an attainment check, not an independently exported upper-bound proof.

## Export implementation boundary

producer_export.py and checker_export.py are additive copies of the original scripts with serialization hooks and output/provenance guards. They preserve all original scientific calculations, parameter values, finite-domain choices and legacy summary bytes. They do not import each other. Original sources are not edited.

The producer retains its already computed rational primal/dual vectors after the original exact checks. Failed or missing certificates stop export; no tolerance retries or alternative answers are permitted.

The checker exports the exact original proof mechanism:
- Lower endpoints: leaf holding row.
- Zero upper endpoints: fork/chain nonnegative row combination plus diagonal equality.
- Positive residual upper endpoints: chain/fan row combination and normalization/diagonal equalities.
- Diagonal endpoints: normalization plus diagonal equalities.
- Attainment: the existing identity or extremal table, tested against the full class.

The solver-free independent validator imports neither exporter and uses no floating-point solver. It reconstructs complete classes and constraints independently, compares full canonical identity sets, validates all certificates, and checks both archives against the original pinned summary bytes. Exporter self-hashes are checked against sibling source files without importing them.

## Prepared rejecting controls

Tests are authored before implementation and remain **unexecuted** in this preparation pass. No RED/GREEN, runtime correctness or deterministic output claim is made.

Required rejection targets:
1. Noncanonical rational spelling or non-string numeric input.
2. Duplicate JSON keys and strict-schema omissions/extras.
3. Forged original/regenerated identity, source, exporter or legacy-summary provenance.
4. Missing, extra or duplicated system, target or endpoint.
5. Count-preserving carrier substitution and incomplete class identity sets.
6. Missing, duplicated, substituted or altered POS rows.
7. Infeasible primal point or violated equality.
8. Negative inequality multiplier.
9. Incorrect dual reconstruction or nonzero duality gap.
10. False endpoint value.
11. Checker diagnostic misrepresented as a full bound proof.
12. Output overwrite attempt.
13. Nondeterministic serialization or mismatched fresh export bytes.

Small synthetic arithmetic/schema fixtures test validator mechanics only. They must never masquerade as complete accepted D24 archives. Complete archive and mutation validation requires a later expressly authorized scientific execution.

Future acceptance requires the full integration, exporter-guard and fresh-reproduction controls to run with no required control skipped. A successful unit-test exit with skipped integration controls is not archival closure. Fresh-reproduction inputs must come from separate authorized execution, be validated as complete archives and match the first producer/checker archive bytes exactly. Distinct paths alone do not prove independent execution; the outer run manifest and logs must establish that provenance. Full-file controls also reject noncanonical whitespace/key ordering, rather than relying only on parsed-object tests.

## Future execution gate and stopping rule

Before any scientific execution:
1. Verify identity exactly proteinfolding-gpt, current head, governing records and concurrent owner workflows.
2. Confirm scope and avoid overlap with the owner's POS/uniformity investigation.
3. Commit the reviewed contract and code before regeneration.
4. Review and freeze the exact execution/publication job plan, runner and resource/time limits before dispatch; no such workflow is included in this preparation. Pin/record the actual environment. Original versions were Python 3.12.15, numpy 2.3.5 and scipy 1.16.3. Execute exporters from the repository root. Test environment switches select controls and do not themselves grant authorization.
5. Preserve all existing frozen files and historical evidence.

One coordinated export/validation campaign is sufficient if successful. The later publication job must freshly reproduce both exporters in separate processes and compare their complete deterministic scientific certificate bytes against the initial export. Any disagreement with the original summary hashes, failed certificate, missing coverage, nondeterminism or mutation-control failure is RED and retained; stop and report instead of changing the contract or silently retrying.

No workflow is included or launched in this preparation package. No Gemini rerun is proposed. Original raw public archival approval is separate and pending. Any later durable publication must retain original-versus-regenerated provenance, full manifests and immutable readback. Completion of this range-archive repair does not imply full inherited-stack/AGENTS closure or native receiver access.

