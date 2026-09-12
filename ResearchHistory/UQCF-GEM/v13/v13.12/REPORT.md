# UQCF-GEM v13.12 — Shear Nonmetricity / Curvature Response Coupling Gate

**Date:** 2026-09-12

## Adjudication

The traceless/shear nonmetricity channel and the retained holonomy/curvature response channel are **not locked to one another** by the present BKM/polar kinematics.

Two exact complementary controls close this.

## 1. Shear object

After v13.11 removes the exact trace/Weyl part, define

`Sigma_ij = dev(log G_ij)`

with

`G_ij = K_j^-1/2 O_ij^T K_i O_ij K_j^-1/2`.

`Sigma_ij` is symmetric and traceless.

Under an endpoint frame rotation it transforms covariantly in the target frame:

`Sigma_ij -> R_j Sigma_ij R_j^T`.

Fresh source-response covariance error:

`6.228e-10`.

So the shear channel is a legitimate gauge-covariant retained observable.

## 2. Zero shear response with nonzero curvature response

Reuse the exact hidden-completion source-flow pair from v13.09/10.

Both states remain in the axial QTC-compatible sector under the common radial source.

Therefore every edge has

`G_ij = I`

and hence

`Sigma_ij = 0`

throughout the flow.

Fresh source jets:

### rigid completion
- shear response norm: `7.807e-12`;
- holonomy response norm: `1.735e-11`.

### hidden phase-drifting completion
- shear response norm: `8.540e-12`;
- holonomy response norm: `0.19261155662`.

At finite source `s=0.8`:
- hidden shear norm remains `2.048e-15`;
- rigid/hidden holonomy difference is `0.206032427262`.

Thus:

**nonzero curvature/holonomy response can occur with exactly zero shear nonmetricity response.**

This immediately rules out any universal law or zero-intercept bound of the form

`||dot curvature|| <= C ||dot shear||`.

## 3. Nonzero shear response with zero curvature response

The reverse control is also realizable by a legitimate PGRL tangent.

Construct a faithful three-qubit family in which:
- the connected pair tensors `C_ij` are held fixed;
- therefore the polar transports `O_ij` remain fixed;
- one local marginal changes, so its BKM metric changes.

The desired traceless state tangent was inverted through the faithful Kubo-Mori map to obtain an ETL/PGRL source operator.

ETL tangent reconstruction error:

`9.272e-11`.

Fresh response:
- connected-correlation jet: `8.213e-11`;
- polar-transport jet: `6.486e-16`;
- shear response norm: `0.0149148854933`;
- holonomy response norm: `8.203e-16`.

Thus:

**nonzero shear nonmetricity response can occur with zero curvature/holonomy response.**

This rules out the reverse universal implication or zero-intercept bound.

## 4. Structural independence theorem

At a metric-compatible edge,

`K_j = O^T K_i O`.

The linear metric defect response is

`dot M_ij = dot K_j - O^T dot K_i O + [Omega_ij,K_j]`.

The loop holonomy response, by contrast, depends only on the edge transport jets through the product rule.

Therefore there are two independent first-order directions:

1. **metric direction**  
   Change endpoint BKM metrics while keeping `O` fixed.  
   Result: shear changes; holonomy does not.

2. **stabilizer connection direction**  
   Change `O` inside a stabilizer commuting with the endpoint metric.  
   Result: holonomy changes; shear remains zero.

The two executed quantum controls realize both directions.

Therefore:

`dot shear` and `dot curvature`

are distinct response channels of the metric-affine parent.

Neither is kinematically a function of the other.

## 5. Generic constant-linear coupling audit

As a falsification test only, not as a field-equation fit, a single constant linear map

`dot h = A dot Sigma`

was estimated on 18 generic faithful states and tested on 10 separate states.

Samples:

`252`.

Train R^2:

`0.108439968403`.

Holdout R^2:

`-0.0488343817553`.

Holdout relative error:

`1.02254683045`.

A matched output-permutation null gave holdout R^2

`-0.162991207256`.

The constant-linear candidate does not supply a reliable generic closure.

This numerical audit is secondary; the exact two-way counterexamples above already rule out deterministic shear/curvature locking.

## 6. Relation to the older retained nonmetricity branch

The older retained-recombination connection found:

`shear-dominated Q ~ g`

followed by

`positive curvature R ~ g^2`.

That remains an important architectural precedent.

But it is a different connection with a different construction and coarse-graining law.

v13.12 therefore does **not** infer

`BKM shear -> curvature`

from that older hierarchy.

A typed bridge between the connections would be required first.

## Scientific meaning

v13.11 showed that the scalar/Weyl part of BKM nonmetricity is exact and integrable.

v13.12 now shows that the remaining shear sector still does not generate curvature by itself.

The generic pre-time metric-affine response architecture is therefore better represented as

`full quantum completion`
-> `metric/BKM response channel`
and independently
-> `connection/holonomy response channel`.

They meet in the full metric-affine connection, but neither channel determines the other at the current kinematic level.

This is consistent with the v13.10/11 non-autonomy result: hidden completion carries source-response information beyond instantaneous geometry.

## Status

- shear observable: **COVARIANT / WELL DEFINED**
- shear -> curvature response: **FALSE GENERICALLY**
- curvature -> shear response: **FALSE GENERICALLY**
- constant-linear generic coupling: **FAIL**
- derived shear-curvature field law: **NOT FOUND**
- QMAR given full state: **REMAINS**
- trace/Weyl exactness: **REMAINS CLOSED**
- metric-affine parent: **INDEPENDENT METRIC + CONNECTION RESPONSE CHANNELS**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a major no-go/channel-separation result.

## Next — v13.13

### Hidden-Completion Response State / Minimal Markov Closure Gate

The next issue is now unavoidable.

Instantaneous geometry—even after adding shear nonmetricity—does not determine its own source response.

The next gate should identify the **minimal hidden-completion data** needed to make the response state autonomous.

Begin with the v13.10 chiral three-body observable and test whether a finite set of higher-order correlators closes QMAR under source deformation, or whether source response opens an irreducible hierarchy.
