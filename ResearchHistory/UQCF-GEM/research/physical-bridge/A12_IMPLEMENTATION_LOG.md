# A12 bounded verifier implementation ledger

Date: 2026-10-06 UTC. Base: 89aeab82272f163c0e3045e05c6224c4c81e34a8.
Authority: user approved the next work under protocol 291425d273412a65e98facc79bc368616200d7a1, with the candidate's prospective five-label fixture clarification.

## Pre-execution findings and rulings

The consolidated candidate at 5541843b2539cd714796d2e9c94d05741b2a49d8 silently substituted several A12.5 supports in Section 6. The original scope/proof bytes did not change, but claiming that the consolidation reproduced the original fixtures was inaccurate. The source-fidelity test was committed first and failed on those substitutions. R1 restores the exact originals:

L: ({d}, {a,c}, {c,e}, {a}, {a,c,e}, {a,b}).
I: ({d}, {a,b,e}, {a,b,e}, {a,c,e}, {b}, {c}).

Both initial tau=3 arguments and both endpoint arguments in the consolidation apply to these originals. This is a candidate-source transcription correction, not a new counterexample family or change in the frozen universe. R1 also escapes the Markdown table bars and makes original publication status explicitly historical; no other mathematical conclusion changes.

Two calculations are now implemented with shared integer-mask input representation only. Reference tau enumerates actual sets by cardinality; it does not import or call W/C/A/D. The reference and primary universes use different Cartesian-product constructions and compare complete identity sets. Pure support memoization is disclosed; every labelled support/floor identity and its obligations remain visited. No sampling or quotient is introduced.

## RED evidence and pipeline correction

Initial RED source: 4928457ebe247382a714584a478fe057ddbad5d8.
Run 37500570046, attempt 1, job 112396204906.
Durable evidence: c008c2679ce4c0f6747ca10ec0279a754c551820 on research/a12-evidence-37500570046-1.
Actual unit output: 10 tests, 9 assertion failures and 1 original-blob preservation pass. Eight failures were unimplemented core contracts; the ninth was the A12.5 source substitution. No scientific main program existed.

Additional implementation defect: implicit shell was bash -e without pipefail, so tee masked test/nonexistent-command exit statuses. Later steps were wrongly labelled successful by the platform, until the final missing-output check failed the whole job. Do not report those step labels as successful scientific execution.

Repair source: 8be884e9793e5ba69f456f61a434f6f086d75ad5. The workflow now sets shell: bash explicitly, enabling -eo pipefail, and includes an exit-23 pipeline control.
Repaired RED run 37500792495, attempt 1, job 112396959265.
Durable evidence: 89f956ff96e514092000b785faac1c7414f5f3d3 on research/a12-evidence-37500792495-1.
Observed: pipeline control succeeded; the unchanged 10-test suite failed with 9 assertion failures; rejecting/full/reproduction/join stages were skipped. Raw contract log was read back. This verifies failure propagation before the implementation is called passing.

## Candidate implementation freeze

Implemented certificate.py, reference.py and verify.py after observing RED. Contract tests remain unchanged. The main verifier follows the exact 35,792-state scope, checks all required primitive/candidate/response/covariance obligations, all original symbolic fixtures and the declared collective cubes, and records eleven deliberately false claim/record rejections (the protocol's ten plus the declared same-root margin interpretation check).

The workflow has contents:write solely for a unique evidence-only branch and actions:read for run/job metadata. It does not move the active research branch, edit scientific sources, close issues, or assert full A12 closure. Scientific network inputs are absent. GitHub setup/publication/metadata access is not a scientific premise.

Status at this implementation freeze: code and corrected candidate written; full bounded execution and reproduction NOT YET completed. Next: execute this frozen source, inspect all obligations/logs, preserve actual outcomes, then reconcile reporting and immutable readback. A12 remains OPEN. No outside-AI calls, local scientific execution, certified-engine imports, whole-history replay claim, A12.6 or physical inference.
