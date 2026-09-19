# UQCF-GEM v15.39 — Higher-Incidence Source Axioms

## Result

The frozen finite canary returns

```text
AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL
```

Exactly one of the three preregistered response axioms survives the common adversarial test:

| Candidate | Frozen formula | Mechanical verdict |
|---|---|---|
| Direct inheritance | `y = kappa` | `STRUCTURAL_ONLY_LOCAL` |
| One-incidence transport | `y = A kappa` | `STRUCTURAL_ONLY_LOCAL` |
| Global balance completion | `(4I-A)y = kappa` on `im(B2)` | `PRETIME_GLOBAL_ORGANIZATION_SURVIVES` |

This is a conditional signal of life inside explicitly new source and response axioms. It is not a
derivation of gravity, a continuum limit, an Einstein-equation result, or a scientific
breakthrough. Pillar 3 remains **OPEN**.

The authoritative machine-readable ledger is [`docs/RESULTS.json`](docs/RESULTS.json).

## Explicit new source semantics

For an oriented parent-face occurrence `(f,e,a)`, v15.39 adds

```text
delta = a e_e
q = B1 delta
sigma = (B2)_(e,f)
kappa = a sigma B2 e_f
```

Thus `kappa in im(B2) subset ker(B1)`. Parent-face provenance is physical input in this model;
it is not recovered from the frozen coarse charge `q`.

That addition changes the meaning of a complete oriented face boundary. Its coarse charge still
vanishes, while its higher-incidence source does not:

```text
q_total = 0
kappa_total = 4 B2 e_f
```

This is an ontology concession, not a theorem derived from v15.38 or earlier.

## Exact finite result

All quantities below are exact rational values. Each value is the same for all four preregistered
edge-occurrence orientations of the source face.

| L | Maximum torus face distance | Global-balance `S_remote` | Global-balance `C_remote` |
|---:|---:|---:|---:|
| 5 | 4 | `2/625` | `1/1562500` |
| 7 | 6 | `2/2401` | `1/23059204` |
| 9 | 8 | `2/6561` | `1/172186884` |
| 11 (locked holdout) | 10 | `2/14641` | `1/857435524` |

For direct inheritance and one-incidence transport, both observables are exactly zero at every
required size and orientation. Those candidates pass the structural checks but remain local.

For global balance completion, the inverse is taken only on the canonical boundary sector. No
ambient pseudoinverse, minimum-norm rule, Hodge selector, spectral-edge tuning, fitted threshold,
or gravity target fit is used.

## What the computation establishes

Within the frozen finite model and the two explicit new axiomatic layers, the exact audit verifies:

- source typing, `B1 kappa = 0`, translation/D4 covariance, sign reversal, and additivity;
- a unique exact global-balance response on the canonical boundary sector;
- exact compatibility for projective scales `lambda = 1` and `7/3`;
- positive far-shell support and positive noncommuting-axis precursor for global balance at
  `L=5,7,9,11`;
- zero commuting-axis precursor and all preregistered hostile controls;
- unchanged formulas on the locked `L=11` holdout;
- zero spectrum queries, zero spectral-edge parameters, zero candidate-specific thresholds, and
  zero gravity-fit parameters.

The computation does not derive the higher-incidence source rule or select/adopt a physical
response axiom. It tests the consequences of the frozen candidates. The full SU(2) holonomy,
continuum behavior, geometry correspondence, Newtonian limit, and Einstein dynamics remain
unevaluated.

## Reproduction

From this directory:

```bash
python -m unittest -v test_gate.py
python source_axiom_canary.py --check docs/RESULTS.json
python -m compileall -q source_axiom_canary.py test_gate.py
```

The GitHub Actions gate additionally runs the inherited v15.37 and v15.38 frontier regressions,
verifies that every branch change is additive relative to
`825b47b276c6a17df35e6620f6de6630a1d729e2`, and requires byte-identical replay of the result
ledger.

## Preregistration receipts

- design freeze: `c71d16ead84620a9d3ac8762c3feb59e5be5c487`;
- intended RED run: Actions run `35452558930`, job `105922134054`, head
  `f5548eb73991705d36349ebe1afa550c4eb207d1`;
- RED failure: `ModuleNotFoundError: No module named 'source_axiom_canary'`;
- finite sizes: `L=5,7,9`; locked holdout: `L=11`;
- next required object:
  `INDEPENDENT_GEOMETRY_AND_CORRESPONDENCE_TESTS_FOR_FROZEN_AXIOM_SURVIVOR`.

No candidate or criterion was changed after observing the canary.
