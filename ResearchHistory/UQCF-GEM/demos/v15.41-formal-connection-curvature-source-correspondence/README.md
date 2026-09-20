# UQCF-GEM v15.41 — Transport-Protocol Erratum

## Mechanical result

```text
PROTOCOL_INVALID
```

The frozen v15.41 transport protocol did not type its transported objects, matrix actions, and
variation sign precisely enough to adjudicate the intended connection question. The corrected gate
therefore stops before connection identifiability, curvature-map identifiability, source
correspondence, or controls are evaluated.

The next required object is:

```text
REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION
```

Pillar 3 remains `OPEN`.

## Protocol defect

The literal frozen tangent-vector reading transports later edge vectors back to the cycle base point
with reverse directed transports while retaining the positive variation
`delta_v_i = +(u[x_i]/2) v_i`. Exact manufactured nonconstant-field audits give:

| `L` | Unknowns | Coefficient rank | Augmented rank | Result |
|---:|---:|---:|---:|---|
| 5 | 50 | 50 | 51 | inconsistent |
| 7 | 98 | 98 | 99 | inconsistent |

Rank mismatch is treated as a protocol defect. The implementation does not reverse the sign, choose
a dual convention, or select the previously executed forward convention after observing output.

## Non-adjudicating theorem

The prior executed forward/positive convention is retained only under
`NON_ADJUDICATING_PROTOCOL_DIAGNOSTIC`. In that formal ansatz, exact local closure forces
alternating rotational coefficients around each square, the rotational circulation vanishes, and
the scalar contribution telescopes. Thus differentiated face holonomy is zero for every tested
exact scalar field.

The exact periodic-carrier parity witnesses are:

| `L` | Rank | Unknowns | Nullity |
|---:|---:|---:|---:|
| 5 | 50 | 50 | 0 |
| 6 | 71 | 72 | 1 |
| 7 | 98 | 98 | 0 |
| 8 | 127 | 128 | 1 |
| 9 | 162 | 162 | 0 |

This is a response-independent no-go result for the executed formal ansatz. It is not an
adjudicating v15.41 connection or curvature result.

## Superseded execution receipt

The previous status
`CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE` is preserved in
`docs/RESULTS.json` only as a non-authoritative execution receipt. Its result blob and successful
exact-head GitHub Actions receipts remain recorded for provenance. It does not survive as a
scientific verdict.

## Claim boundary

After correction, v15.41 establishes no adjudicating connection, curvature, or source-curvature
correspondence. It does not establish a physical affine connection, spacetime curvature,
stress-energy, Newtonian gravity, Einstein dynamics, a continuum limit, or a scientific
breakthrough. The diagnostic theorem is neither evidence for nor evidence against physical gravity.

A replacement transport protocol requires a separately reviewed design and implementation plan and
must pass a preregistered manufactured nonflat conformal-field control before source correspondence
is evaluated.

## Reproduce

From this directory:

```bash
python -m unittest -v test_operational_complex.py test_linearized_connection.py test_gate.py
python connection_curvature_gate.py --check docs/RESULTS.json > /tmp/v1541-erratum-results.json
cmp docs/RESULTS.json /tmp/v1541-erratum-results.json
python -m compileall -q \
  exact_algebra.py response_inputs.py operational_complex.py \
  linearized_connection.py source_target.py connection_curvature_gate.py \
  test_operational_complex.py test_linearized_connection.py test_gate.py
```

The authoritative machine-readable ledger is `docs/RESULTS.json`.
