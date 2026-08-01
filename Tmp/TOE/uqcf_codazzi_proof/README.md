# UQCF-GEM Codazzi Verification Harness

This package reconstructs and verifies the smallest explicit state-level
Codazzi finding from the three-binary-node UQCF-GEM response program.

## What it verifies

The code starts from the exact eight-state exponential-family probability law

\[
p(x)\propto\exp[h_1x_1+h_2x_2+J(x_1x_2+x_2x_3+x_3x_1)]
\]

and computes, rather than hard-codes:

1. node means, variances, and pair covariances;
2. canonical local Fisher/BKM score coefficients;
3. intrinsic covariance-defined edge response maps;
4. the bidirectionally symmetrized pulled-back response tensor;
5. its exponential-affine Codazzi defect;
6. spin-flip-protected closure at the unbiased point;
7. the weak-coupling Codazzi susceptibility and its rank.

At the audit point \(h_1=0.20,\ h_2=-0.15,\ J=0.70\), the harness reproduces

\[
\mathcal M^{\rm sym}\approx
\begin{pmatrix}
1.3812994662 & 1.3574832752\\
1.3574832752 & 1.3907319546
\end{pmatrix},
\]

\[
(\mathfrak I_{121},\mathfrak I_{122})
\approx(-0.3458963928,-0.3209724905).
\]

It also verifies that the unbiased point has zero Codazzi defect and that,
for weak nonzero coupling, the field susceptibility is full rank with

\[
\Xi(J)=J^2
\begin{pmatrix}
0&1\\
-1&0
\end{pmatrix}
+O(J^3).
\]

## Scientific claim boundary

This is a high-precision executable verification harness, not a formal proof
assistant certificate. It verifies the finite model and numerical/asymptotic
claims directly from exact state enumeration. It does **not** prove that the
result holds for all graphs, all quantum systems, or physical gravity.

## Run

```bash
python -m pip install mpmath
python uqcf_codazzi_verification.py
```

Optional tests:

```bash
python -m pip install pytest
pytest -q
```

## Files

- `uqcf_codazzi_verification.py` — standalone verification script
- `test_uqcf_codazzi.py` — regression tests
- `requirements.txt` — minimal dependencies
