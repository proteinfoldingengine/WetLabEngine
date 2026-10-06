# Reproducing the bounded A12 check

Scope: A12_SELF_CONTAINED_AUDIT_PROTOCOL.md at 291425d273412a65e98facc79bc368616200d7a1, with the prospectively recorded five-label clarification. This is finite corroboration of the consolidated written arguments, not a proof of universality, an outside-AI review, or an inherited-engine recertification.

Use Python 3.11. No packages beyond the standard library are required. Scientific execution for this project is GitHub Actions only, workflow .github/workflows/uqcf-a12-self-contained.yml. The commands below are exactly the commands to reproduce in that tracked workflow from a frozen commit:

```bash
A12=ResearchHistory/UQCF-GEM/research/physical-bridge
python -m unittest discover -s "$A12/verification" -p 'test_*.py' -v
python "$A12/verification/verify.py" --controls-only --output controls.json
python "$A12/verification/verify.py" --output primary.json
PYTHONHASHSEED=1 python "$A12/verification/verify.py" --output reproduction.json
cmp primary.json reproduction.json
```

The workflow applies 600-second command limits and a 25-minute job limit. Every pipeline uses explicit Bash with pipefail. An exit-23 control verifies that tee cannot hide a failed command. No complete check is considered passing until the contract suite, rejecting controls, both complete executions and exact reproduction comparison pass. Files from failed runs are retained, not renamed PASS.

## Calculation routes and complete domain

reference.py obtains tau by enumerating ALL palette subsets by increasing cardinality and testing set intersections against actual supports. It obtains legality directly from the edited state and original floors. It imports no certificate code. Its universe enumerates support tuples first, then floor tuples.

certificate.py obtains W/C directly from bitwise incidence, predicts primitive updates from the indicator identities, and calculates candidate A/D margins. Candidate legality refuses application outside protected source states. Its universe enumerates ordered products of support/floor pairs. All masks use bit x for palette label x; root slots are ordered and repeats retained. This common encoding is disclosed, not mistaken for independent authorship.

verify.py compares exact identity sets from both routes, requires no duplicate, and checks all 35,792 declared support/floor states (p=2,3,4; m=1,2,3). It visits every syntactic toggle, including floor-forbidden endpoints, and every legal-first/distinct-candidate response in protected initial states. It applies every adjacent palette/root transposition. Pure support computations are memoized to avoid recomputation across different floor tuples; no state or floor identity is removed or sampled.

The complete primary domain has at most three roots and cannot exercise tau=4-to-5 exits. The original five-label upper-bound controls supply those separately, alongside the specified A12.4 fixed-candidate controls, original A12.5 states/endpoints, domain/floor/shadow diagnostics, and collective n=2,...,8 cubes with every subset, edge and Mobius coefficient. Original A12.5 fixtures are parsed from the immutable original proof and checked against the code's explicit transcription; the consolidated source is independently tested for equality with those originals.

## Evidence interpretation

primary.json/reproduction.json report exact domain counts, obligation counters, complete identity-set equality and canonical digests, fixtures, all finite collective chi/coefficient arrays, and rejecting outcomes. Digests do not purport to retain raw per-state output. A failed assertion records its first context and traceback; an externally interrupted command leaves an INCOMPLETE checkpoint and/or platform failure, never a legitimate PASS.

context.json records the input commit, Python/platform, run/attempt/job key and source SHA-256 map. jobs_snapshot.json records actual numeric job IDs but is taken BEFORE evidence publication and job termination, so it is not a final success snapshot. Terminal job/run conclusions and immutable evidence publication are reconciled after the run. Small raw outputs and command logs are automatically committed on a unique evidence-only branch rooted at the input source; the workflow does not move the active research branch or close issue #104. The run's complete platform log remains accessible through GitHub Actions.

Historical RED records: run 37500570046 exposed failure masking by tee and did not execute the absent full verifier; evidence c008c2679ce4c0f6747ca10ec0279a754c551820. Repaired RED run 37500792495 stopped at the nine intended contract failures, with later scientific stages skipped; evidence 89f956ff96e514092000b785faac1c7414f5f3d3. Both are failures, not mathematical counterexamples or successful campaigns.
