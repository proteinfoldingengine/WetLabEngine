# UQCF-GEM Holonomy Landscape — Phase 2

## Exact theorem

For qubit nodes, let the BKM-whitened connected covariance response on edge
\(i\to j\) be

\[
M_{ij}=G_j^{-1/2}\Gamma_{ij}^{\mathsf T}G_i^{-1/2}.
\]

When every \(M_{ij}\) is full rank, its polar factor \(V_{ij}\) is an element
of \(O(3)\). Therefore the triangle loop

\[
H_\triangle=V_{31}V_{23}V_{12}
\]

is exactly orthogonal:

\[
H_\triangle^{\mathsf T}H_\triangle=I.
\]

Its orientation parity is

\[
\nu=\det H_\triangle
=\prod_{\text{edges}}\operatorname{sgn}\det\Gamma_{ij}.
\]

The BKM metric matrices are positive definite and therefore cannot alter the
determinant signs.

Consequences:

- \(\nu=+1\): the loop is a proper rotation.
- \(\nu=-1\): the loop is an improper rotation (a reflection when its
  continuous angle is zero).
- \(\nu\) cannot change under a continuous state deformation unless at least
  one edge covariance determinant crosses zero, i.e. an edge response loses
  rank.

This is the exact topological structure behind the earlier
reflection → rank loss → identity transition.

## Scientific correction

The generalized W family gives the special improper loop

\[
\operatorname{spec}H_\triangle=\{-1,+1,+1\},
\]

which is a pure reflection.

That reflection is **not** the only possible full-rank loop. General mixed
three-qubit states produce both proper rotations and improper
rotoreflections with continuous angles. Generic pure states in the survey
remained in the improper sector but were not always exact reflections.

## Run

```bash
python -m pip install -r requirements.txt
python holonomy_landscape_phase2.py --samples 500
```

Outputs:

- `phase2_output/phase2_results.json`
- `phase2_output/01_holonomy_angle_landscape.png`
- `phase2_output/02_parity_rank_loss_transition.png`

## Claim boundary

This concerns canonical BKM observable-response transport for finite
three-qubit states. It is not spacetime curvature, a physical gauge field,
gravity, or an ADM/Einstein derivation.


## Explicit pure-state rotoreflection counterexample

`pure_rotoreflection_counterexample.json` contains a normalized pure
three-qubit state with all three edge-response maps full rank, but with

\[
\operatorname{spec}H_\triangle
=
\{-1,e^{+i\theta},e^{-i\theta}\},
\qquad
\theta\approx 0.03533.
\]

This falsifies the stronger statement that every pure-state loop is an exact
reflection. The exact pure-state statement is orientation parity
\(\det H_\triangle=-1\) on the full-rank sector.
