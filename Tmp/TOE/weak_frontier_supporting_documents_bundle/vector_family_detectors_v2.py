
from dataclasses import dataclass
from typing import Literal

VectorSubclass = Literal[
    "coherent_rotational_directional",
    "multifrequency_directional",
    "weak_signal_multifrequency",
    "transient_boundary_directional",
    "switching_boundary_directional",
    "noisy_scalar_like",
    "unclassified",
]

@dataclass
class DirectionalFeatures:
    winding_mean: float
    mean_vel_mean: float
    std_vel_mean: float
    mean_acc_mean: float
    std_acc_mean: float
    monotonicity_mean: float
    sign_change_rate_mean: float
    peak_ratio_mean: float
    spectral_entropy_mean: float
    effective_modes_mean: float
    dominant_fraction_mean: float

def detect_coherent_rotational(f: DirectionalFeatures) -> bool:
    return (
        f.winding_mean > 15
        and f.monotonicity_mean > 0.90
        and f.sign_change_rate_mean < 0.08
        and f.std_acc_mean < 0.60
    )

def detect_multifrequency(f: DirectionalFeatures) -> bool:
    return (
        f.dominant_fraction_mean > 0.15
        and f.effective_modes_mean < 19.0
        and f.sign_change_rate_mean < 0.40
    )

def detect_weak_signal_multifrequency(f: DirectionalFeatures) -> bool:
    """
    Intended to catch blurred or weak multifrequency structure that sits
    between clean multifrequency and noisy contrast.
    """
    return (
        0.10 < f.dominant_fraction_mean <= 0.15
        and 19.0 <= f.effective_modes_mean <= 20.5
        and 0.30 <= f.sign_change_rate_mean <= 0.55
        and 0.60 <= f.std_acc_mean <= 1.10
        and f.monotonicity_mean < 0.80
    )

def detect_transient_boundary(f: DirectionalFeatures) -> bool:
    return (
        f.monotonicity_mean > 0.90
        and 0.08 < f.sign_change_rate_mean < 0.30
        and f.std_acc_mean < 0.80
    )

def detect_switching_boundary(f: DirectionalFeatures) -> bool:
    """
    Intended to catch cases with strong directional structure, but with
    episodic switching that prevents clean rotational or multifrequency assignment.
    """
    return (
        f.monotonicity_mean > 0.88
        and 0.20 <= f.sign_change_rate_mean <= 0.45
        and 0.75 <= f.std_acc_mean <= 1.30
        and f.dominant_fraction_mean < 0.15
        and f.effective_modes_mean >= 19.0
    )

def detect_noisy_scalar_like(f: DirectionalFeatures) -> bool:
    return (
        f.sign_change_rate_mean > 0.30
        and f.std_acc_mean > 0.80
    )

def classify_vector_subclass(f: DirectionalFeatures) -> VectorSubclass:
    if detect_coherent_rotational(f):
        return "coherent_rotational_directional"
    if detect_multifrequency(f):
        return "multifrequency_directional"
    if detect_weak_signal_multifrequency(f):
        return "weak_signal_multifrequency"
    if detect_switching_boundary(f):
        return "switching_boundary_directional"
    if detect_transient_boundary(f):
        return "transient_boundary_directional"
    if detect_noisy_scalar_like(f):
        return "noisy_scalar_like"
    return "unclassified"
