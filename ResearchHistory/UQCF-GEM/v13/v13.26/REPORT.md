# UQCF-GEM v13.26 — RSCL Origin / Absolute Source Calibration Gate

**Date:** 2026-09-12

## Adjudication

The RSCL origin search stops here.

None of the currently frozen ontology-native normalization candidates fixes the absolute retained-to-observer source scale.

The obstruction is again type-level, but it is different from QRSL:

- retained structure can identify source origin, source balance, source direction/support, source-response geometry, and conditionally the current inside a fixed retained measurement convention;
- it does not supply a canonical conversion from those retained source units to the observer stress-energy normalization.

Therefore

`retained source/current -> (varrho_obs, j_obs, kappa_obs)`

still contains the exact positive rescaling freedom

`(varrho_obs, j_obs, kappa_obs) -> (a varrho_obs, a j_obs, kappa_obs/a)`.

No ADM/Einstein residual is needed to see this, and none may be used to remove it.

## 1. Protected source grading

The archived protected grading result fixes source amount/extensivity on the retained side.

That is useful, but it is not an observer calibration.

If a retained grade assigns a definite amount `g_ret`, an observer bridge may still be

`g_obs = a g_ret`

for any positive conversion factor `a` unless one additional calibrated observable fixes the retained-to-observer unit map.

The grade therefore fixes **relative retained source amount**, not the absolute observer stress-energy normalization.

**Verdict: NO RSCL.**

## 2. PGRL exponential-family amplitude has an exact parameterization gauge

For the ETL/PGRL family

`rho_t = exp(log rho + t P) / Z_t`,

perform

`P -> a P`

and

`t -> t/a`.

Then

`(t/a)(aP)=tP`,

so the quantum state is exactly unchanged.

Thus the physical state family cannot distinguish an absolute normalization of `P` from an inverse normalization of its source parameter.

Fresh generic faithful-state controls over

`a = [0.2, 0.5, 1, 2, 5, 11]`

give maximum state mismatch

`1.734e-16`.

The corresponding source-path tangent, transformed with the chain rule, agrees to

`8.210e-11`

under finite-difference evaluation.

Therefore PGRL provides an exact source direction/response family, but no intrinsic absolute source unit unless either `P` or `t` is independently calibrated.

**Verdict: NO RSCL.**

## 3. Genesis Pin / source-origin structure does not supply an observer energy standard

The certified Genesis stack supplies source-origin identity, retained-sequence/provenance identity, and source-flow closure.

Those are identity and compatibility statements.

The source-current equation

`B J = s`

is homogeneous:

`B(aJ)=a s`.

Therefore Genesis anchoring and source-flow closure survive common positive rescaling of the retained source/current pair.

No certified Genesis artifact in the frozen stack supplies an independently calibrated observer energy/momentum scalar that breaks this homogeneity.

Calling the Genesis origin itself the absolute source strength would introduce a new normalization axiom rather than derive one.

**Verdict: NO RSCL.**

## 4. Recoverability-response rank/stability is not absolute calibration

Measured recoverability response can conditionally remove cycle ambiguity and select a retained current when the response aperture is full rank.

But measurement-unit rescaling remains.

For a response equation

`y = R J`,

change response units by

`R -> c R`

and

`y -> c y`.

The reconstructed `J` is unchanged, while every singular value of `R` scales by `c`.

Fresh control over

`c = [0.1, 0.3, 1, 3, 10]`

gives:

- maximum reconstructed-current change: `2.756e-15`;
- maximum error in `sigma_min(cR)=c sigma_min(R)`: `1.887e-15`.

So rank and conditioning certify **identifiability/stability inside a declared measurement convention**. They do not create a physical unit conversion to observer stress-energy.

The common source/current scaling control likewise gives:

- maximum balance residual under `s,J -> a s,a J`: `8.426e-15`;
- maximum coupled-product error under `kappa -> kappa/a`: `5.207e-16`;
- maximum normalized source-direction change: `1.403e-16`.

**Verdict: NO RSCL.**

## 5. RSCL irreducibility theorem for the frozen ontology

Let `D_ret` denote all currently frozen retained data available before observer stress-energy normalization is declared:

- Genesis/source provenance;
- protected source grade;
- selected retained source/current;
- PGRL/QMAR response data;
- recoverability response aperture, rank, and stability;
- retained covariance and balance certificates.

Suppose those data determine some retained source package `F(D_ret)`.

Without an independently calibrated observer scalar, the family

`T_obs(a)=a F(D_ret)`

is equally compatible with the retained data for every `a>0`, while

`kappa_obs(a)=kappa_0/a`

leaves the coupled source object invariant:

`kappa_obs(a) T_obs(a)=kappa_0 F(D_ret)`.

Therefore no function of the frozen retained data alone can determine `a` unless one of those data already contains an observer-calibrated unit standard.

The archive audit finds no such standard.

Hence:

**RSCL is irreducible relative to the current frozen ontology.**

This is not a theorem that no deeper ontology can generate an absolute source scale. It is a branch-stop theorem for the present certified primitives.

## 6. What remains identifiable without RSCL

The no-go does **not** erase source physics already derived.

The following survive:

- source origin/provenance;
- source-current balance;
- conditional response-selected current support/shape;
- PGRL/QMAR source direction and first-order response;
- covariance;
- the projective source class `[T_obs]` under positive common rescaling;
- the coupled object `Sigma_obs = kappa_obs T_obs`, if it can be derived directly and target-blind.

This last object is important because the field equation only sees the product, while v13.25-v13.26 prove that splitting it into an absolutely normalized `T_obs` and `kappa_obs` is not currently derivable.

## Status

- protected source grading -> RSCL: **NO**
- PGRL source amplitude -> RSCL: **NO**
- Genesis source anchoring -> RSCL: **NO**
- recoverability-response normalization -> RSCL: **NO**
- RSCL: **IRREDUCIBLE RELATIVE TO CURRENT FROZEN ONTOLOGY**
- RSCL origin search: **STOP**
- absolute physical stress-energy normalization: **OPEN**
- response-selected retained current: **PRESERVED CONDITIONAL**
- controlled source-coupled ADM/Einstein correspondence: **PRESERVED**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major absolute-source-calibration no-go and branch stop**.

## Next — v13.27

### Projective Coupled-Source / Direct `kappa T` Bridge Gate

Do not try to separate `kappa_obs` from `T_obs`.

Instead define the scale-invariant coupled source object

`Sigma_obs = kappa_obs T_obs`.

Test whether actual retained/PGRL/source-current observables determine `Sigma_obs` directly, before and without consulting any ADM/Einstein residual.

Required gates:

1. target-blind construction from retained data only;
2. invariance under the proven common source rescaling;
3. frame covariance;
4. source/null controls;
5. heldout evaluation against the existing controlled observer source-coupled correspondence only after `Sigma_obs` is locked.

If `Sigma_obs` is derivable, Pillar 3 can advance at the level actually required by the coupled field equation even while absolute stress-energy units remain open.
