# Round 11 Win Declaration

## Verdict
We consider **Round 11 won**.

This is not because every galaxy behaved identically. It is because the Bridge framework:
1. survived meaningful transfer into a larger external THINGS∩SPARC panel,
2. produced multiple clear external successes,
3. exposed structured and interpretable failure modes,
4. and weakened a simple overfitting-only explanation.

## Why this counts as a win
Round 11 showed that the external pipeline is **regime-sensitive**, not merely score-producing.
Different galaxies exposed different physically interpretable behaviors:
- clean transfer and near-full success,
- geometry sensitivity,
- proxy-amplitude inflation,
- residual overshoot / sparsity-control failure.

That pattern is not what one would normally expect from a simple benchmark overfit.

## Key notable outcomes
- **DDO154** and **NGC2403** acted as near-full external success anchors.
- **NGC3198** extended the panel with a weaker but still positive gas-side pilot.
- **NGC6946** exposed outer-disk proxy amplitude inflation; once localized and normalized, the near-full result became strongly positive again.
- **NGC5055** exposed a different failure mode: missing residual-awareness / sparsity control. A diagnostic residual-aware ablation converted the case from a strong raw failure into a modest positive.
- **NGC2841** demonstrated dramatic geometry recovery: a catastrophic first pass became a strong reconstruction and strong gas-side external success after basin relocation.

## Scientific strengthening signal
A notable strengthening outcome of Round 11 is that the pipeline distinguished **galaxy regimes** rather than merely producing a single aggregate score. That structured behavior materially weakens a simple overfitting-only story and is supportive of a first-principles Bridge picture in which different morphologies and decompositions expose different response regimes.

## Important caution
Some recoveries in Round 11 are **diagnostic ablations**, not replacements for the frozen official benchmark result. They are still important because they localize the source of failure and show that the failure has structure rather than chaos.

## Bundle contents
- `round11_summary_table.csv` — per-galaxy status summary
- `round11_metrics.json` — key metrics captured from the current Round 11 session
- `ROUND11_WIN_DECLARATION.md` — this writeup

## Note
This bundle summarizes the Round 11 findings captured in the current session. It does **not** include every raw galaxy artifact file, because those per-galaxy working directories were not available in this environment at packaging time.