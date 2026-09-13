# v15.13 — Independent events / partial-order simulation

**Executed conditional demonstration, not a new physical-law closure.**

This extends the v15.12 integrated simulator with two local record chains,
`A1 -> A2` and `B1 -> B2`, on a supplied four-qubit carrier. It enumerates all
six interleavings preserving those two dependencies, for all sixteen supplied
four-bit outcome assignments. No cross-stream clock or total physical order
is supplied. No earlier source or result is overwritten.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_model.py test_replay.py
python replay.py --out outputs
# Optional MP4; FFmpeg must also be installed.
python replay.py --out outputs --video
```

`outputs/independent_events.html` is a standalone browser replay. Select two
execution orders or click one of the nine record-lattice nodes to compare paths
that reach the same completed-event set. It includes all 96 computed runs and
makes no external requests. `outputs/replay_data.json` contains the normalized
complex states, joint weights and event metadata. `outputs/verification.json`
records the fresh numerical checks. The optional movie is a 21-second,
1280x720 H.264 replay. Media duration and coordinates are display conventions.
The portable conversation bundle includes generated outputs and local test logs;
these large generated files are not committed to the source directory.

## What is supplied

The four-qubit carrier, correlated initial state, reversible motion generators,
two local dependency chains, retained-algebra reductions and actual records are
illustrative inputs. The two streams have disjoint operational support even
though their initial state is entangled. No random sampler, maximum-weight
selection, entropy objective, elapsed time or downstream gravity score selects
an actual outcome. RAS and RCR remain distinct supplied ingredients inside each
local event. The replay's checkpoints are AFTER complete declared local events;
it does not assign physical intervals between motion, RAS and RCR.

Pre-time motion is reversible. The model tests its inverse and never turns a
finite transformation coordinate into a clock. The later local transformations
preserve their earlier records. Local dependency arrows are part of the declared
scenario, not a derivation of a physical causal structure from nothing.

## Why execution order should not select the answer

For supplied outcomes a and b, the independent branch operators have the form

    K_A = k_A tensor I_B
    K_B = I_A tensor k_B.

Thus K_A K_B = K_B K_A, also on entangled input states. For a given completed
record set D, define its unnormalized branch operator output

    tau_D = K_D rho K_D^dagger.

Any two linear extensions of the same finite dependency poset are connected by
adjacent swaps of incomparable events. The operators in each such swap commute.
Consequently tau_D, its trace (joint branch weight), and tau_D/Tr(tau_D) all agree
at matching completed-event sets. A positive-weight condition is required for
the normalized state. The full-rank supplied fixture gives positive weights for
all sixteen branches.

The nine displayed nodes correspond to prefix counts (0..2, 0..2). They are
record sets, not physical points, equal-time slices or global simultaneity.
Different equal-length prefixes can contain different records; the browser does
NOT present their state difference as a confluence failure.

This is an implementation of the earlier v11.3 conditional independent-event
structure restored in v15.11, not a new theorem about physical time.
For standard measurement/operator notation see IBM Quantum Learning, General
measurements: https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/general-measurements
That mathematical reference does not validate the project's physical ontology.

## Important distinction: conditional factors versus joint weights

Correlated records need not have the same conditional probability in different
contexts. For example, P(A1=1) and P(A1=1 | B1=0) are different questions. The
product of conditional factors along a full schedule is the invariant joint
branch weight, not each displayed conditional factor separately.

Across the executed 96 runs:

- largest same-record-set trace distance: about 1.02e-15;
- largest same-record-set joint-weight difference: about 1.39e-16;
- largest change of an event's conditional weight across contexts: about 0.19168.

Independent operations therefore must not be advertised as statistically
independent outcomes. See `docs/RESULTS.json` and regenerated numerical outputs.

## Sensitivity control

An explicitly labeled rejected control inserts a cross-stream unitary into B1.
The branch operators then no longer commute. In the default supplied `1001`
record assignment, a shared-set trace distance is about 0.35283 and the final
joint-weight spread is about 0.00534. This control is not an adopted interaction,
new physical axiom, or gravitational force. It demonstrates that the test does
not declare every arbitrary ordering interchangeable.

## Verification and boundaries

Local TDD: 23 model assertions failed before model implementation; four replay
assertions failed before replay implementation. Final local verification passed
all 27 new tests plus the 30 v15.12 and 20 v15.11 regression tests. The earlier
six principal source blobs were checked against their archived Git hashes.
Python 3.13.5, NumPy 2.3.5, Matplotlib 3.10.8 were used locally.

Browser checks in Chromium covered all 96 final record views, all nine shared
record sets, comparison rejection for differing record sets, playback controls,
no external requests or JavaScript errors, and tablet/mobile overflow. Native
Safari/iPad attachment handling was not tested. The MP4 was rendered, visually
inspected and fully decoded without reported errors.

The exact-head CI result is recorded on the draft PR, not presumed here. CI runs
27 new tests, the prior 50 tests, compilation and replay generation. It does not
render the video, rerun the browser checks, execute the entire repository test
suite, or constitute independent scientific review.

No first-collapse law, physical entropy production, metric duration, global
simultaneity, physical source law, quantum-carrier origin, gravity or Einstein
correspondence is derived. Pillar 3 remains OPEN. Earlier conditional assumptions
are not promoted into unconditional derivations. No scientific breakthrough is
claimed; this is a stronger integrated demonstrator.

## Files

`event_model.py`: finite state/instrument model, six schedules, all-record audit.
`replay.py`: export, interactive HTML assembly and optional MP4 renderer.
`viewer.html`: browser template; run the exporter to embed computed data.
`test_model.py`: 23 integration and claim-boundary controls.
`test_replay.py`: four export/comparison controls.
`requirements.txt`: pinned local numerical/rendering dependencies.
`docs/PLAN.md`: implementation scope and ontology constraints.
`docs/RESULTS.json`: measured local numerical result, not a physical certificate.
`evidence/`: actual local logs/check scripts in the portable bundle.

Base Git commit: `c1b0582d15e0720e3e01989f7aa195ed89e6a62a`.
