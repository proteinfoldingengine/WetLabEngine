
# Windowed Instability Detector for Weak Multifrequency

## New idea
Weak multifrequency should not be separated from noisy contrast only by global spectral richness.

It should also require lower **windowed instability**.

## New windowed instability features
- windowed_mean_sign_change
- windowed_mean_phase_resets
- windowed_mean_std_ddang

## Current intended role
These features are used specifically inside the weak_signal_multifrequency detector to prevent:
- degraded noisy contrast
from
being mistaken for
- weak but still structured multifrequency

## Current heuristic thresholds
- windowed_mean_sign_change < 0.57
- windowed_mean_phase_resets < 6.1
- windowed_mean_std_ddang < 1.15

These were chosen to separate the recent:
- exotic_weak_multifreq_a
from
- exotic_weak_multifreq_b

## Next step
Run rescue-vs-regression again on:
- recent weak multifrequency misses
- noisy contrast neighbors
- preserved clean cases
