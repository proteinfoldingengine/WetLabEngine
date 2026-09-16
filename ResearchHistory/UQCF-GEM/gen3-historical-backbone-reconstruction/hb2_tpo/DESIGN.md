# Gen3 HB2 — Torsional Pre-Organization Reconstruction and Validation Design

Date: 2026-09-16
Status: design checkpoint; measurement-only first

## Purpose

Test the historical TPO/Goldilocks hypothesis independently of the now-closed Patch-630 general contact-graph hypothesis.

Historical source defines two pre-relaxation torsional observables on true N-CA-C backbone geometry:

1. 2D phi/psi histogram entropy (`calculate_torsion_entropy`), lower interpreted as more torsionally organized;
2. RMS angular distance to the nearest canonical alpha or beta Ramachandran basin (`calculate_phi_psi_rms_to_basins`), lower interpreted as closer to canonical local backbone basins.

The historical V3 Goldilocks ranking then combined geometry/topology (Rg sweet spot + Betti1 threshold) with these torsional metrics and compared rankings with later `final_RMSD`.

## Key scientific correction

The historical composite Goldilocks score contains tunable normalization constants and an Rg/Betti filter. Therefore HB2 must not begin by validating the composite score. It must first test the raw TPO observables independently:

- torsion entropy;
- RMS-to-basin;
- then assess incremental predictive value beyond initial Rg and Betti1.

## HB2-1 historical reproduction

Recompute the historical torsional metrics from seed-generated full backbones and verify agreement with preserved ranked CSV artifacts, especially the 1QYS V3 dataset. This is a measurement reproduction, not a folding claim.

## HB2-2 predictive audit

Using complete preserved seed scans where both initial metrics and later final_RMSD exist, test whether pre-relaxation torsion entropy and RMS-to-basin predict subsequent final_RMSD.

Report:

- Spearman rank correlation for each raw metric vs final_RMSD;
- partial/incremental association after initial Rg and Betti1;
- top/bottom quantile outcome differences;
- all seeds, not selected examples.

No score weights may be retuned after looking at outcomes.

## HB2-3 held-out validation

If raw TPO metrics show predictive signal in historical data, preregister thresholds/model on one dataset and test on a different protein without retuning. A held-out failure closes the general TPO-predictor hypothesis; no rescue campaign.

## Promotion rule

TPO may enter Gen3 only as a measurement/control feature unless it demonstrates reproducible held-out predictive value beyond simpler initial-state descriptors. Even then, promotion to an active force requires a separate causal intervention gate.

## Historical source anchors

- `torsional_metrics.py` blob `0aee35076a59805aa4f99897d7c662b943051ebe`
- `temp/Tmp-rank_seeds_v3.py` blob `54c35f5cc7cb0175ef4808944878d563b0b6ef79`
- `deep_scan_results/1QYS/deep_scan_results_1QYS_v3_ranked.csv` blob `b4afb9d890a5b88aa456b84b0a3f7a6f74c0e6e6`

## Boundary

HB2 does not revive QIS and does not reopen the contact-graph mechanism. It asks a separate prospective question: whether measurable pre-relaxation backbone torsional organization contains information about later foldability.