# v15.14 — Record-dependent event simulation

**Executed conditional demonstrator, not a new physical-law closure.**

Extends v15.13's independent-event model with one explicit classical record-read
rule: B2 reads the already-realized A1 bit. The inherited local requirements are
A1 before A2 and B1 before B2. Their graph plus A1 before B2 admits five schedules,
not six. All sixteen supplied record assignments are tested: 80 valid runs.

## Run and view

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_adaptive.py test_replay.py
python replay.py --out outputs
# Optional MP4: FFmpeg must be on PATH.
python replay.py --out outputs --video
```

`outputs/record_dependencies.html` is a standalone computed replay. Use
**Show blocked example** to realize B1 and attempt B2 while A1 is still missing.
The blocked attempt changes no state. Then realize A1: A2 and B2 are both ready.
Use the event buttons to choose execution order, not physical outcomes. The
sixteen outcome scripts are explicit inputs. Each successful step displays the
computed retained state, joint branch weight and available records.

`outputs/replay_data.json` exports complex density matrices, record stores,
readiness metadata and joint weights for all 80 runs. `verification.json` contains
fresh checks. The optional 24-second MP4 illustrates the blocked/read-enabled
path. Media playback duration, checkpoint count and diagram layout are not
physical time, global simultaneity or geometry. Generated media is not committed
as source. The portable conversation bundle includes the video, HTML and logs.

## Exact supplied extension

On the existing four-qubit carrier, the B2 unitary is

    U_B2(a) = exp(-i s(a) Y_B2) U_B2_old,
    s(0) = +0.6, s(1) = -0.6.

This is a predeclared illustrative controller, not a fitted motion/source law.
Its local instrument is K_b(a)=P_(B2,b) U_B2(a), and the two branch operators obey
sum_b K_b(a)^dagger K_b(a)=I for either already-realized value a. The controller
acts on B's second qubit and preserves all earlier record projectors. The carrier,
RAS, RCR, motion generators and classical record wire remain supplied.

The instrument resolver accepts ONLY its declared realized read keys. It has no
argument for the full future outcome script. An outcome still has to be supplied
explicitly after readiness is checked. Premature execution, repeated records,
nonbinary values and undeclared read keys are rejected. Previous states and record
stores are immutable. This is an API and mathematical-model property, not a claim
that malicious callers cannot fabricate input objects.

## Conditional partial-order result

At a fixed realized record set, independent remaining operations commute. In
particular, after A1 is realized, A2 and adaptive B2 commute at the shared value
of A1. Swapping permissible incomparable events therefore preserves

    tau = K_history rho K_history^dagger,
    p = Tr(tau), and rho_retained = tau / p.

The argument requires the same realized control values and positive branch mass.
The order constraints come from the DECLARED dependency interface. This is not an
unconditional derivation of physical causality or the onset of time. Classical
record feed-forward is standard quantum-instrument machinery; coherent-control
or deferred-measurement implementations of related operations are not ruled out.

References for the mathematical machinery, not validation of the physical ontology:
https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/general-measurements

## Numerical result and sensitivity control

The local 80-run reconstruction gives a largest same-record-set trace distance
of approximately 6.25e-16 and joint-weight difference 1.11e-16. All 19 inadmissible
orders among the 24 event permutations are rejected. The five valid orders remain
interchangeable only at matching completed-event sets.

A rejected control guesses A1=0 before A1 exists. Every fully measured normalized
basis state still matches its correctly executed counterpart to roundoff, but a
joint branch weight differs by as much as 0.26106. Guessing A1=1 similarly leaves
final basis states unchanged while a joint weight differs by up to 0.04406.
Neither guessed control is adopted. These are counterexamples to using only a
final normalized state as the test of correct record-dependent execution.

`docs/RESULTS.json` is a measured local snapshot, not a formal physical certificate.
The executable tests enforce scientific thresholds independently of that snapshot.

## Evidence and preservation

The vendored v15.13 core is byte-identical to Git blob
`95d0303d617422d74e61ae017f0354233ec9454b`, from base commit
`3fd5aa06ddc2970aa5662dfc57afbfcbe4b3c7e5`. Earlier repository files are not changed.

Actual local RED logs contain 24 missing-model assertions and six missing-replay
assertions before their implementations. All 30 new tests then passed, together
with 27 v15.13, 30 v15.12 and 20 v15.11 tests: 107 checks. These are selected
regressions, not a full-repository test run or independent peer review.

The HTML bytes were tested in Chromium using `page.set_content` because this
browser's policy blocks direct `file:` navigation. Tests covered all 80 final
views, rejection without state mutation, backward replay, no external requests or
JavaScript errors, and widths 1280/820/390. Native iPad/Safari attachment behavior
was not tested. The MP4 was rendered, inspected and fully decoded locally.
CI, when run, verifies tests/exports/compilation; it does not repeat browser or
movie verification. Consult the draft PR for the actual exact-head CI conclusion.

No new fundamental physical axiom is accepted. The added controller is an explicit
simulation input. No automatic choice, entropy selector, clock calibration or
gravity fit is inserted. First-collapse semantics, physical entropy production,
metric duration and gravity remain unresolved. Pillar 3 remains OPEN.
