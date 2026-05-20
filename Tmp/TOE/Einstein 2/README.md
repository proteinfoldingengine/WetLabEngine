# V831 Full Stack Accessibility-Flow Visualization

Cleaned full-stack version of the V831 visualization.

## What changed

- Removed physical-time framing.
- Removed “quantum spin” claim.
- Removed “verification engine” language.
- Uses ordered update slices.
- Computes phase winding from the phase field `theta`, not from `J = -grad(logA)`.
- Keeps gauge correction as a diagnostic, not proof.
- Uses ADM-like / accessibility-flow language.

## Outputs

```text
v831_full_stack_accessibility_flow.mp4
v831_full_stack_accessibility_flow.png
v831_full_stack_diagnostics.csv
```

## Claim boundary

Allowed:

```text
The visualization shows accessibility-flow / conformal / ADM-like response structure across ordered recoverability slices.
```

Not allowed:

```text
physical GR
Einstein equations
actual ADM constraints
actual spacetime curvature
quantum spin
physical time evolution
```

## Run

```bash
python v831_full_stack_accessibility_flow.py
```
