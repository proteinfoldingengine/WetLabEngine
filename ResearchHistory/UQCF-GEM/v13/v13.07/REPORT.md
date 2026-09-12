# UQCF-GEM v13.07 — LCSP Origin / Source-Compatible Levi-Civita Morphism Gate

**Date:** 2026-09-12

## Adjudication

PGRL and the archived source-current compatibility law do **not** derive LCSP.

The reason is now exact: preserving the Levi-Civita sector imposes additional geometric tangent equations that are not part of either source law.

## 1. Exact tangent condition for metric compatibility

On an edge `i <- j`, define

`F_ij = K_j - O_ij^T K_i O_ij`.

Inside the LC-compatible sector, `F_ij=0`.

For an infinitesimal deformation let

`Omega_ij = O_ij^T dot O_ij`,

so `Omega_ij` is antisymmetric.

Then

`dot F_ij = dot K_j - O_ij^T dot K_i O_ij + [Omega_ij,K_j]`.

Therefore the exact first-order QTC condition is

`dot K_j - O_ij^T dot K_i O_ij + [Omega_ij,K_j] = 0`.

Fresh finite-difference verification of this formula over the executed three-edge state gives maximum error

`1.009e-10`.

## 2. Torsion has its own independent tangent equation

Continuum Cartan torsion obeys

`T = de + omega wedge e`.

At a torsion-free point,

`dot T = D_omega dot e + dot omega wedge e`.

Thus remaining torsion-free requires

`D_omega dot e + dot omega wedge e = 0`.

The discrete RESA precursor is the derivative of transported solder-loop closure.

Fresh finite-difference verification of the discrete formula gives error

`1.252e-11`.

So source-compatible LC motion requires *both* a metric/transport tangent equation and a solder/connection tangent equation.

## 3. PGRL source directions are not generically tangent

Use a faithful anisotropic three-qubit baseline with exact initial QTC and exact solder closure.

Baseline:
- minimum state eigenvalue: `0.0696195265178`;
- max QTC error: `3.846e-16`;
- solder closure: `0.000e+00`.

Now span local source operators by the nine Pauli generators

`A:x,A:y,A:z,B:x,...,C:z`.

Under PGRL/ETL each generator produces a state tangent and therefore induced `dot K` and `dot O`.

The combined LC tangent map has:
- Q-tangent rank: `7`;
- fixed-RESA torsion-like tangent rank: `3`;
- combined rank: `8`;
- nullity: `1`.

The one-dimensional numerical null is dominated by a common z-directed source across all three sites:

`{'A:x': -7.363461701734396e-10, 'A:y': 2.8164278029931556e-09, 'A:z': 0.5773500259497066, 'B:x': -7.340646567420205e-10, 'B:y': 2.811182237107102e-09, 'B:z': 0.576727485098633, 'C:x': -7.394975746341578e-10, 'C:y': 2.8250458300276193e-09, 'C:z': 0.5779726251888401}`.

Combined null residual:

`5.601e-11`.

This rank/nullity is an executed control for this baseline and source class, not a universal representation theorem.

But it is sufficient to falsify the statement that PGRL source tangents automatically lie inside the LC tangent space.

Examples:

`A:z`
- Q tangent norm: `0.63947311082`;
- fixed-RESA torsion-like tangent norm: `5.837e-11`.

So one source can break metric compatibility while leaving the solder closure tangent essentially zero.

`A:x`
- Q tangent norm: `0.193643646351`;
- fixed-RESA torsion-like tangent norm: `0.0047853291171`.

Thus Q and T tangency remain distinct constraints.

## 4. PGRL does not select the solder lift

For the same `A:x` PGRL state tangent, hold RESA solder fixed.

The torsion-like tangent norm is

`0.0047853291171`.

But choose an infinitesimal solder update that cancels the transported closure variation.

Then the tangent norm becomes

`2.168e-19`.

Both lifts share the same `dot rho`, `dot K`, and `dot O`.

The difference is only `dot xi`.

Therefore PGRL cannot determine whether the source deformation is torsion-preserving because PGRL contains no source-to-solder lift.

That missing map is real new information.

## 5. Tangency at one point is not enough

Take the numerically identified one-dimensional first-order null source.

Its tangent residual is below

`5.601e-11`.

But finite source flow leaves the LC sector with scaling

`QTC residual ~ s^2.031824`.

Thus the first nonzero obstruction is second order.

This is an integrability issue: a vector can be tangent to the sector at one point without its finite flow preserving the sector.

## 6. Isotropic points can hide the same obstruction

At maximally mixed local marginals the BKM metric is isotropic.

The commutator term in the tangent condition vanishes, and the BKM metric has no linear anisotropy response at that point.

For the local `A:z` source:

first derivative of the QTC residual:

`-1.692e-11`.

Yet the finite defect scales as

`QTC residual ~ s^1.999473`.

This explains the v13.06 quadratic source escape.

An isotropic state can look LC-tangent at first order while still leaving the sector immediately at second order.

So first-order LC tangency is necessary but not sufficient for LCSP.

## 7. Source-current compatibility has the wrong type to close the gap

PGRL/ETL supplies:

`(rho,P) -> dot rho`.

The archived Path-A source-current rule supplies a ledger balance of the form

`div J + C = 0`

plus observer/source balance.

But LC preservation requires:
- `dot K`;
- `dot O`;
- a compatible `dot xi` or `dot e`;
- and the two tangent equations above.

No current archived theorem maps source-current balance into those joint geometric tangent constraints.

Therefore source-current compatibility can support the Path-A scalar constraint while still being insufficient to guarantee that source deformations remain inside the Levi-Civita sector.

## 8. New missing object

Define:

**SCLL — Source-Compatible Levi-Civita Lift**

For every allowed source deformation in the LC sector, SCLL must jointly lift the PGRL state tangent to:
- connection/transport tangent;
- solder/coframe tangent;

such that the metric-compatibility and torsion-free tangent equations hold.

And because pointwise tangency is insufficient, the resulting tangent distribution must integrate to finite LC-preserving source flows.

SCLL is the infinitesimal/integrability content required by finite LCSP.

## Status

- LC tangent equations: **CLOSED THEOREM**
- PGRL -> LC tangency: **FALSE GENERICALLY**
- source-current compatibility -> LC tangency: **NOT DERIVED**
- first-order tangency -> finite LC preservation: **FALSE**
- SCLL: **NOT DERIVED**
- LCSP: **NOT DERIVED**
- Levi-Civita sector: **NONEMPTY BUT NOT SOURCE-INVARIANT**
- metric-affine parent: **REMAINS GENERIC CONTAINER**
- Pillar 3: **OPEN**

No broader scientific breakthrough is declared.

## Next — v13.08

### LCSP Integrability / Source Superselection Algebra Gate

The next question is global rather than pointwise.

Classify source generators whose PGRL vector fields are tangent to the LC sector **at every state in a connected LC-compatible family**, and test whether those generators are closed under:
- source addition;
- source composition;
- commutator / algebraic generation.

If a nontrivial globally tangent source algebra survives, it is the candidate source superselection algebra of the Einstein-compatible sector.

If only gauge/trivial directions survive, that is an exact no-go for deriving ordinary source dynamics while remaining in the LC sector.
