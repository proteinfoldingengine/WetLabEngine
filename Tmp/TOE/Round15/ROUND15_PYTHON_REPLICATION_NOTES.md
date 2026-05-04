# Python Replication Notes

## Core idea
The Python used in Round 15 was intentionally simple:
- load extracted CSVs
- normalize the observable arrays
- compute gaps or offsets
- emit JSON and CSV artifacts

## Tier 1 profile scoring template
```python
import pandas as pd
import numpy as np

def score_profile(csv_gas, csv_mass, gas_col, mass_col, r_col="R_kpc_manual_extract"):
    gas = pd.read_csv(csv_gas).dropna(subset=[r_col, gas_col]).copy()
    mass = pd.read_csv(csv_mass).dropna(subset=[r_col, mass_col]).copy()

    gas = gas.sort_values(r_col)
    mass = mass.sort_values(r_col)

    shared_r = np.array(sorted(set(gas[r_col].tolist()) & set(mass[r_col].tolist())))
    if len(shared_r) == 0:
        raise ValueError("No shared radii")

    g = np.interp(shared_r, gas[r_col], gas[gas_col])
    m = np.interp(shared_r, mass[r_col], mass[mass_col])

    g_norm = g / g.max()
    m_norm = m / m.max()
    gaps = np.abs(g_norm - m_norm)

    mean_gap = float(gaps.mean())
    max_gap = float(gaps.max())

    if mean_gap < 0.10:
        verdict = "positive_signal"
    elif mean_gap < 0.25:
        verdict = "neutral"
    else:
        verdict = "destructive_failure"

    return {
        "shared_r": shared_r.tolist(),
        "mean_abs_norm_gap": mean_gap,
        "max_abs_norm_gap": max_gap,
        "verdict": verdict,
    }
```

## Tier 2 offset scoring template
```python
import numpy as np

def offset_kpc(xg, yg, xm, ym):
    return float(np.sqrt((xg - xm)**2 + (yg - ym)**2))

main = offset_kpc(xg_main, yg_main, xm_main, ym_main)
sub  = offset_kpc(xg_sub,  yg_sub,  xm_sub,  ym_sub)

if main >= 30.0 and sub >= 30.0:
    verdict = "positive_signal"
elif main >= 30.0 or sub >= 30.0:
    verdict = "neutral"
else:
    verdict = "destructive_failure"
```

## Bullet table-calibrated example
Round 15 used the page-8 offset table as a hardening step.
The logic was:
1. read the published arcmin offsets,
2. convert arcmin to kpc with page-derived map scale,
3. compute gas–mass separations,
4. classify the result.

## Artifact patterns
Every scored step produced:
- a score JSON
- a scoreable CSV
- a classification JSON
- and sometimes a checkpoint JSON

That artifact discipline matters. It makes every step inspectable.
