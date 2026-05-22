# V923 Full-Stack Proof Report: Minimal Source-Role Closure

## Executive result

This full-stack proof reproduces the V919–V922 closure result from the frozen V921 blind cohort.

```text
E_OSC closes basin geometry.
Endpoint/path observables define a quotient taxonomy.
Observable-only closure fails.
Binary source-role collapse fails.
A ternary source-role primitive closes exact source legitimacy.
The older four-state source-family/source-origin label is over-complete.
```

## Minimal primitive

```text
source_active_role
source_basin_eligible_nonactive_role
source_rejected_or_broken_role
```

Mapping from the former four source families:

```text
active_source             -> source_active_role
passive_source            -> source_basin_eligible_nonactive_role
structured_source         -> source_basin_eligible_nonactive_role
rejected_or_broken_source -> source_rejected_or_broken_role
```

## Dataset

```text
input rows: 840
source families: active_source, passive_source, rejected_or_broken_source, structured_source
true classes: 7
observable quotient column: v921_observable_quotient
```

## Lift ladder

| Lift | Symbol count | Accuracy | False cases | Collision groups | Collision rows |
|---|---:|---:|---:|---:|---:|
| Observable quotient only | 1 | 0.628571 | 312 | 3 | 662 |
| Best binary lift | 2 | 0.916667 | 70 | 2 | 306 |
| Ternary source-role primitive | 3 | 1.000000 | 0 | 0 | 0 |
| Full four-family source lift | 4 | 1.000000 | 0 | 0 | 0 |

## Exhaustive partition result

The script exhaustively enumerates all canonical partitions of the four source families into 1, 2, 3, and 4 symbols. The best possible binary partition still fails; a ternary partition is the first exact closure.

```text
minimal exact source-symbol count: 3
best binary accuracy: 0.916667
best binary false cases: 70
ternary accuracy: 1.000000
ternary false cases: 0
```

## Stress behavior

Random role corruption degrades the taxonomy smoothly, as expected for a necessary information-bearing primitive.

| Noise p | Mean accuracy | Min accuracy | Mean false cases |
|---:|---:|---:|---:|
| 0.001 | 0.999101 | 0.995238 | 0.755 |
| 0.005 | 0.995339 | 0.988095 | 3.915 |
| 0.010 | 0.991137 | 0.978571 | 7.445 |
| 0.020 | 0.982440 | 0.971429 | 14.750 |
| 0.050 | 0.954107 | 0.933333 | 38.550 |
| 0.100 | 0.909083 | 0.884524 | 76.370 |
| 0.200 | 0.820381 | 0.790476 | 150.880 |


Worst targeted role flip:

```text
source_basin_eligible_nonactive_role -> source_active_role
affected rows: 360
accuracy: 0.571429
false cases: 360
```

## Scientific interpretation

The result shows that the signed-coherence basin is not enough to certify source legitimacy. Endpoint/path observables collapse multiple source histories into a quotient. A ternary source-role primitive is the minimal exact lift in this branch.

The ternary primitive does not add a new physical-time claim. It is a minimal information role needed to distinguish active repair, basin-eligible nonactive occupancy, and rejected/broken origin.

## Claim boundary

YES:

- E_OSC closes basin geometry in this tested branch.
- Endpoint/path observables define a quotient taxonomy.
- Observable-only closure fails.
- Binary source-role lift fails.
- Ternary source-role primitive is necessary and sufficient in this branch.
- Four-state source-family/source-origin labeling is over-complete for exact closure here.

NO:

- No 1/f ledger claim is used or certified here.
- No physical-time claim is made.
- No CMB or black-hole claim is made.
- No unique repair-channel law is claimed.
- No GR, Einstein equations, physical spacetime curvature, or continuum closure is claimed.

## Reproduction

Run:

```bash
python v923_full_stack_source_role_closure_proof.py
```

The script writes all reproduced proof artifacts to:

```text
/mnt/data/v923_full_stack_source_role_closure_proof_run/
```
