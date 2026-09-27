# v15.79 results — transforming source data restore observable couplings

Verdict: **COVARIANT_SOURCE_COUPLING_CLASSIFICATION_CONFIRMED**.
Separate gate: **COVARIANT_COUPLINGS_ENSEMBLE_NULL_EXCLUDED**.
All validity controls passed. Three tests passed; no implementation repair,
preregistration change, threshold adjustment, or amplitude adjustment occurred.

## Scientific result

The source-free obstruction of v15.78 changes when the source transforms as
data. For the explicitly restricted class of state-independent real bilinear
maps from one Hermitian three-qubit source tensor and one weight-three hidden
tangent into retained weight-one/two output, independent local SU(2)^3
covariance permits exactly 18 coupling tensors.

A source support S can feed retained support T precisely when S union T
covers all three sites. Each allowed support pair has one coupling: preserve
at source-scalar sites, dot at output-scalar sites, and cross where both
source and output are vectors. These are invariants of the qubit adjoint
representation, not an inserted spatial geometry or alignment convention.

| Source weight | One-body output couplings | Pair-output couplings | Total |
|---|---:|---:|---:|
| 1 | 0 | 3 | 3 |
| 2 | 3 | 6 | 9 |
| 3 | 3 | 3 | 6 |
| Total | 6 | 12 | 18 |

The independent local Lie-algebra nullities were 0,1,1,1 for scalar/scalar,
scalar/vector, vector/scalar, vector/vector source/output cases, stable at
all three frozen thresholds. Their products give the table above; the
explicit delta/epsilon tensor basis also had rank 18. The scalar source
sector has no retained coupling, agreeing with v15.78.

The commutator response -i[P_a/2,h] is the sum of the nine one-cross tensors,
with the frozen coefficients +1. Its finite unitary control agreed to
2.221e-16. The traceless Jordan benchmark is the sum of six zero-cross
tensors with coefficient +1 and three two-cross tensors with coefficient -1.
Both direct complex-matrix response checks agreed to 1.111e-16. The Jordan
benchmark is algebraic only. This does not give 18 independent physical
channel parameters, nor nine independently selectable unitary couplings.

## Observable response and negative control

Both stacked Q and E coefficient maps, each 183708 by 18, had rank 18 at
relative thresholds 1e-9,1e-10,1e-11. Thus the common coefficient nullspace
was zero. The smallest/largest singular-value ratios were:

- Q: 0.0407542241361284; smallest singular value 4.791698591833591.
- E: 0.040151882163759756; smallest singular value 24.357023993210756.

These gaps are well separated from the frozen cutoffs. As a diagnostic,
each of the 12 individual reference maps also had Q/E coefficient rank 18
when all 63 source basis elements and 27 hidden probes were included.
This does not mean every individual source/probe pair has a response, nor
that edge rotational geometry has dimension 18. Each individual edge-direct-
sum rotational tangent still has at most nine components; the rank here
identifies shared coupling coefficients over many input experiments.

The certified zero-Bloch fixture had Q/E rank 12, with exactly the six
one-body-output columns in its kernel. Their response and the expected-kernel
projector error were zero at reported precision. Nonzero one-body leakage
can therefore remain rotationally invisible at that special state. The
control distinguishes this pointwise failure from common nullity across
the asymmetric ensemble.

## Validation

The canonical tensor Gram error and all infinitesimal covariance residuals
were zero at reported precision. Maximum generic finite covariance residual
was 2.520e-16. The local kernel-projector comparison error was 7.656e-16.
Complex moments were preserved: maximum imaginary retained residue was
2.776e-17. Independent direct Q/E assembly checks were within 1.777e-15 and
7.106e-15; maximum Sylvester residual was 1.461e-14. The reference/control
state domain passed, with minimum density eigenvalue 0.0383382 and minimum
edge singular value 0.0208610. All frozen validity criteria passed.

## Exact certification evidence

- Certified parent: `7f68c941f699ccbebec5b15834bfdb032807950f`.
- Preregistration/tests, gate.py absent: `52b9db5167a995a6545288b34385da3ee060e6bd`.
- Tested scientific implementation: `034621dc0751adbc8d0406c4804e0b9237590a07`.
- RED [run 36327978182](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36327978182), job `108644320415`, artifact `10934597454`.
- RED artifact SHA-256: `64b127665c84ec821288cbbd475df795ce65a19249aa7096fa3b10ab57e15f25`.
- GREEN [run 36328255481](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36328255481), job `108645096885`, artifact `10934528168`.
- GREEN artifact SHA-256: `faa07dc4efb028558041307f5e93201de7598d1d55d1d9c37d1b0cba6ee6e407`.
- Full result JSON SHA-256: `ff74e08ecc0cdb944f27efdaa97602de4f285ee8937f55386b6bfa580c18fecd`.
- Lossless `RESULT.json.gz` SHA-256: `6728127fd9a2f88ef105eb7ba968dd3254f11ff83b71987d7064ca3bc777354f`.
- Compressed result Git blob: `db0850baa9d9a8ff818c83e232d3274517cbb5dc` (16,705 bytes).

The exact RED job log was read: setup succeeded, then the absent-implementation
assertion stopped execution with zero tests run. Its downloaded artifact
confirmed the execution SHA, absent gate.py, and identical frozen document
and test bytes. The exact GREEN job log showed all three tests passing and
the two scientific verdicts. Its artifact was downloaded and SHA-256 checked;
execution SHA, all frozen source bytes, and SHA256SUMS were verified. The
JSON scientific verdicts were read independently of the green CI status.

The complete JSON, including local kernel projectors, coefficient spectra
and Gram matrices, is preserved losslessly in the repository beyond Actions
retention. `SUMMARY.json` is a convenience derived from that artifact.
`TEST_LOG.txt` and `SHA256SUMS` are copied from the GREEN artifact. Final
publication adds documentation only; the scientific certification boundary
is the tested SHA above. No merge to main was performed.

## Reproduction

At the tested commit, use Python 3.11 and numpy==2.3.5. From this folder:

```sh
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > result.json
gzip -dc RESULT.json.gz > certified-result.json
sha256sum certified-result.json
```

The gzip command uses the additive documentation head containing the archived
result; the tested implementation SHA predates that archival file.

## Interpretation boundary and next question

The new content is the explicit classification of transforming source
representations and their finite-ensemble observability. The general
open-state exclusion of state-independent retained rotational-null response
was already established in v15.75; it is not claimed as a new theorem here.
No open-set conclusion is inferred just from finite sampled ranks.

This result concerns a single source tensor, bilinearity, fixed coefficients,
and the specified local representation content. It does not cover additional
transforming source tensors, state-adapted coefficients, nonlinear source
laws, or higher local source representations. Earlier calibrated symmetric-
null examples and all historical verdicts remain intact. In particular,
a reference-derived retained tensor is additional source data, not something
this single-source classification silently includes.

Covariance now permits leakage, and no nonzero coupling in this restricted
class remains null on all frozen source/hidden experiments. Covariance still
does not select a physical law or its coefficients. The next useful gate
should distinguish these algebraically permitted responses from those that
admit positive affine source updates, with the unitary positive control
preserved and source-sign/reversibility assumptions stated explicitly.
Restriction/composition naturality and changing admissible-world consistency
are not established here. Genesis Pin and ordered recoverability remain
foundational; no fundamental time, dark-matter primitive, or gravity
derivation is introduced.
