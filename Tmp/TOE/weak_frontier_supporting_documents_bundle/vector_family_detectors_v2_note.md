
# Weak-Signal Multifrequency Detector and Switching-Boundary Detector

## New detectors added

### weak_signal_multifrequency
This detector is meant for blurred multifrequency cases that are:
- too weak to satisfy the clean multifrequency detector
- but still more structured than noisy contrast

Current intended signature:
- moderate dominant spectral fraction
- slightly elevated effective mode count
- moderate sign-change rate
- moderate acceleration variance
- lower monotonicity than boundary-style states

### switching_boundary_directional
This detector is meant for cases with:
- strong directional structure
- but episodic switching or instability
- too unstable for clean rotational closure
- and too structured for noisy contrast

Current intended signature:
- high monotonicity
- moderate-to-high sign-change rate
- elevated acceleration variance
- low spectral concentration
- high effective mode count

## Current scientific role

These detectors should be inserted between the current clean subclass detectors and the generic noisy/boundary fallback logic.

## Next step

Test these detectors on:
- weak multifrequency blur
- switching boundary blur
- fresh mixed out-of-suite families
