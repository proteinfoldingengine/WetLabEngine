# v15.17 — Retained-motion closure / record identity

**Executed conditional simulation extension, not a new physical-law gate.**

This extends v15.16's static recoverable-observable map to ask whether existing
finite motions descend to a FIXED retained algebra. Earlier files and physical
assumptions remain unchanged. No motion is fitted or replaced to secure closure.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_motion.py test_replay.py
python retained_motion.py --out outputs
python replay.py --out outputs
# Optional 24-second H.264 video; FFmpeg is separately required.
python replay.py --out outputs --video
```

The standalone `outputs/retained_motion.html` contains the 96 motion/mask cases
and 65 computed diagnostic rotation frames. It makes no external requests.
`verification.json` and `replay_data.json` contain the full numerical ledger.
The source includes a movie renderer, not a precommitted MP4 or a live website.
The portable conversation ZIP includes generated media and actual local evidence.

## Fixed-algebra descent: exact conditional theorem

Let A be the supplied finite-dimensional retained block algebra, E its
trace-preserving conditional expectation, and C_U(X)=UXU† the supplied unitary
conjugation. We ask whether the retained input E(rho) alone determines the
retained output of the UNPRUNED motion, E(C_U(rho)), for every density operator.

The exact criterion is

    E C_U = E C_U E, equivalently E C_U (I-E)=0.

Necessity follows because discarded directions cannot affect any function of
E(rho). Every Hermitian discarded direction can be embedded in a sufficiently
small positive perturbation of I/d, so the density-matrix statement spans the
operator statement. Sufficiency follows by taking the induced map on A to be
E C_U restricted to A.

The adjoint identity gives (I-E) C_(U†) E=0: U† A U is contained in A.
Both have the same finite dimension, hence U† A U=A. Conversely, if U normalizes
A, its Hilbert-Schmidt-unitary action preserves both A and its orthogonal
complement, so E commutes with C_U and the criterion holds.

Thus, for the supplied finite unitary case,

    exact fixed-algebra descent <=> U A U† = A.

The code checks the full discarded-to-retained superoperator block and,
independently, whether the transformed central projectors permute the original
central projectors. Numerical errors do not replace the finite proof above.

### Algebra preservation is not fixed-record preservation

A normalizing unitary may permute equal-size central sectors. It is a reversible
algebra automorphism but does not fix each named record projector. Fixing all
records requires U P_s U†=P_s for each s. Such within-block motion can still change
the quantum state nontrivially.

For a continuous one-parameter group starting at identity, normalization for
EVERY extent forces every central projector to remain fixed: a continuous path
cannot change a finite permutation. Equivalently [H,P_s]=0. A finite sector-swap
endpoint can normalize A even though the intermediate rotations do not.

## Three processes that must remain distinct

1. E C_U(rho): unpruned motion followed by a fixed reduction.
2. E C_U E(rho): actual pruning first, then motion and final fixed inspection.
3. E_U C_U(rho), where P'_s=U P_s U†: inspection in a transported algebra.

Process 2 is always a valid CPTP process. Failure of fixed-algebra descent does
NOT mean that unitary motion after actual pruning is forbidden. It means process
1 cannot be reproduced from only E(rho). Two inputs with equal retained states
stay equal under process 2; the simulator does not resurrect lost information.

Process 3 has the exact intertwiner P'_s U=U P_s, hence

    E_U C_U = C_U E.

Transporting the retained algebra therefore preserves its content covariantly
for any supplied U. This is a different description, not a repair of a failed
fixed-algebra hypothesis or a physical law selecting transport.

A separate two-sector control compares E C_(U^2)(rho) with E C_U E C_U(rho).
Their trace distance is 0.5: inserting another projection changes the operation.
A display checkpoint must not silently become an extra physical pruning event.

## Existing finite operations and numerical outcome

The panel reuses the earlier pre-time finite unitary, A1, A2, B1, and B2 evaluated
at its two supplied controller values. These matrices are tested as candidate
motions relative to the completed instrument's input-coordinate reductions.
This does NOT reclassify their earlier circuit execution as physically invalid.
The two B2 controller values are explicit alternatives, not actualities derived
here. Every one of the 16 masks is included: 96 combinations.

Local classification: 17 are closed and fix record sectors; 79 are not closed on
the chosen fixed algebra. Separate synthetic controls demonstrate within-block
motion, closed sector permutation, nonclosed mixing, and trivial central phases.
Every nonclosed case carries explicit valid input states with equal E(rho) but
distinct E(C_U(rho)). The smallest measured counterfactual output separation
among the 79 cases is approximately 0.07138. All 96 transported-algebra
intertwiners pass, with maximum error about 7.13e-15.

In the displayed phase-pair control, initial retained distance is about 1.60e-15;
motion without initial pruning gives distance approximately 1; actually pruning
first leaves distance about 8.36e-16. This is a comparison of different operations,
not evidence that the discarded distinction was recovered.

## Effective continuous action, not just generator counts

For v15.16's A=direct_sum_(2^k) M_(2^(4-k)), the Hermitian generator dimension is
256/2^k. Its 2^k central generators act trivially on A. Therefore the dimension of
the effective inner automorphism action, with fixed record identities, is

    256/2^k - 2^k = 255, 126, 60, 24, 0.

The earlier v11.5 count of generators INCLUDING their center is not contradicted.
These are different counts. None is entropy, elapsed time, or a newly derived
clock calibration. Zero effective continuous inner action on the final abelian
algebra does not exclude discrete record permutations, other supplied dynamics,
or further physical degrees of freedom. It is not a claim that a classical world
cannot change.

## Evidence and scope

The model preserves the v15.16 source blob
`0a01d2eea4f0114b119fbb7beaf4619775c0f9f6` and nested earlier sources exactly.
Base: `4f282b70dcda6713db4bf884523870c624fa4c76`.

Twenty-six model tests failed for the intended absent-implementation reason
before implementation; six presentation tests likewise failed before their layer.
All 32 new and 170 selected prior checks passed locally (202 total), in separate
processes to isolate versioned imports. Identity assertions generally use 1e-11;
full-superoperator classification uses 1e-10. Nonclosed cases require positive
collision separation, not merely a large diagnostic norm. No tolerance was tuned
after observing a failure.

Browser checks used Chromium/Playwright `set_content`: all 96 case selectors,
three diagnostic presets, no external requests/JavaScript errors, and no overflow
at widths 1280/820/390. Native Safari/iPad attachment behavior is untested. The
24-second 1280x720 H.264 movie was rendered, visually inspected and fully decoded.
Local Python 3.13.5, NumPy 2.3.5, Matplotlib 3.10.8. The PR records the actual
exact-head Actions result separately; CI does not render video or test a browser.
No full-repository regression, independent peer review or empirical validation
is claimed. Code and theorem received an inline self-review only.

This is standard finite operator-algebra mathematics used to interrogate the
existing simulator. For the broader observable-based viewpoint, see Bény, Kempf
and Kribs, *Quantum Error Correction of Observables*, arXiv:0705.1574 (2007).
That reference does not establish this program's physical interpretation.

Pre-time motion remains reversible relational change, not elapsed time. RAS and
RCR remain explicit and separate. No actual record, physical motion selector,
entropy-production objective, first-collapse law, duration or gravity is derived.
No new fundamental physical axiom is adopted. Pillar 3 remains OPEN.
