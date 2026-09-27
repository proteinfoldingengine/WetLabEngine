# v15.84 — Conditional channel admissibility and recovery obstruction

Verdicts: **LATE_CPTP_LOOP_POWER_CONFIRMED** and
**CPTP_LOOP_RECOVERY_OBSTRUCTED**. All frozen validity checks passed.

The inherited geometric loop does not automatically define a quantum
operation. Under the explicitly specified unital qubit Bloch extension,
powers one through three are positive but not completely positive. The
fourth power is CPTP and admits an exact measure-and-prepare realization.
It retains distinguishability but does not admit exact CPTP recovery of
the tested orthogonal pairs.

These conclusions are conditional on that operational interpretation.
They do not identify the loop with the original three-qubit source channel,
derive a source law, or overturn any historical verdict.

## Direct complete-positivity audit

For T=L^n use
Phi_T(z)=[Tr(z)I+sum_ij T_ij Tr(sigma_j z)sigma_i]/2.
No scaling, correction, optimization or noise is added. All four powers
contract the single-qubit Bloch ball, but this alone does not guarantee
valid action on a system entangled with an ancilla.

| Spatial traversals n | Minimum unnormalized Choi eigenvalue | Classification |
| --- | --- | --- |
| 1 | -0.5000000000 | NON_CP |
| 2 | -0.2427099881 | NON_CP |
| 3 | -0.02514404389 | NON_CP |
| 4 | +0.1603679710 | CPTP |

The Choi matrix has trace 2. Its half is the candidate output for a
normalized maximally entangled input, so the first three rows directly
produce nonpositive candidate joint states. These are substantial negative
eigenvalues, not cancellation artifacts. All matrices and spectra are
published without clipping. The rank-two spectral formula independently
agrees with the direct complex Choi construction.

This pattern was predicted by the already-published singular spectra.
v15.84 is a preregistered diagnostic audit, not a held-out discovery of a
new depth law. Traversal count is spatial composition, not fundamental time.
A valid fourth-power channel does not make the preceding candidate maps
physical or establish a CP-divisible family.

## Constructive realization of the fourth power

The singular values of L^4 are approximately (0.3707634706,0.3085005874,0).
Using its native singular input/output axes gives the exact decomposition:

| Channel component | Weight |
| --- | --- |
| Measure first input axis, prepare corresponding signed first output axis | 0.3707634706 |
| Measure second input axis, prepare corresponding signed second output axis | 0.3085005874 |
| Complete depolarization | 0.3207359420 |

These weights decompose the unchanged matrix; they are not fitted noise
admixtures. The decomposition matches the original map on every complex
matrix unit to 1.32e-81. It proves CPTP implementability and entanglement
breaking: measurement and preparation produce separable outputs with any
ancilla. Some classical distinguishability remains.

This is a mathematical existence result. No physical mechanism selecting
this interpretation or implementing the block has been derived.

## Recoverability is stronger than algebraic inversion

For each right singular axis, test the equally likely antipodal pure input
states. All input trace distances are one. The measured results are:

| Axis | Output trace distance | Optimal mean recovery overlap |
| --- | --- | --- |
| First active axis | 0.3707634706 | 0.6853817353 |
| Second active axis | 0.3085005874 | 0.6542502937 |
| Kernel axis | approximately 0 (5.91e-82 or less) | 0.5 |

Here fidelity means the pure-target overlap
F=Tr(rho_target rho_recovered), without a square root. Each row has its
own binary recovery problem. The optimum (1+D_out)/2 follows from binary
state discrimination and is attained by an explicit measurement followed
by preparation of the guessed input state. This is not an optimum for
arbitrary input ensembles or one universal recovery operation.

Trace-distance contraction prevents any CPTP recovery from restoring both
orthogonal states exactly on either active axis. The formal linear inverse
on the active plane nevertheless exists: its reconstruction error is
7.38e-81 or less. Extending that pseudoinverse as a unital qubit map yields
negative eigenvalues on pure output-axis inputs:

