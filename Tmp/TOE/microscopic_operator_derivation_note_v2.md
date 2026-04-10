# Microscopic Operator Derivation Note (Worked Example v1)
## UQCF-GEM retained-coherence bridge
## Sprint H — executable worked example extension

This note extends `microscopic_operator_derivation_note.md` by executing the 2-shell × 2-microstate example numerically.

## 1. Fixed toy-example choices

We take:
- A0 = 1.0
- B0 = 1.0
- C0 = 1.0
- d_eff = 3.9
- shell / micro / cross exponents all fixed to 1 in the 2×2 truncation

The microscopic basis is:
- |1,1>, |1,2>, |2,1>, |2,2>

The off-diagonal couplings are:
- shell transport: -A_gamma / 2
- microstate return: -B_gamma / 2
- cross coupling: -C_gamma / 4

with diagonals chosen so each row sums to zero.

## 2. Concrete matrix at the certified closure point gamma*

Using gamma* = 0.26671093, the matrix is given in the companion CSV.

## 3. Spectral response

For each gamma, we compute:
- eigvals of L_coh(gamma)
- return probability P(tau; gamma) = Tr(exp(-tau L))
- D_spec from the slope of log P vs log tau on tau = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

## 4. Explicit affine normalization for the toy example

To tie the toy example back to the certified reduced map, we use an explicit affine normalization

sigma(D) = a + b D

with:
- sigma(gamma*) = 1 - gamma*
- sigma(0.36) = 0.75

This yields:
- a = -2.619076613
- b = 4.824526992

This normalization is not claimed as fundamental. It is an explicit calibration layer making the toy operator auditable against the known closure scale.

## 5. Result

On the sampled interval, the toy example gives:
- F(0.18) > 0
- F(gamma*) ≈ 0
- F(0.36) < 0

So the explicit 2×2 operator now demonstrates a concrete crossing structure rather than only a schematic one.

## 6. Interpretation

This does not prove the full bridge. It does show that:
- the shell–microstate–cross triad can be written explicitly,
- the spectral response can be computed directly,
- the reduced map can be recovered in a concrete low-dimensional truncation,
- and shell-only / no-cross / no-return ablations can be tested directly on the same matrix model.

This is a substantial auditability upgrade over a purely prose-level operator proposal.
