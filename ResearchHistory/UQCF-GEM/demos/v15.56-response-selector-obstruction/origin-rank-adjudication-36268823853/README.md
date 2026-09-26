# v15.56 origin adjudication: 243 -> 9 -> 3

**Date:** 2026-09-26  
**Scope:** the frozen 11-state, 27-hidden-by-9-source experiment.  
**Decision:** the measured mechanism has two stages. Each local mixed polar response has at most three components; the three-edge direct sum retains nine independent components on every tested fixture; loop composition maps those nine to three. This is not one unexplained local 243 -> 3 compression.

The original result and verdict are preserved unchanged. The rank-nine saturation is numerical evidence on 11 fixtures, not a theorem for all states. The local rank bound and the loop-composition factorization below are algebraic consequences of the stated regularity and hidden-marginal conditions.

## 1. Immutable evidence

- Source commit: `0b7e9ca67cfa98831e60eb3e2add7c42a806f513`.
- Branch at execution: `research/v15.56-response-selector-obstruction`.
- GitHub Actions run: `36268823853`; job: `108478725134` (`origin`). The job completed successfully; its two unit tests and artifact upload completed successfully.
- Artifact: `10914946906`, `polar-sylvester-rank3-origin-result`.
- Downloaded ZIP SHA-256: `b49b4707b297029685c5545983681fdbb7bea67450389c360b95bfef6d865bea`. This was recomputed locally and matches GitHub's digest.
- Extracted, byte-preserved JSON SHA-256: `e756d960ef4b8d5469f457ed2401c4a77b494c98454a7bcb84de70c3bbda29e2`.
- The adjacent `polar_sylvester_rank3_origin_result.json` preserves all 11 original rows, including the original non-skew rank reports and the verdict `LOCAL_SYLVESTER_RANK3`.

Run: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36268823853

Artifact: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36268823853/artifacts/10914946906

## 2. What was measured

| Quantity | Result on all 11 fixtures |
| --- | --- |
| Hidden/source tensor-basis columns | 27 x 9 = 243 |
| Three separate edge ranks | 3, 3, 3 |
| Three separate edge-skew ranks | 3, 3, 3 |
| Stacked three-edge direct-sum rank | 9 |
| Loop-response rank | 3 |
| Full-edge reconstruction relative error | 0.0 as recorded |
| Maximum skew-only reconstruction relative error | 2.9843198351646166e-16 |
| Maximum basis-spectrum discrepancy | 6.362992150585372e-16 |
| Fitted parameters | 0 |

The reported non-skew ranks are 8, 8, 8 on every row. They are not accepted as physical ranks: see the numerical diagnostic below. The artifact contains summary ranks and reconstruction errors, not the raw edge matrices, non-skew norms, or full singular spectra. Those missing quantities cannot be reconstructed from this JSON.

The original label `LOCAL_SYLVESTER_RANK3` describes the per-edge rank cap. It must not be read as saying the entire source-to-loop map becomes rank three before edge composition. The observed direct-sum rank nine rules out that interpretation.

## 3. Local rank bound from hidden-marginal invisibility

Let h be any exact-weight-three Pauli hidden tangent. Its proper one- and two-body partial traces vanish. Consequently, at zero source strength, the one-body means and connected pair-correlation matrices of rho + eta h are unchanged. The hidden and source parameters are perturbation labels, not fundamental time.

For each oriented edge, write the regular polar decomposition

    C_e = O_e P_e,   O_e in SO(3),   P_e positive definite.

Because C_e is unchanged along the hidden direction at zero source strength, O_{e,eta} = 0 and P_{e,eta} = 0 there. Let

    M_e = O_{e,eta s},     W_e = O_e^T M_e.

Differentiating O_e^T O_e = I once in eta and once in s gives

    M_e^T O_e + O_e^T M_e
      + O_{e,eta}^T O_{e,s} + O_{e,s}^T O_{e,eta} = 0.

The last two terms vanish. Therefore W_e^T = -W_e, so M_e lies in the three-dimensional tangent space O_e so(3).

