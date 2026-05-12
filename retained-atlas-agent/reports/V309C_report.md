# V309C — Regime redesign and nondegenerate component ablation

## Question
Can the reachability-law ablation be placed into a regime with usable score variance and enough bad cases for interpretation?

## Hypothesis
If the harness is valid, then redesigning the regime toward a bad rate in the 0.20–0.40 range should produce nonzero score variance, nonzero trigger rate, and enough positive bad cases for component ablation to distinguish the full score from one-component ablations.

## Method
Executed a fixed-seed toy simulation across seeds 0–19 with a small severity sweep. The chosen severity was `0.8`. Reported:
- `A_full`
- `no_rf`
- `no_cw`
- `no_be`
- `no_dr`
- `no_rv`

Tracked:
- `bad_rate`
- `adaptive_rate`
- `trigger_rate`
- `AUC`
- `balanced_accuracy`
- `accuracy`
- `score_mean`
- `score_var`
- `mean_bad`
- `mean_safe`
- `corr`
- `phase_counts`
- `validity_gate`

## Controls
- Fixed seeds 0–19
- Shared configuration across variants
- Same train/test split for ablation metrics
- No threshold tuning after validation
- Regime sweep used only to try to enter a non-degenerate bad-rate window

## Results
Sweep:
- severity `0.8`: `bad_rate` `0.43`, `score_var` `0.0021934775336681276`, `trigger_rate` `0.4`, `valid_for_interpretation` `false`
- severity `1.0`: `bad_rate` `0.43666666666666665`, `score_var` `0.003443656356996739`, `trigger_rate` `0.4`, `valid_for_interpretation` `false`
- severity `1.2`: `bad_rate` `0.44583333333333336`, `score_var` `0.005204568983101478`, `trigger_rate` `0.4`, `valid_for_interpretation` `false`
- severity `1.4`: `bad_rate` `0.4825`, `score_var` `0.006878488888493234`, `trigger_rate` `0.4`, `valid_for_interpretation` `false`
- severity `1.6`: `bad_rate` `0.5141666666666667`, `score_var` `0.009127265710726584`, `trigger_rate` `0.4`, `valid_for_interpretation` `false`

Chosen regime summary:
- `bad_rate`: `0.43`
- `adaptive_rate`: `0.9383333333333334`
- `mean_A_norm`: `1.0898789746371649`
- `min_A_norm`: `0.8713551368202963`
- `score_mean`: `1.0898789746371649`
- `score_var`: `0.0021934775336681276`
- `phase_counts` bad: `516`, safe: `23484`
- `threshold`: `1.1082369593574317`

Validity gate:
- `enough_positive_cases`: `true`
- `nondegenerate_bad_rate`: `false`
- `nonzero_score_variance`: `true`
- `nonzero_trigger_rate`: `true`
- `valid_for_interpretation`: `false`

Ablation results:
- `A_full`: `AUC` `0.397349154540097`, `accuracy` `0.46`, `balanced_accuracy` `0.44492044063647496`, `corr` `-0.20770003318812041`, `mean_bad` `1.078679275368584`, `mean_safe` `1.0983278705766206`, `trigger_rate` `0.4`
- `no_be`: `AUC` `0.3975871526361122`, `accuracy` `0.515`, `balanced_accuracy` `0.4722222222222222`, `corr` `-0.21311198620790095`, `mean_bad` `1.0698542311171175`, `mean_safe` `1.0865430046805986`, `trigger_rate` `0.19833333333333333`
- `no_cw`: `AUC` `0.4013809556190217`, `accuracy` `0.5491666666666667`, `balanced_accuracy` `0.49576703386372906`, `corr` `-0.20171327145085652`, `mean_bad` `1.0619797835677434`, `mean_safe` `1.0780051103308579`, `trigger_rate` `0.11916666666666667`
- `no_dr`: `AUC` `0.40490276077791376`, `accuracy` `0.5483333333333333`, `balanced_accuracy` `0.49289405684754517`, `corr` `-0.19586733785049518`, `mean_bad` `1.0623379277611498`, `mean_safe` `1.0771849264349203`, `trigger_rate` `0.105`
- `no_rf`: `AUC` `0.39837197969082916`, `accuracy` `0.5641666666666667`, `balanced_accuracy` `0.49916700666394664`, `corr` `-0.19842975939822766`, `mean_bad` `1.0493097132167424`, `mean_safe` `1.0642986267096932`, `trigger_rate` `0.035833333333333335`
- `no_rv`: `AUC` `0.4013441225803527`, `accuracy` `0.5325`, `balanced_accuracy` `0.48590711274309806`, `corr` `-0.19832727224268015`, `mean_bad` `1.0680872066625287`, `mean_safe` `1.083349144178982`, `trigger_rate` `0.16916666666666666`

## Interpretation
Inside this toy run, the regime redesign did produce nonzero score variance, nonzero trigger rate, and enough positive bad cases. However, the validity gate still failed because `nondegenerate_bad_rate` was false.

So this is a harness/regime failure, not a valid component-interpretation run. The ablation numbers are present, but the run should not be treated as interpretable evidence for the component law.

## Failure / Caveat
- The target bad-rate window was not reached: the chosen regime had `bad_rate` `0.43`.
- `valid_for_interpretation` was `false`.
- The sweep stayed outside the intended 0.20–0.40 range at the selected regime.
- `AUC` and `balanced_accuracy` were low for the full score.
- No component conclusion should be promoted from this run.

## Decision
branch

## Next
Smallest useful next test: redesign the harness again to land in a valid bad-rate window before attempting component interpretation.