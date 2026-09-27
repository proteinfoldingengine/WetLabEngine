# v15.81 results — component interference carries the response; finite window fails

Primary verdict: **MATCHED_COMPONENT_INTERFERENCE_RESPONSE_CONFIRMED**.
Secondary verdict: **FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED**.
All validity controls passed. GREEN CI passed three tests because the tests
accept valid scientific NOs; the finite-window verdict remains NO.
No threshold, source strength, depth, state or scientific criterion changed.
No implementation repair was required after the first scientific run.

## Matched physical source mechanism

For the frozen P=ZII and Q=XXI components, the five CPTP-admissible arms
kept diagonal component rates .5,.5 and coefficient-matrix trace 1 fixed.
Both components remained active: P affected 18 hidden probes and Q affected 12,
with nonzero component-output HS norm 2. Their separate retained leakages
were at roundoff. Removing their cross term therefore did not deactivate
the nominal components.

All 60 generator cases passed. The incoherent arm lambda=0 had retained/Q/E
rank 0. Every nonzero lambda had retained rank 12 and Q/E rank 6, stable at
all three preregistered thresholds. The signal lay on edges (1,2) and (2,0),
rank 3 each; source edge (0,1) was null. At a common original state, the
complete Q and E maps scaled with lambda, with reported scaling error zero.

| Cross coefficient | Retained norm | Q norm | Retained rank | Q/E rank |
|---|---:|---:|---:|---:|
| -1 or +1 | 3.4641016151 | 11.3137084990 | 12 | 6 / 6 |
| -.5 or +.5 | 1.7320508076 | 5.6568542495 | 12 | 6 / 6 |
| 0 | 4.808e-17 | 0 | 0 | 0 / 0 |

At absolute lambda 1, E norms ranged 45.2991–70.3086 across the references;
half-strength interference halved these norms. Thus, within this explicit
physical family, the source-component cross term carries the hidden-to-
retained rotational response. Mere activation of the two components with
the same diagonal rates is insufficient.

This is interference relative to the specified source decomposition, not a
basis-independent Lindblad coherence measure. A jump-basis change can
diagonalize the coefficient matrix without changing the channel. The arms
match component rates, not total generator norm. The cross contribution by
itself is not claimed to be a physical generator.

## Finite updates: exact transfer, but one proper-polar domain exit

The exact retained transfer factor b(lambda,u)=exp(-u)sinh(lambda u) agreed
with the finite channel to maximum entry error 1.388e-16. Independent PTM
exponentiation agreed with the mixture channel within 5.294e-16, and the
all-matrix-unit composition checks within 6.662e-16. These identities survived
all frozen strengths. All 35 distinct channels used for measurement and
composition passed CP/TP checks. All finite centers and hidden-perturbed
states passed positivity, trace and Hermiticity controls.

Of 240 finite-output cases,239 passed the full finite-window conditions.
The single failure was candidate 46, lambda=-1, depth 8, strength u=.8.
Its connected correlation on edge(0,1) had:

- singular values 0.1524387862,0.0509686286,0.0009280840;
- polar determinant-1.0000000000000002;
- determinant of C reconstructed from the SVD: -7.210837794e-6;
- minimum finite-state eigenvalue over center/probes 0.0668608081;
- retained hidden rank 12, still nonzero.

The endpoint is nonsingular and above the frozen singular-value floor 1e-4,
but its polar factor has improper orientation. It fails the stipulated
proper-polar domain. This is not loss of quantum-state positivity, loss of
CPTP composition, or evidence that retained leakage vanished. Q/E fields
for that case are null, as preregistered; no proper-polar helper was called
outside its domain and no reflection correction was inserted.

All 239 regular cases passed. In the finite incoherent arm, worst retained,
Q and E norms were 8.330e-17,3.846e-16,4.510e-15 respectively, and ranks 0.
The minimum singular value among regular finite cases was 0.00606221.

## Investigation of the NO using the unchanged artifact

The artifact-only audit DOMAIN_EXIT_AUDIT.json records the same case across
its four frozen depths; it introduces no new simulation or gate.

