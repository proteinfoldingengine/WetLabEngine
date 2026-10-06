# A12 bounded verifier implementation ledger

Date: 2026-10-06 UTC. Base: 89aeab82272f163c0e3045e05c6224c4c81e34a8.
Authority: user approved the next work under protocol 291425d273412a65e98facc79bc368616200d7a1, with the candidate's prospective five-label fixture clarification.

## Pre-execution findings and rulings

The consolidated candidate at 5541843b2539cd714796d2e9c94d05741b2a49d8 silently substituted several A12.5 supports in Section 6. The original scope/proof bytes did not change, but claiming that the consolidation reproduced the original fixtures was inaccurate. Restore the exact originals before a passing campaign. A source-fidelity test is committed first and is expected to fail against the current consolidation. This is a transcription/candidate-source correction, not a new counterexample family or a change in the frozen test universe.

Original L: ({d}, {a,c}, {c,e}, {a}, {a,c,e}, {a,b}).
Original I: ({d}, {a,b,e}, {a,b,e}, {a,c,e}, {b}, {c}).
Both initial tau=3 arguments and both endpoint arguments in the consolidation apply to these originals: {a,c,d} and {b,c,d} cover initially; {a,b,c} covers the legal L endpoint; {b,c} covers the illegal I endpoint with distinct singleton lower bound. That written reasoning does not replace the declared computation.

Use separate reference and certificate modules with shared integer-mask input representation only. Reference tau uses actual set intersections over all palette subsets in cardinality order; it must not call certificate fields or margins. Primary and reference universe generators use different product constructions and compare complete identity sets, including duplicates/omissions rejection. Caching pure support calculations is allowed for repeated floor assignments, but every labelled support/floor identity and its required obligations are still visited. No sampling or quotient is introduced.

## Execution order

1. RED: run committed contract tests against explicit unimplemented scaffolding and the incorrect consolidated fixture transcription. Preserve actual failures; no primary campaign should run.
2. Implement certificate/reference calculations and complete bounded obligation verifier. Restore the original A12.5 fixtures in a new candidate revision and fix Markdown table escaping. Freeze all source before the next run.
3. Run unchanged contract tests, rejecting controls, complete primary domain and all frozen fixtures/cubes. Reproduce in a fresh process from the same commit and compare deterministic scientific JSON byte-for-byte.
4. Preserve small output/logs on a unique evidence-only branch based on the exact run source. The workflow may create that new branch using its repository token; it must not advance the active research branch, edit proofs, close issues, or declare overall A12 closure. Integrate evidence only after inspection.

The workflow has contents:write solely for durable evidence publication and actions:read for run/job metadata. GitHub metadata requests are not scientific inputs. No outside-AI calls, local scientific execution, certified-engine imports, whole-history replay claim or new physical interpretation is authorized.

Status at this commit: tests/scaffolding/workflow written, not yet executed. Main verifier and corrected consolidated source still pending. A12 remains OPEN.
