# Protein P8B — Authoritative Recovered Topology-Gated Controller Result

**Decision:** `NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION`

**Authoritative launch head:** `14a37025b6869b46a79dd5b016aee9889aa7ba4c`  
**Frozen premeasurement head:** `a85a50c9f9ccdc95871afb653a5200da3ce01007`  
**GitHub Actions run:** `35361130812` — SUCCESS  
**Job:** `105652373518`  
**Artifact:** `10556959039`, `protein-p8b-authoritative-measurement`  
**Artifact SHA-256:** `dccab3bb0b261c815f203d62ae1c7c5b5e000dedb8de22b8ded0e73d2f86be6e`

All internal files listed in `SHA256SUMS.txt` independently matched the extracted artifact bytes.

## Question tested

P8B prospectively tested whether the coordinate-effective historical controller recovered in P8 adds transferable native-blind preorganization when translated onto the validated P6 canonical peptide backbone, and specifically whether its state-dependent topology gate outperforms information-matched nonadaptive schedules using the same force family.

The frozen comparison contained four arms:

1. `recovered_state_gate`
2. `fixed_step99_lockin`
3. `static_lockin`
4. `compaction_only`

Targets were `1VII`, `1L2Y`, and `1UAO`, with six matched seeds each: 72 trajectories total.

## Primary pooled result

Mean final fixed-budget top-K long-range native-contact precision:

| arm | pooled mean precision |
|---|---:|
| recovered state gate | **0.22530864197530864** |
| fixed step-99 LockIn | **0.22530864197530864** |
| static LockIn | 0.19814814814814816 |
| compaction only | 0.2160493827160494 |

The recovered state gate therefore does **not** have the highest pooled primary mean because it ties the fixed-time control exactly.

## Candidate vs fixed step-99 LockIn

Across all 18 matched target/seed pairs:

- mean precision delta: `0.0`
- median delta: `0.0`
- wins: `0/18`
- ties: `18/18`
- raw exact paired sign-flip p: `1.0`
- Holm-adjusted p: `1.0`

Target-wise mean deltas are exactly zero for `1VII`, `1L2Y`, and `1UAO`.

This is the most direct falsifier of state-gating value under the frozen experiment: the recovered controller does not outperform the earliest fixed-time schedule using the same force family.

## Candidate vs static LockIn

Across 18 matched pairs:

- mean precision delta: `+0.027160493827160494`
- median delta: `0.0`
- wins: `5/18`
- ties: `13/18`
- raw exact p: `0.0625`
- Holm-adjusted p: `0.1875`

Target-wise mean deltas:

- 1VII: `+0.06481481481481481`
- 1L2Y: `+0.016666666666666666`
- 1UAO: `0.0`

## Candidate vs compaction only

Across 18 matched pairs:

- mean precision delta: `+0.009259259259259259`
- median delta: `0.0`
- wins: `2/18`
- ties: `16/18`
- raw exact p: `0.5`
- Holm-adjusted p: `1.0`

Target-wise mean deltas:

- 1VII: `+0.027777777777777776`
- 1L2Y: `0.0`
- 1UAO: `0.0`

## Candidate improvement from starting state

Mean candidate primary precision:

| target | start | final |
|---|---:|---:|
| 1VII | 0.25 | 0.09259259259259259 |
| 1L2Y | 0.21666666666666667 | 0.11666666666666667 |
| 1UAO | 0.26666666666666666 | 0.4666666666666667 |

The candidate improves on 1UAO but becomes worse on 1VII and 1L2Y. The frozen every-target improvement condition therefore fails.

## Anti-collapse gate

Median final candidate Rg/native-Rg:

- 1VII: `0.5361237329981463` — FAIL
- 1L2Y: `0.4605802685933045` — FAIL
- 1UAO: `0.6406059147236696` — FAIL

The frozen admissible interval was `[0.75, 1.25]`.

All three targets therefore fail the anti-collapse sanity gate.

## Controller-use condition

This condition **passes**.

Every one of the 18 candidate trajectories entered LockIn and activated the recovered contact/electrostatic force pair.

- all 1VII seeds transitioned at optimizer index `99`;
- all 1L2Y seeds transitioned at optimizer index `99`;
- 1UAO transitioned at indices `99, 113, 100, 111, 119, 99` across seeds 0–5.

Thus this is not a failure caused by the recovered gate never being exercised.

## Frozen acceptance predicates

| condition | result |
|---|---|
| complete unique 72-run matrix | PASS |
| candidate highest pooled mean primary precision | **FAIL** |
| candidate beats every control on every target | **FAIL** |
| all three Holm-adjusted p < 0.05 | **FAIL** |
| candidate improves from start on every target | **FAIL** |
| all candidate trajectories exercise LockIn | PASS |
| candidate Rg ratio gate on every target | **FAIL** |
| canonical covalent geometry preserved | PASS |
| all runs numerically healthy | PASS |
| native-information firewall passed | PASS |
| historical source integrity and proxy checks passed | PASS |

Therefore the preregistered decision is necessarily:

```text
NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION
```

## Independent verification

The outcome-blind verifier was frozen and CI-certified before authoritative result exposure:

- verifier test-freeze commit: `1c04499c33cee2aa8bfcb333dce9bd0895e91ded`
- verifier implementation commit: `7f04a23ad5c3ac15b4909d9fb40b426ff92584df`
- verifier workflow head: `a760e1455a4f01441e213875e053536ebbba0ca0`
- verifier run: `35366692881`
- verifier job: `105670770520`
- verifier result: `4/4 tests passed`

The raw authoritative `p8b_results.csv` was then independently recomputed without relying on `p8b_acceptance.json`. The pooled means, all three matched comparisons, exact sign-flip p-values, Holm correction, start-to-final condition, controller-use requirement, Rg gate, geometry/numerical-health conditions, and final NO-GO all match the generated packet.

## Scientific consequence

P8 remains important as a source-forensics correction: the historical Patch-622/624 lineage did contain a materially distinct coordinate-effective mechanism that P7's broader contact-only generalization had missed.

P8B now answers the next prospective question: when that recovered mechanism is transferred onto a physically valid backbone and tested against same-force nonadaptive controls, the recovered **state-dependent topology gate does not earn a transferable preorganization claim**.

Most notably, its primary outcome is exactly tied with the fixed step-99 schedule across all 18 matched observations.

This closes the recovered coordinate-effective topology-gated controller mechanism under the current preregistered translation.

Do not rescue it by post-exposure coefficient tuning, changing the 8/100/50 thresholds, extending runs, changing targets/seeds, replacing the historical proxy with true persistent homology, or selecting alternate endpoints. Any such study is a new hypothesis and requires a new preregistration.
