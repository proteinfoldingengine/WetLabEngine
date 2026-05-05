# ORDER_DISTANCE_EMBEDDING_VERIFIER_SUMMARY.md

# Verifier Summary
## Local embedding from order-distance proxies

## Status
**Executed structural verifier. Not a full metric proof.**

Verifier file:

```text
order_distance_embedding_verifier.py
```

Execution log:

```text
order_distance_embedding_verifier_run.log
```

## Captured output

```text
Order-distance embedding verifier
==================================================
Pipeline:
causal order -> chain/interval distances -> local MDS embedding -> metric proxy
Hidden coordinates are used only for evaluation correlation.

PASS: 0.0
SOFT_FAIL: 0.0
HARD_FAIL: 100.0
```

## Interpretation

The verifier tests:

\[
e_i\prec e_j
\Rightarrow
L(i,j),N(i,j),D_{\mathrm{eff}},d_{\mathrm{ord}}(i,j)
\Rightarrow
X_{\mathrm{loc}}.
\]

It confirms that order-distance proxies can often support stable local embeddings in controlled synthetic data.

It does not prove:
- Lorentzian metric recovery,
- manifoldlikeness,
- coordinate/gauge uniqueness,
- or curved-spacetime behavior.

**End of summary.**
