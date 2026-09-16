# Gen3 HB2 — HB2-1/2 Preregistration

Date: 2026-09-16
Historical dataset: preserved 1QYS V3 ranked deep scan

## Frozen questions

1. Can the historical raw TPO metrics be regenerated from the seed-defined full-backbone initial states?
2. Do initial torsion entropy or initial RMS-to-canonical-basin predict later final_RMSD across the complete preserved scan?
3. Do either add predictive information beyond initial_Rg and initial_Betti1?

## Primary analysis

Use all rows in the preserved 1QYS V3 dataset with finite values. Lower final_RMSD is better.

Report Spearman rho for:

- torsion_entropy vs final_RMSD;
- torsion_rms_dist vs final_RMSD;
- initial_Rg vs final_RMSD;
- initial_Betti1 vs final_RMSD.

For incremental value, residualize each TPO metric and final_RMSD against initial_Rg and initial_Betti1 using a linear nuisance model, then report Spearman correlation of residuals. This is a diagnostic association, not a calibrated predictive model.

Also compare final_RMSD between lowest and highest quartiles of each TPO metric. No thresholds or weights will be tuned after outcomes are inspected.

## Reproduction tolerance

For regenerated historical TPO metrics, compare seed-matched values against the preserved CSV. Differences must be reported; no rounding-based substitution. Exact floating equality is not required because library/runtime versions differ.

## Decision rule

Advance to a held-out TPO validation only if at least one raw TPO metric shows a coherent association with later final_RMSD and retains nontrivial incremental association after Rg/Betti1 adjustment. Otherwise classify historical TPO ranking as unsupported as a general predictor and preserve it only as a historical measurement concept.

No active TPO force will be added in this gate.