| Strength u | Minimum edge(0,1) singular value | det C | Polar orientation |
|---|---:|---:|---:|
| .1 | .0330366 | +5.235785e-4 | proper |
| .2 | .0249907 | +3.435853e-4 | proper |
| .4 | .0126899 | +1.370179e-4 | proper |
| .8 | .000928084 | -7.210838e-6 | improper |

The sign change and endpoint singular margin are far above the recorded
channel implementation residuals. By continuity of the exact channel and
connected correlations, a singular crossing lies between strengths .4 and .8;
its location was not measured. The exit occurs on the source edge, whose
hidden rotational response was null, illustrating why baseline geometry
and hidden-response leakage must be tracked separately. The finite-window
NO is preserved, not converted into a pass by dropping that edge, changing
the polar convention, or shortening the window.

## Validation and boundaries

Generator decomposition error was 4.441e-16. Retained generator reconstruction
error was 2.776e-17. Analytic geometry reconstruction errors were at most
1.333e-15 for Q and 1.777e-14 for E; Sylvester residual was 1.839e-14.
Minimum channel Choi eigenvalue was-2.264e-15, within the frozen -1e-12
roundoff tolerance for rank-deficient channels. Minimum finite-state
center/probe eigenvalue over all cases was 0.0418252. These controls distinguish
the proper-orientation domain failure from an implementation or CP failure.

The result isolates a physical source term in this specified model; it does
not explain why global consistency selects the components or lambda. It does
not derive gravity, change admissible-world consistency, or establish a
finite natural retained atlas. Historical verdicts remain intact. Genesis
Pin, ordered recoverability and geometry as retained exhaust are unchanged;
no fundamental time, external alignment, heuristic fit or dark-matter
primitive was added. The next finite-atlas claim must address this orientation
boundary rather than assume that CPTP source composition preserves the
proper-polar geometry domain.

## Exact certification evidence

- Certified parent: `f7bf2826e6952dae11ae67d548423911ecf94151`.
- Preregistration/tests with implementation absent: `dfc29c734be6c9da94c37bdb5d24e43b7738d825`.
- Tested scientific implementation: `7f24484160626c85dd05c321f5b7903143a0f378`.
- RED [run 36347764347](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36347764347), job `108700360497`, artifact `10941511136`.
- RED artifact SHA-256: `15adae368cbe214029568fabc687c43bfe01ca4596ea5120958fecc2f9576b23`.
- GREEN [run 36348037094](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36348037094), job `108701126478`, artifact `10941172257`.
- GREEN artifact SHA-256: `74ca328d773c5c3d473b29df7ac6417d860c90445ad10f070d92a56f7099c9b2`.
- Full result JSON SHA-256: `14d1fdac212d7373bddd3f450269a0c39dd0ae0d7937fa9356fe1acc64c646fc`.
- Lossless RESULT.json.gz SHA-256: `6ec462e269a8cfd81b8cbd9312a2b613e8c802434b28dd2b38d3cbce4f37217d`.
- Compressed result Git blob: `aa9a146064e86e806ad4b515e9f3e3d74a30f9ed` (163,186 bytes).

Exact job logs were read. RED setup succeeded and stopped at the intended
missing-implementation assertion, with zero tests executed. Both artifacts
were downloaded and SHA-256 checked. Execution SHAs, frozen source bytes
and GREEN SHA256SUMS were verified. The GREEN artifact JSON was inspected,
including its secondary NO, rather than inferring success from CI color.

The full result is archived losslessly beyond Actions retention. SUMMARY.json
is derived from it; TEST_LOG.txt and SHA256SUMS are copied from the artifact.
The final documentation commit is additive and does not change the tested
scientific implementation. Nothing was merged to main.

## Reproduce

Use Python 3.11 and numpy==2.3.5 at the tested commit, from this folder:

```sh
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > result.json
```

At the additive documentation head:

```sh
gzip -dc RESULT.json.gz > certified-result.json
sha256sum certified-result.json
```
