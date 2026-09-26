# v15.61 Source-derivative classification — theorem target

Date: 2026-09-26.

## Scope

No new source law is measured in this stage. The purpose is to classify the first mixed hidden/source response for a general differentiable source update and identify the exact mathematical object that can carry hidden global completion into retained edge geometry.

Perturbation parameters below are ordered repair/source labels, not fundamental time.

## Setup

Let rho be a full-rank global state and h a hidden tangent satisfying

    R_e h = 0

for every retained proper marginal map R_e used to construct edge geometry. Let T_s be a differentiable normalized source update with T_0(rho)=rho.

Define its source vector field

    X(rho) = partial_s T_s(rho)|_{s=0}.

The mixed hidden/source state response is

    Y_rho[h] = partial_eta partial_s T_s(rho + eta h)|_{eta=s=0}
             = D X_rho[h].

Thus the source-law classification begins with the Frechet derivative D X_rho, not with the finite update itself.

## Retained mixed response

For edge e define

    B_{e,rho}[h] = R_e D X_rho[h].

This is the hidden-to-retained leakage operator induced by the source vector field.

If the retained edge observable is a differentiable map C_e=C_e(R_e rho), its mixed source response is

    delta_{eta s} C_e = D C_{e,R_e rho}[ B_{e,rho}[h] ].

For the present connected-correlation construction this derivative includes the derivative of the one-body subtraction terms and is linear in B.

## Polar/Sylvester projection

On the regular polar stratum write

    C_e = O_e P_e,   O_e in SO(3),   P_e > 0.

Because the hidden tangent alone leaves retained marginals fixed, partial_eta C_e=0, hence partial_eta O_e=partial_eta P_e=0.

Let M_e=partial_{eta s} O_e and W_e=O_e^T M_e in so(3). Then

    P_e W_e + W_e P_e
      = O_e^T(delta C_e) - (delta C_e)^T O_e.

Since P_e>0, the Sylvester operator S_{P_e}: W -> P_e W + W P_e is invertible on so(3). Therefore

    W_e = S_{P_e}^{-1} [ O_e^T(delta C_e) - (delta C_e)^T O_e ].

The complete mixed response factors as

    hidden/source column
      -> D X_{rho,p}[h]
      -> R_e D X_{rho,p}[h]
      -> D C_e[...]
      -> O_e-skew projection
      -> S_{P_e}^{-1}
      -> W_e in so(3).

Across three edges the codomain is so(3) direct-sum so(3) direct-sum so(3), hence dimension at most nine.

## Theorem 1 — retained-closure obstruction

If

    R_e D X_rho[h] = 0

for every hidden h in the common retained kernel and every edge e, then the complete mixed edge response vanishes:

    E_rho = 0.

Proof: retained mixed leakage is zero, hence delta C_e=0, hence W_e=0 edge by edge.

This is the infinitesimal form of the v15.57 local-unitary null. Exact finite-s marginal autonomy is sufficient but stronger than necessary.

## Theorem 2 — non-closure is not sufficient in general

The converse of Theorem 1 is false without an observability condition.

It is possible that

    R_e D X_rho[h] != 0

while

    O_e^T D C_e[R_e D X_rho[h]]
      - D C_e[R_e D X_rho[h]]^T O_e = 0.

Such leakage changes only the polar-positive/symmetric sector of the edge observable and produces no rotational response.

Therefore a particular hidden/source column is rotationally visible at edge e exactly when the O_e-skew projection above is nonzero.

Because the Sylvester inverse is invertible, it cannot create or destroy rank after this projection.

## Theorem 3 — rank classification on the regular stratum

Define the pre-Sylvester observable map Q_rho by

    Q_rho(h,p)
      = direct_sum_e {
          O_e^T D C_e[R_e D X_{rho,p}[h]]
          - D C_e[R_e D X_{rho,p}[h]]^T O_e
        }.

Then

    rank(E_rho) = rank(Q_rho) <= 9.

Reason: the block-diagonal Sylvester inverse is an isomorphism on the nine-dimensional codomain.

Thus rank-nine saturation is exactly the statement that the observable hidden-leakage map Q_rho is surjective onto the complete three-edge rotational tangent space.

## Consequence for v15.57–v15.60

The experiments now separate three layers:

1. source closure: does R_e D X[h] vanish?
2. observable leakage: if not, does D C_e[R_e D X[h]] have a polar-skew component?
3. geometric conditioning: the invertible Sylvester map reshapes amplitudes but does not determine rank.

The local-unitary law lies in layer-1 null: no retained hidden leakage.

The exponential and positive-filter laws empirically reach rank nine after layer 2 on the tested ensembles. v15.59 does not prove that arbitrary non-closure is sufficient; Theorem 2 shows why such a universal converse is false.

## Candidate source-class invariant

For each source law define

    I_X(rho) = rowspace Q_rho

inside the 243-dimensional hidden/source column space.

v15.60's amplitude-stable overlap is evidence that two non-closed source laws have nearby I_X(rho) on the tested states.

This is the correct invariant candidate. In a regular rank-nine case, left multiplication by the block-invertible Sylvester map preserves row space, so rowspace(E_rho)=rowspace(Q_rho).

## Falsification target

The next experiment should not use another generic non-closed law. It should construct a differentiable normalized source vector field with:

1. demonstrable retained hidden leakage R_e D X[h] != 0;
2. leakage engineered or naturally constrained to the polar-symmetric null of the skew-observable projection for at least one controlled sector.

The theorem predicts non-closure with reduced or zero rotational response in that sector. Observing full rotational response despite an exact projected-null construction would falsify the factorization or its implementation.

## Boundaries

These are local derivative statements on the regular polar stratum. They do not select a physical source law, identify gravity, establish Einstein dynamics, or apply through singular polar strata without additional analysis.