The corresponding mixed polar Sylvester equation simplifies to

    P_e W_e + W_e P_e = O_e^T C_{e,eta s} - C_{e,eta s}^T O_e.

The operator is invertible on skew matrices when P_e is positive definite. Hence the local output has at most three independent components. Attainment of all three is a property of the source-to-edge map; it is observed for each edge on all 11 fixtures, not assumed by this proof.

This uses the actual hidden basis in `response_quotient_rank.py`, the connected-correlation construction in `independent_hidden_fixture.py`, and the mixed derivative in `closed_form_hidden_response.py`, all at the frozen source commit. It is not an extension to singular polar strata or determinant-branch crossings.

## 4. Exact loop factorization, kernel, and spectrum

Use the actual edge ordering (0,1), (1,2), (2,0). Put

    H = O_0 O_1 O_2,     A_e = M_e O_e^T in so(3).

All mixed product terms containing O_{e,eta} vanish under the condition above. The mixed loop response is

    K = M_0 O_1 O_2 + O_0 M_1 O_2 + O_0 O_1 M_2.

Right-trivializing at H gives

    K H^T = A_0 + O_0 A_1 O_0^T
                  + (O_0 O_1) A_2 (O_0 O_1)^T.

Thus the tensorized response factors as

    R^243 --E--> so(3) direct-sum so(3) direct-sum so(3) --L--> so(3),

where E is the genuine source-to-edge response and

    L = [I, Ad(O_0), Ad(O_0 O_1)].

The loop map is onto because its first block is I. Its rank is exactly three on the full nine-dimensional edge space, independent of the source law. A constructive six-dimensional kernel is obtained by choosing arbitrary A_0 and A_1 and setting

    A_2 = -(O_0 O_1)^T (A_0 + O_0 A_1 O_0^T) (O_0 O_1).

There is a stronger normalization-sensitive identity. In Hilbert-Schmidt orthonormal skew bases, every adjoint block is orthogonal, hence

    L L^T = 3 I_3.

Therefore the three nonzero singular values of the loop-composition map itself are exactly sqrt(3), sqrt(3), sqrt(3). The canonical visible projector on edge space is

    Pi_visible = L^T L / 3,

and I - Pi_visible projects onto the six-dimensional loop-invisible subspace. This statement is about the loop map L, NOT about the singular values of the full 243-column response L E.

Using the observed edge-map rank nine, the measured tensorized nullity splits as

    dim ker(E) = 243 - 9 = 234,
    dim ker(L) = 9 - 3 = 6,
    dim ker(L E) = 234 + 6 = 240.

These dimensions refer to the linear span of hidden/source tensor products. They do not count 240 independent physical states or assert that every kernel vector is one decomposable h tensor p.

The loop reduction is an ordinary consequence of SO(3) product geometry. It is not, by itself, evidence for a new gravitational law, physical universality, emergent spatial dimension, or uniqueness of the chosen source prescription. Any scientific specificity must be found in E and in its loop-visible projection, not in the existence of a rank-three output.

## 5. Independently executed algebra checks

The adjacent script `origin_factorization_check.py` was executed locally with NumPy 2.3.5, seed 20260926. It checks the archived result, the polar rotations derived from all 11 fixture parameters, and 100 additional independent triples of rotations. It does not rerun or replace the original source experiment.

All 111 loop-map cases passed the rank-three, six-dimensional-kernel, sqrt(3)-spectrum, product-rule, and visible-projector checks. Maximum residuals were:

| Check | Maximum residual |
| --- | --- |
| L L^T - 3 I | 5.224429723519646e-15 |
| Constructed loop-kernel residual | 3.3638580222410747e-15 |
| Pi_visible squared - Pi_visible | 1.768936061381237e-15 |
| Direct product derivative versus trivialized formula | 4.727089922702825e-15 |

The original fixture correlation blocks used in this independent check are

    [[d,-a,0],[a,d,0],[0,0,d/2-m^2]].

