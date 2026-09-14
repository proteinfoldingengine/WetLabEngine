# v15.19 — Linear prediction module versus invariant observable algebra

**Executed conditional simulation extension. No new physical law is claimed.**

v15.18 required a multiplication-closed observable algebra. This extension removes
that requirement, keeps the same motions and target observables, and finds their
smallest invariant real Hermitian linear space. These expectation coordinates are
not assumed to form a quantum density matrix or a physical pruning channel.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_linear.py test_replay.py
python linear_module.py --out outputs
python replay.py --out outputs
# Optional 24-second H.264 movie; FFmpeg must be installed separately.
python replay.py --out outputs --video
```

`outputs/linear_prediction.html` is a standalone inspector for all 112 cases.
Choose a motion family and original pinching mask. The plot compares direct
quantum-state evolution with predictions from the computed linear coordinates.
The full input and original observables are unchanged. Checkpoints represent
finite diagnostic words, not physical time, pruning events, or a realized history.
Both B2 control alternatives remain supplied alternatives in the family, not two
simultaneously actual records.

`outputs/verification.json` contains every dimension, rank-gap record, residual,
and control. `replay_data.json` includes 1,456 plotted checkpoints. Two example
basis matrices and the original input-basis transform are in `example_modules.npz`.
The portable ZIP includes generated HTML, video, numerical data and local logs.

## What minimum is computed?

Let A be the earlier retained algebra, A_h its Hermitian part, and G the same
supplied unitary family used in v15.18. Define

    V_min = span_R { U_w† A U_w : A in A_h, w a finite word in G and G† }.

This space contains the identity and is invariant under every supplied
conjugation and its inverse. It need not be closed under products. Its dimension
is a real Hermitian dimension INCLUDING the identity. The number of independent
unknown coordinates for normalized states is one smaller.

Minimality is straightforward: every invariant real linear space containing the
seed must contain each orbit element, hence their span. Conversely the orbit
span is invariant because composing with a generator merely changes the word.
No model of physical time or entropy is used in this definition.

Choose an orthonormal Hermitian basis H_mu for the complete operator space. Let
Q have orthonormal columns spanning V_min in these coordinates, and let T_U be
the real orthogonal matrix representing A -> U† A U. Then

    T_U Q = Q R_U,      R_U = Q^T T_U Q.

For a quantum input rho, the feature vector is

    z_a = Tr(rho O_a),  where O_a = sum_mu Q_(mu,a) H_mu.

After rho -> U rho U†, the exact reduced-coordinate update is

    z' = R_U^T z.

Any original target observable is a linear combination of the O_a. Its prediction
therefore follows exactly from z for all input states and all finite motion words.
The 12-operation tests are numerical witnesses of that identity, not a proof
that finitely sampled trajectories alone establish the all-word theorem.

The coordinates must have been retained before any information reduction.
Calculating a larger feature vector from an already-pruned state does not recover
lost input distinctions.

## Results

The seven families and sixteen masks match the earlier 112-case algebra audit.
In 92 cases the linear module is strictly smaller than the invariant algebra.
Starting from the fully pinched, 16-direction diagonal target algebra:

| Supplied finite motion family | Initial target dimension | Linear module | Invariant algebra |
|---|---:|---:|---:|
| B1 | 16 | 40 | 64 |
| B2, controller 0 | 16 | 40 | 64 |
| B2, controller 1 | 16 | 40 | 64 |
| A1 | 16 | 44 | 128 |
| A2 | 16 | 44 | 128 |
| Existing pre-time motion | 16 | 126 | 256 |
| All six supplied motions | 16 | 255 | 256 |

Thus multiplication closure was a genuine extra requirement. Single-motion
prediction can use substantially fewer directions. The whole-family requirement
removes almost all of that saving. This is not a universal assertion about all
reduced descriptions, all observables, or physical motion laws.

Maximum all-target prediction error over the executed checks: 1.4495046741437895e-14.
Maximum invariant-subspace residual: 3.3299289550099546e-14.
Both are below the predeclared 1e-9 verification threshold. These dimensions
are NOT entropy, elapsed time, clock ticks, or physical qubit counts.

## The one missing whole-family coordinate

Define Gamma = Y tensor Y tensor Y tensor Y on the original four-qubit carrier.
Every Pauli term in the frozen generators has either zero or two factors that
anticommute with Gamma. Therefore each generator commutes with Gamma, as do its
exponentials and products. This is an exact algebraic explanation of a symmetry
already present in the supplied toy operations, not a new assumption.

The numerical commutator maximum across all six original motions is 4.55e-15.
For the fully pinched seed, the computed 255-dimensional module is

    V_min = { A Hermitian : Tr(Gamma A) = 0 }.

The identity belongs to this hyperplane because Tr(Gamma)=0. The module's
orthogonal projector matches I - |Gamma/4><Gamma/4| with residual 9.09e-14.
The Krylov construction supplies the matching 255-dimensional lower bound;
conservation and seed orthogonality supply the upper bound. No operator is removed
merely because its expectation happens to be small in one chosen input.

The two valid states rho_+ = (I+Gamma)/16 and rho_- = (I-Gamma)/16 are supported
on opposite parity sectors and have trace distance 1. Nevertheless their target
record probabilities and all module features agree. The missing coordinate is
conserved and irrelevant to the chosen predictions.

The whole-family module has dimension 255 for the fourteen masks pinching any
of A1/A2/B1. For masks 0000 and 0001, the target seed also probes the parity
direction and the module is full, dimension 256. This mask statement is part
of the numerical fixed-instrument audit, not a new physical record-selection law.

## A smaller prediction vector is not automatically a smaller quantum world

The Hilbert-Schmidt projection onto the 255-dimensional hyperplane is

    Pi(rho) = rho - Tr(Gamma rho) Gamma / 16.

Take rho to be the pure product of four +Y eigenstates. It is positive and has
Gamma eigenvalue +1. Pi(rho) has minimum eigenvalue -1/16, confirmed numerically
as -0.06250000000000196. Consequently THIS orthogonal projection is not even
positive and cannot be a physical CPTP pruning operation.

The simpler qubit space span{I,X,Z} gives another control: its orthogonal
projection has an unnormalized Choi eigenvalue -1/2. It is not completely positive.
The product XZ also leaves the linear space. These controls distinguish linear
prediction closure from both associative closure and quantum-channel admissibility.

This does not prove that no different physical realization or encoding of these
predictions exists. It says the coordinate projection being used here is not one.
No replacement RAS, RCR or physical collapse mechanism is supplied.

## Numerical methods and conditioning

The constants were fixed before the computations:

- singular values <= 1e-11: numerical null;
- singular values >= 1e-8: retained;
- values between: AmbiguousRank, no rank adjudication from that route;
- invariant-subspace and prediction residual ceiling: 1e-9.

A direct block-Krylov implementation passes the generic small controls but enters
the forbidden rank gap in some pre-time cases, due to repeatedly normalizing
weak residual directions. The first implementation correctly stopped rather than
silently changing the tolerance. Logs retain those failures.

For each single unitary the final algorithm uses its Schur eigenspaces. On an
adjoint eigenphase sector the conjugation is scalar, so the cyclic dimension is
the rank of the seed projected into that sector. Conjugate sectors are paired
explicitly into real Hermitian directions. This avoids subtracting nearly aligned
vectors to infer the second real direction. The real-basis construction is
cross-checked against complex-sector rank sums; both use the same spectral
partition, so they are not fully independent software implementations.

The smallest retained spectral seed singular value is 7.3974e-8; the largest
spectral null value is 8.62e-15. The minimum distinct adjoint eigenphase gap is
0.20584. Thus no rank threshold was relaxed to obtain the reported dimensions.
As with earlier versions, no symbolic proof of every floating-point zero is claimed.

For the full family, every original algebra contains the diagonal seed. Its
invariant module is computed first with the block-Krylov method. Reusing this
certified lower-bound subspace when adding other seeds avoids unstable rediscovery.
If a new seed lies in it, minimality is established by both containment bounds;
otherwise its residual is added and closure retested. This is a numerical
organization of the same mathematical problem, not an extra physical symmetry
constraint imposed on the calculation.

## Historical continuity and references

The recovered v12.48 report, `UQCF_GEM_v12_48_Geometric_Observable_Sufficient_Module_Gate.md`,
already reports exact exchange-generated solder modules with dimensions
9, 24, 81, 264 for N=2,3,4,5. This extension uses different supplied motions and
target observables. It does not reopen or rederive that historical result, and
those earlier calculations were not rerun here.

For the standard distinction between minimal linear Krylov reductions and
quantum models obtained by extending to operator algebras, see Grigoletto, Tao,
Ticozzi and Viola, *Exact Model Reduction for Continuous-Time Open Quantum
Dynamics*, Quantum 9, 1814 (2025):
https://quantum-journal.org/papers/q-2025-07-29-1814/
Their continuous-time framework is mathematical context only; it is not imported
as a physical clock, and does not validate the UQCF-GEM ontology.

## Verification and publication status

All 36 new tests pass: 30 model/conditioning/parity controls and six replay tests.
All 236 selected previous v15.11-v15.18 tests were rerun successfully in separate
processes: 272 selected checks in total. This is not a full-repository regression,
formal proof check, empirical validation or independent external peer review.
The new code and arguments received self-review only.

Chromium/Playwright tests cover all 112 cases, 336 checkpoint views, preset/back/
next controls, no external requests or JavaScript errors, and no horizontal
overflow at widths 1280, 820 and 390. The 24-second, 1280x720 H.264 movie was
rendered, visually inspected and completely decoded. Native Safari/iPad attachment
behavior was not tested. The numerical plots use computed data, not image synthesis.

The v15.18 completion source is copied unchanged as Git blob
`f50d12b46c72d564a4e69ebab38d477f147becba`, and its nested baseline hashes are checked.
During this continuation, a GitHub retry accepted the v15.18 core tree object
`485043123792b1ef4829b5c4a5f0f1333b27a5cf`, but the subsequent renderer/template tree
upload was again blocked with indeterminate safety status. No new branch, PR,
merge, or exact-head CI result was created for v15.18/v15.19 in this continuation.
The latest published simulation remains the earlier v15.17 branch. All new v15.19
work is delivered locally in this package; no alternate write path was used.

No entropy objective, fundamental time, calibrated duration, new source law,
carrier identification, automatic actuality, or gravitational fit is introduced.
Pre-time reversible change remains allowed. RAS and RCR stay explicit, separate
inputs of the earlier conditional program. Pillar 3 remains OPEN. No scientific
breakthrough is claimed; the new result is an executed refinement of what this
particular simulator needs for prediction.
