# UQCF-GEM v15.41 — Formal Connection, Curvature, and Source Correspondence

## Mechanical result

```text
CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE
```

At each frozen size `L=5,7,9,11`, the response-only square complex has tangent rank two, the
baseline connection has one local-`D4` gauge orbit, and the exact linearized Cartan system has full
column rank with zero residual. The admissible local equivariant curvature contraction space has
dimension one. However, the mechanically differentiated holonomy is exactly zero on the complete
source orbit, so its centered contraction cannot equal `alpha_L s_f` for any required nonzero
`alpha_L`. The preregistered route therefore closes without tuning.

| `L` | Cartan coefficient rank | Augmented rank | Nullity | Contraction dimension | Curvature | Correspondence |
|---:|---:|---:|---:|---:|---|---|
| 5 | 50 | 50 | 0 | 1 | exactly zero | false |
| 7 | 98 | 98 | 0 | 1 | exactly zero | false |
| 9 | 162 | 162 | 0 | 1 | exactly zero | false |
| 11 | 242 | 242 | 0 | 1 | exactly zero | false |

All 80 family/scale/relabel/size cells are recorded. The four inherited control families do not
pass the complete gate, the two asymmetric scrambles fail correspondence, exact superposition is
verified, and the locked `L=11` holdout uses the unchanged construction.

## Boundary of the result

This is a finite exact result for a new formal discrete candidate class, conditional on the frozen
v15.39 source and response axioms and the v15.40 operational metric. It is not a physical affine
connection, spacetime curvature, a stress-energy law, a continuum result, a Newtonian limit,
Einstein dynamics, or a scientific breakthrough. Historical retained connection and holonomy
artifacts are not used in adjudication. Pillar 3 remains `OPEN`.

The inherited base is exact commit `84aa1c81fd86ac4d7a06015482f98572f3afc05f`. Every v15.40
input blob is hash-pinned in `response_inputs.py`; the exact v15.41 GitHub Actions head, run, job,
test counts, and pull-request state are recorded in the implementation plan's execution receipts.

## Reproduce

From this directory:

```bash
python -m unittest -v test_operational_complex.py test_linearized_connection.py test_gate.py
python connection_curvature_gate.py --check docs/RESULTS.json > /tmp/v1541-results.json
cmp docs/RESULTS.json /tmp/v1541-results.json
python -m compileall -q exact_algebra.py response_inputs.py operational_complex.py linearized_connection.py source_target.py connection_curvature_gate.py test_operational_complex.py test_linearized_connection.py test_gate.py
```

The authoritative machine-readable ledger is `docs/RESULTS.json`.
