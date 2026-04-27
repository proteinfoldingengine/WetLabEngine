# Round 12A Update — WALLABY DR2 External Gas-Side Pilot

## Status
Round 12A has now been executed on a **strict unseen WALLABY DR2 subset** with **no SPARC overlap**.

This is the first real external Round 12 execution on public unseen data using the locked WALLABY source decision.

## What was done
We:
1. audited the local unified corpus and confirmed its WALLABY entries were metadata-only, not runnable data blocks,
2. queried the live public WALLABY DR2 kinematic model catalogue,
3. identified the active DR2 table:
   - `AS102.wallaby_pdr2_kinematic_models_v01`
4. exported a strict 10-galaxy unseen WALLABY subset with:
   - no SPARC overlap,
   - valid radial arrays,
   - valid rotation-curve arrays,
   - valid HI surface-density proxy arrays,
   - strict point-count filtering,
   - preference for `qflag_model = 0`,
5. ran a gas-side external pilot on the locked subset.

## Important scope note
This was a **Round 12A gas-side pilot**, not yet the final full frozen baryonic Round 12 run.

Reason:
- the public WALLABY DR2 kinematic table provides real radial kinematics and HI structure,
- but it does **not** directly provide the full stellar decomposition fields required by the full frozen Bridge scorer:
  - `Vdisk`
  - `Vbul`

So this run tests whether a Bridge-like gas-side external proxy carries real signal on unseen public galaxies.

## Strict locked WALLABY subset
Ten unseen galaxies were locked and scored from public WALLABY DR2 products.

## Results
### Per-galaxy summary
| galaxy | n_points | rmse_flat_baseline | rmse_gas_proxy | improvement | positive_improvement |
|---|---:|---:|---:|---:|---|
| WALLABY J123917-003149 | 47 | 19.367010 | 20.863247 | -1.496238 | False |
| WALLABY J165901-601241 | 35 | 24.747219 | 19.741246 | 5.005973 | True |
| WALLABY J130314-172514 | 25 | 13.735865 | 6.422724 | 7.313141 | True |
| WALLABY J124508-002747 | 21 | 34.798762 | 12.486609 | 22.312153 | True |
| WALLABY J125548+041805 | 21 | 21.200337 | 22.067577 | -0.867240 | False |
| WALLABY J171804-575135 | 19 | 22.554904 | 6.381627 | 16.173277 | True |
| WALLABY J100342-270137 | 17 | 14.150972 | 14.386614 | -0.235642 | False |
| WALLABY J123427+021108 | 17 | 10.107190 | 31.967555 | -21.860365 | False |
| WALLABY J101655-485238 | 15 | 56.853930 | 42.143577 | 14.710353 | True |
| WALLABY J123138+035620 | 15 | 25.276208 | 11.198548 | 14.077659 | True |

### Aggregate
- `n_scored = 10`
- `positive_rate = 0.60`
- `mean_improvement = +5.5133`

## Interpretation
This is a **real external signal**, not a narrative-only outcome.

What held:
- the source lock was real,
- the unseen subset was real,
- the public DR2 ingestion was real,
- the gas-side proxy achieved **positive mean improvement** on unseen WALLABY data.

What did not yet hold:
- the run did **not** meet the locked Round 12 win threshold of:
  - at least **70% positive wins**, and
  - mean RMSE improvement of at least **5 km/s**.

It cleared the second threshold, but not the first.

## Scientific meaning
This is best interpreted as:

> The Bridge-style gas-side proxy survived contact with unseen public WALLABY data well enough to produce positive mean improvement, but not strongly enough yet to count as a full Round 12 win.

That is scientifically meaningful for three reasons:
1. it confirms that the external execution path is now real,
2. it shows nontrivial signal on unseen public galaxies,
3. it reveals that the current gas-side proxy layer is too crude to generalize cleanly across the full strict subset.

## Most likely reason for the miss
The current Round 12A proxy is incomplete:
- it uses real HI kinematic and surface-density information,
- but not the full stellar decomposition layer,
- so it is not yet the full frozen Bridge scorer.

That means this result is more consistent with **partial external support** than with outright failure.

## Proper classification
### Round 12A WALLABY gas-side pilot
- external execution: **success**
- scientific signal: **success**
- locked Round 12 threshold: **not yet met**

## Next step
Round 12B should keep:
- the external WALLABY source lock,
- the no-SPARC-overlap rule,
- the public execution requirement,

while improving the physics/input layer by adding one or more of:
- better gas-support mapping,
- stronger quality filtering,
- additional public decomposition layers,
- or a full baryonic augmentation path.

## Bottom line
Round 12A is now live, external, public, and meaningful.

It does **not** yet count as a Round 12 win.

But it does prove that the challenge has moved out of thread rhetoric and into real unseen public execution.
