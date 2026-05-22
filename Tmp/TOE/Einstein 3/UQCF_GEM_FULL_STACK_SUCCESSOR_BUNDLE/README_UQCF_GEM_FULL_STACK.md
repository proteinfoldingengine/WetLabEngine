# UQCF-GEM Full-Stack Successor Runner

## What this is

A standalone Python runner for the Recoverability Accessibility / ADM-like same-slice constraint empirical stack.

It runs:

1. Ordered-update accessibility-flow simulation
2. Accessibility density `A`
3. Potential `psi = log(A)`
4. ADM-like scalar and momentum analog quantities
5. Flow-frame momentum decomposition
6. Compact law fitting
7. Frozen transfer tests
8. Shuffled and bad-frame falsification
9. Resolution scaling
10. Markdown/JSON/CSV outputs

## What this is NOT

This does not prove:

- General Relativity
- Einstein equations
- physical spacetime curvature
- continuum closure
- ontology of reality

Use the phrase **ADM-like same-slice constraint analog**.

## Install

```bash
pip install numpy pandas tabulate
```

`tabulate` is only needed for markdown table output from pandas.

## Run

```bash
python uqcf_gem_full_stack_runner.py --outdir runs/v832_full_stack
```

Optional:

```bash
python uqcf_gem_full_stack_runner.py --operator-order 4 --train-nx 32 --seed 832 --outdir runs/v832_order4
```

## Outputs

Inside the output directory:

- `FULL_STACK_REPORT.md`
- `full_stack_results.json`
- `frozen_compact_flow_frame_law.json`
- `transfer_scores.csv`
- `transfer_summary.csv`
- `transfer_compatibility.csv`
- `resolution_scaling_scores.csv`
- `resolution_scaling_summary.csv`

## Expected qualitative outcome

A healthy run should show:

- True compact law transfer significantly better than rotated-frame and shuffled controls.
- Momentum law highly specific to the accessibility-flow frame.
- Resolution scaling that improves somewhat with grid refinement, but does not claim zero continuum residual.
- Strong empirical support for ADM-like same-slice analogs without claiming physical GR.

## Successor AI instructions

Do not continue feature hunting unless you have a principled mathematical reason.

Priority next work:

1. Variational derivation
2. Boundary/operator analysis
3. Graph/non-Cartesian mesh tests
4. Spectral or Green-function operators
5. Claim-hardening for publication

Mandatory guardrail:

The update index is ordered recoverability sequence, not physical time.