All have positive determinant and smallest singular value at least 0.02, allowing for floating-point comparison. The proof is not relying on an edge-rank loss at a singular boundary.

### Roundoff diagnostic

The original rank function compares each matrix's singular values only to that same matrix's largest singular value. For a theoretically zero residual, this can normalize numerical noise into an apparent nonzero rank.

I reproduced this mechanism using synthetic columns known algebraically to have M_e = O_e W_e with W_e skew, then performing the same floating-point projection as the experiment. Self-relative non-skew ranks were [8,8,8,5,5,8,5,5,8,5,8] while the maximum residual-to-parent norm was only 3.0585921420230705e-16. With an illustrative parent-scaled floating-point floor, all those synthetic residuals had effective rank zero.

This is a diagnostic reproduction, not a measurement of the original non-skew matrices: the latter were not archived. The illustrative floor is not a new scientific acceptance threshold, and no original tolerance or recorded value was changed. The next run must save the original residual norms and spectra and use a preregistered error budget anchored to the parent matrix.

NumPy's rank documentation explicitly distinguishes SVD roundoff from errors already present in the matrix and permits a tolerance based on the latter: https://numpy.org/doc/2.3/reference/generated/numpy.linalg.matrix_rank.html

## 6. Audit limitations: not repaired by this documentation

1. The original unit test accepts `INVALID` as an allowed verdict and does not assert the scientific control gates. The original CLI prints JSON without a verdict-dependent failure exit. Thus green CI alone is not scientific certification. The actual archived rows and controls were inspected independently here; this limitation does not erase their recorded values.
2. Full reconstruction uses the same closed-form ingredients and product formula as `K_for`. Its zero error is an internal consistency check, not an independent experimental or finite-difference validation in this run.
3. Orthogonal column mixing tests singular-spectrum invariance. It is not a new measurement of physical universality or a recomputation under every local-frame change.
4. No raw nine-by-243 source-to-edge matrix, parent-scaled non-skew diagnostic, or full spectral gap is stored in the original result. The reported non-skew rank eight is quarantined rather than silently replaced with zero.

The production experiment, source law, original tests, workflow, and tolerances are unchanged by this adjudication. This directory adds evidence, mathematical analysis, and a separately executed reproducibility check only.

## 7. Next bounded task: source-to-edge factorization gate

The next implementation should retain the same 11 fixtures, all 243 columns, and frozen source prescription, without fitting or selecting new states based on the result.

Export E (9 x 243), L (3 x 9), and the independently assembled loop response, using documented orthonormal skew bases. Save all singular spectra, the actual hidden first-edge derivative norms, non-skew norms relative to their parent edge matrices, state/edge conditioning margins, and source provenance. Verify the factorization and decompose E with Pi_visible and I - Pi_visible.

Before interpreting new results, add failing tests for an invalid control record, missing fixture/column, nonfinite value, and a roundoff-only residual. Make scientific invalidity fail the CLI and workflow, and propagate failures through any logging pipeline. Freeze scale-aware rank/error criteria before the full rerun; do not infer thresholds from the desired rank.

Only then ask which structure in E survives conditioning, basis, and source-law controls beyond the compulsory SO(3) tangent-space cap. That is the scientifically discriminating part; the rank-three loop output itself is now explained.

**Status:** original fixture-level origin result adjudicated; factorization and six-dimensional loop kernel derived and independently checked; source-suite diagnostic hardening and raw-matrix export not yet implemented or run.

## Reproduction

From this directory, with Python and NumPy installed:

```bash
OPENBLAS_NUM_THREADS=1 python origin_factorization_check.py
```

Do not use Python's `-O` option, which disables assertion checks. The script validates the SHA-256 of the adjacent preserved JSON and writes `origin_factorization_check_result.json`. If the original ZIP is present under `polar-sylvester-rank3-origin-36268823853.zip`, it also verifies the ZIP digest; the ZIP is not required to reproduce the algebra checks. Small floating residuals may differ across numerical-library builds; exact decimal agreement is not the gate.
