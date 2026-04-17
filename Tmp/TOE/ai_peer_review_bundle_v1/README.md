# AI Peer Review Bundle v1
## Restricted Affine Coupling Program

This bundle contains the current peer-review packet for the Restricted Affine Coupling Program.

## What is inside

### 1. Core report
- `AI_PEER_REVIEW_REPORT.md`
  - progress report for AI peer review
  - current theorem shape
  - remaining proof gap
  - explicit review questions

### 2. Current theorem packet
- `THEOREM_PACKET_V27.md`
  - latest integrated theorem packet
  - restricted theorem hierarchy
  - operational defaults
  - domain separation
  - current honest status

### 3. Calibration materials
- `CALIBRATION_RUNBOOK.md`
- `CALIBRATION_SCAFFOLD.py`
- `DIRECT_RUNNER.py`
- `DIRECT_RUNNER_README.md`
- `DATA_CONTRACT.md`

These files define the numerical anchoring and calibration workflow.

### 4. Input templates
- `BASELINE_ANCHOR_TEMPLATE.json`
- `SCREENED_FAMILY_TEMPLATE.jsonl`
- `SCREENED_FAMILY_TEMPLATE.csv`

These define the expected input format for future real-data calibration runs.

### 5. Constructed calibration dataset
Folder:
- `constructed_calibration_dataset/`

Contents:
- `constructed_baseline_anchor.json`
- `constructed_screened_family.jsonl`
- `README.md`

This is a generated stand-in dataset used to exercise the calibration workflow end to end.
It is not external or measured baseline data.

### 6. Constructed calibration results
Folder:
- `constructed_calibration_results/`

Contents include:
- `anchor_constants.csv`
- `screened_family_calibration.csv`
- `calibration_summary.csv`
- `affine_overlay.png`
- `remainder_vs_bound.png`
- `constructed_calibration_report.md`

These are the first anchored calibration results on the constructed dataset.

## Current strongest claim

The strongest current claim is restricted, not universal:

\[
\Delta \mathrm{Cov} = a_0\,\Delta \mathrm{Var} + b_0 + \epsilon
\]

with \(a_0\) and \(b_0\) arising from baseline residual geometry, and \(\epsilon\) controlled by gain drift, response curvature, and innovation scale.

## Current honest status

- theorem shape: stabilized in restricted form
- remaining gap: calibration of constants on screened family
- hard operational default: aggressive + high-coverage
- softer interpretive alternative: aggressive + balanced

## Important scope note

This bundle is suitable for:
- AI peer review
- internal technical review
- reproducibility-oriented discussion

This bundle is not claiming:
- universal proof
- final closure
- external-data calibration

The constructed calibration materials are included to validate the workflow and anchor the next phase of work.

