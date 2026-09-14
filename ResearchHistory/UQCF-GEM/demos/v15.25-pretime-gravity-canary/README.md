# v15.25 — Pre-time global-compatibility gravity canary

**Verdict:** `KILLED_BARE_COMPATIBILITY_DOES_NOT_FORCE_GLOBAL_RESPONSE`.

This is the explicit pivot back toward a gravity-before-time signal. It deliberately
operates upstream of pruning, entropy, record selection, calibrated duration,
Newton fitting and GR fitting. The candidate source changes an admissibility
relation, not a quantum state. The first diagnostic Hodge representative looked
promising: it spread across the connected relational complex and produced remote
noncommuting holonomy. A stronger control kills that interpretation, because bare
compatibility also admits an exact one-edge local cancellation. The long-range
field is therefore not forced by the current candidate law.

That negative result is the scientific point of this gate. It prevents a supplied
minimum-norm/Hodge selector from being mistaken for emergent gravity.

## Reproduce

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_canary.py test_replay.py
python pretime_gravity_canary.py --out outputs
python replay.py --out outputs --video
```

FFmpeg is required only for the MP4. The GitHub workflow reruns the full selected
v15.11-v15.25 stack, regenerates numerical and viewing assets, decodes the movie,
and publishes only after all release-asset sizes and SHA-256 digests match.

## 1. Candidate source law

The finite canary uses a supplied 7x7 periodic relational 2-complex. The square
layout is a visualization only, not claimed physical space. Its vertex-edge and
edge-face incidence matrices are B1 and B2, with exact chain closure

    B1 B2 = 0.

The candidate source changes one edge occurrence in one face boundary. Write the
added 1-chain as delta_b. Its induced boundary-of-boundary defect is

    q = B1 delta_b.

This is local: q has support on the two endpoints of the affected incidence and
sums to zero on the closed finite complex. It changes the admissibility equation
rather than acting on a density matrix. No event or outcome is selected.

A complete closed-face multiplicity gives delta_b=B2 f and therefore

    q = B1 B2 f = 0,

which is the exact null control.

## 2. The initially promising diagnostic representative

One canonical *diagnostic* completion is the equal-edge minimum-norm solution

    j_H = -B1^T (B1 B1^T)^+ q,

so that

    B1 j_H + q = 0.

On the L=7 canary, this representative has nonzero support on about 86.7% of
edges and closure residual 2.51e-15. The response is covariant under arbitrary
vertex/edge relabeling and superposes linearly. Translating equivalent sources
leaves the aggregate response invariant to about 2.24e-16.

The source-edge orientation sweep gives the same response norm and approximately
the same remote-shell noncommuting holonomy RMS, 1.403e-2, for all four incidence
orientations. The commuting-axis loop control is about 5e-17 to 6e-17 RMS.

This looked like the desired pre-time pattern: a local admissibility defect,
followed by a distributed response without pruning or a time parameter.

## 3. Holonomy controls

The minimum-norm current is in im(B1^T), hence has zero scalar circulation on
every closed face because B2^T B1^T=0. Edge provenance classes are then mapped
to two noncommuting SU(2) axes. The ordered loop product can be nontrivial even
when the scalar circulation is zero.

For the displayed far face, the SU(2) loop defect at probe epsilon=0.2 is
approximately 2.198e-3, while replacing every edge axis by the same commuting
axis gives approximately 3.85e-19.

The raw face holonomy has a first-order component: doubling small epsilon from
0.01 to 0.02 gives ratio about 2.0. This was an important correction to the
initial expectation of a purely quadratic law. A separate group-commutator
observable removes first-order terms and has ratio about 4.0 under the same
epsilon doubling. Its source-amplitude scaling is likewise quadratic, as expected
for a commutator term. Nothing is fitted to Newton or GR.

## 4. The decisive local-cancellation control

Because the source was defined by q=B1 delta_b, the current

    j_local = -delta_b

is itself an exact solution:

    B1 j_local + q = 0.

It is supported on **one edge only** and has zero remote holonomy. Therefore the
compatibility equation does not require a long-range response. The global Hodge
field is one chosen representative of the solution class, not an emergent fact.

This is a hard failure for the intended gravity canary under bare compatibility.
No amount of attractive visualization or remote holonomy in j_H can override the
existence of this exact local solution.

## 5. Further response nonuniqueness

The solution set contains

    j = j_H + z,   z in ker(B1).

For the L=7 torus the cycle-space freedom has dimension 50. Adding 0.25 times a
closed face cycle keeps the closure residual at approximately 2.52e-15 while
changing the displayed remote holonomy by approximately 0.198.

The minimum-norm representative also depends on the edge inner product. Replacing
the equal edge weights by a fixed positive ramp from 0.75 to 1.25 changes the
response vector by norm approximately 0.108 while preserving closure. The current
frozen ontology has not selected either the cycle component or this edge metric.

These are not small numerical ambiguities; they are structural nonuniqueness.

## 6. What survives the kill

Several useful exact facts survive:

- the source law acts on an admissibility relation rather than on the state;
- B1 B2=0 provides a clean higher-incidence null control;
- equivalent microscopic defects differing by a closed face have the same q;
- the equal-edge Hodge representative is covariant and global;
- noncommuting relational transports can convert that representative into remote
  holonomy while the commuting control vanishes;
- the response equations use no pruning, entropy or physical-time primitive.

But these facts do **not** amount to a signal of gravity because globality is not
forced. The gate therefore records

    global_compatibility_signal = false
    signal_of_life = false
    gravity_canary_certified = false

for this candidate mechanism.

## 7. Direct next target

The next gravity-facing gate should not return to retention bookkeeping. It must
attack exactly the missing selector. There are two lawful possibilities to test:

1. derive a response inner product / Hodge representative from already-existing
   pre-time quantum relational structure (for example a frozen local Gram/support
   object) without using pruning, entropy, duration, Newton or GR; or
2. replace the source-to-admissibility law by one whose admissible compensations
   have a quotient-invariant nonlocal observable, so no arbitrary cycle selector
   is needed.

A candidate that merely declares minimum norm, smoothness, radiality, inverse
square behavior, or GR agreement is disallowed. A candidate that forbids the
local solution only by hand is also disallowed.

## 8. Provenance and claim boundary

Parent research head: `4c29601f79128d354de14d564f4c17a26a414fb8`
(v15.24, which closed the retention/composition branch). Tests were written first;
the local model RED had 14 missing-implementation failures, followed by one
scientifically informative scaling failure that was investigated rather than
tuned away. Presentation RED had six missing-presentation failures. The final
local suite currently contains 28 tests.

The visualization parameter epsilon is a dimensionless probe strength, not time.
The supplied toroidal complex is a canary arena, not derived physical geometry.
The X/Y edge-axis assignment is a supplied provenance-class control, not a new
particle or force. The equal-edge Hodge representative is explicitly marked as
supplied diagnostic structure.

No dark matter, dark energy, new particle, actual outcome, entropy-production law,
physical clock, Newtonian potential, Einstein equation, or physical gravity law is
derived. No breakthrough claim is made. Pillar 3 remains OPEN.