- First axis: minimum eigenvalue -0.8485686688.
- Second axis: minimum eigenvalue -1.1207424572.

Thus algebraic inversion on the image does not provide a physically
admissible recovery map. This gives operational meaning to attenuation
**if** the stipulated Bloch-channel interpretation is used. It does not
retroactively make every geometric contraction a physical information-loss
process. Complete loss occurs for the kernel-axis pair; the two active
pairs remain distinguishable to the nonzero amounts above.

## Exact evidence and reproduction

Parent documentation SHA: `782ed08968e19da829e9b041d5af047af94ba588`.
Preregistration/tests SHA: `af9a92f89ee59065b2ba6316592250bf60cd9778`.
Scientific implementation SHA: `9fc5bfa34fc0624b8f57c2520f2d008aef65b743`.
Branch: `research/v15.84-loop-channel-recoverability`.

- [Expected RED run 36352418004](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36352418004), job `108713505081`.
  Setup passed; the explicit absent-implementation assertion failed.
  [Artifact 10942134777](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36352418004/artifacts/10942134777).
  ZIP SHA-256: `49c99ed3112969525d4a0bed62975950c7947ce62a623f08f9fc3f9bfbba0c3b`.
- [GREEN run 36352664122](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36352664122), job `108714190665`.
  Three tests passed; actual scientific JSON reports the two verdicts
  above and `all_valid: true`.
  [Artifact 10942199904](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36352664122/artifacts/10942199904).
  ZIP SHA-256: `791154df4e28a2a21346e51955e798f2a542764007e62b4f6a6be5437a9ba6f1`.
- Lossless [RESULT.json](RESULT.json) SHA-256:
  `2b51d58a3d5b93c494904a179942feb3e574b8bcec53dbe80c6a6cf5b5ced9f4`.
  [SUMMARY.json](SUMMARY.json), [EVIDENCE.json](EVIDENCE.json),
  [TEST_LOG.txt](TEST_LOG.txt), and [SHA256SUMS](SHA256SUMS) accompany it.
  SHA256SUMS names the artifact's `result.json`, preserved here as `RESULT.json`.

The inherited result is pinned by SHA-256
`bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166`.
All loop powers agree with those stored data to better than 7e-81. All
Choi Hermiticity, TP/unital, and action-reconstruction residuals are zero
at the working precision; spectral-formula errors are at most 4.22e-81.
Recovery distance/fidelity residuals are at most 2.11e-81. The smallest
admissible-state eigenvalue, -2.64e-81, is within the frozen roundoff tolerance;
the order-one negative formal-inverse witnesses are retained separately.

Exact job logs, both downloaded ZIP hashes, execution SHAs, frozen source
bytes and every artifact checksum were verified. Mathematical, code and
artifact-interpretation reviews found no critical or important defect.
There were no implementation repairs or changed criteria after measurement.

Reproduce from the scientific implementation SHA with Python 3.11:

```sh
python -m pip install numpy==2.3.5 sympy==1.13.3 mpmath==1.3.0
cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/loop-channel-recoverability
python -m unittest -v test_gate
python gate.py > result.json
```

The final documentation commit is separate and uses `[skip ci]`. This branch
is not merged to main. Earlier source files and verdicts remain unchanged.

## Remaining boundary

The unital interpretation was explicit. A useful next question is whether
allowing a nonunital affine shift can change channel admissibility while
preserving the measured linear loop matrix. This experiment does not answer
that extension, nor does it establish which operational interpretation a
physical recoverability law should select.

Geometry remains exhaust of retained relational structure. Genesis Pin,
ordered recoverability, and the distinction between acting on a state and
changing admissible worlds remain foundational. No external alignment,
heuristic fitting, fundamental time, dark-matter primitive or gravity
derivation is introduced.
