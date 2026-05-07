# Heat Operator Stability + Window Calibration

## Diagnosis from the modal-library run

The theorem did not cleanly fail. The heat-side operator/window failed first.

Symptoms:

- flat trace slopes were not smoothly scaling across N
- many N=12 delta trace slopes approached zero
- several delta trace slopes changed sign
- C and q became dominated by small-denominator artifacts

## Next target

Before more geometry tests, freeze the heat operator.

The campaign compares:

- raw graph Laplacian
- dx-normalized graph Laplacian
- degree-normalized graph Laplacian
- volume-scaled dx-normalized trace

across short, medium, and long heat windows.

## What to send back

```text
HEAT OPERATOR STABILITY SUMMARY
OPERATOR_SUMMARY
GEOMETRY_FITS
```
