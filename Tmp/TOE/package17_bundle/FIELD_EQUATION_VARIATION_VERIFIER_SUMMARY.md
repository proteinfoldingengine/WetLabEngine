# FIELD_EQUATION_VARIATION_VERIFIER_SUMMARY.md

# Verifier Summary
## Variational stress-energy and weak-memory decoupling

## Status
**Executed structural verifier. Not a full GR derivation.**

Verifier file:

```text
field_equation_variation_verifier.py
```

Execution log:

```text
field_equation_variation_verifier_run.log
```

## Captured output

```text
Field equation variation verifier
==================================================
Symbolic proxy:
Tmem_general: eta**2*(ZR*dr2/2 + r**2*v2/2) + eta*(Tmat*lam*r + r*v1) + v0
Tmem_with_V0_zero: eta**2*(ZR*dr2/2 + r**2*v2/2) + eta*(Tmat*lam*r + r*v1)
Q_exchange_proxy: eta*(Tmat*lam + divT*lam*r)

Sweep results:
PASS: 95.1
SOFT_FAIL: 0.0
HARD_FAIL: 4.9
leading_order_median: 1.0
fraction_Oeta: 100.0
fraction_Oeta2: 0.0
fraction_Q_Oeta: 100.0
```

## Interpretation

The verifier checks a symbolic/proxy scalar-density memory sector.

It confirms:
- \(V(0)=0\) removes the \(O(1)\) memory residue;
- finite coefficients produce \(O(\eta)\) or smaller memory stress-energy;
- the interaction exchange current can be represented as \(Q_\nu=O(\eta)\);
- singular coefficients or \(V(0)\neq0\) are hard failures.

This does not prove:
- full Einstein-Hilbert variation from the discrete action,
- exact matter-memory coupling,
- exact \(Q_\nu\),
- or microscopic conservation.

**End of summary.**
