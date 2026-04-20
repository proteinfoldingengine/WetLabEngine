
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
class DirectionalFeaturesV3:
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
    # windowed instability additions
    windowed_mean_sign_change: float
    windowed_mean_phase_resets: float
    windowed_mean_std_ddang: float

def detect_coherent_rotational(f: DirectionalFeaturesV3) -> bool:
    return (
        f.winding_mean > 15
        and f.monotonicity_mean > 0.90
        and f.sign_change_rate_mean < 0.08
        and f.std_acc_mean < 0.60
    )

def detect_multifrequency(f: DirectionalFeaturesV3) -> bool:
    return (
        f.dominant_fraction_mean > 0.15
        and f.effective_modes_mean < 19.0
        and f.sign_change_rate_mean < 0.40
    )

def detect_weak_signal_multifrequency(f: DirectionalFeaturesV3) -> bool:
    """
    Cleaned-up weak multifrequency logic:
    require weak spectral concentration PLUS lower windowed instability
    than true noisy contrast.
    """
    return (
        0.10 < f.dominant_fraction_mean <= 0.15
        and 19.0 <= f.effective_modes_mean <= 20.5
        and 0.30 <= f.sign_change_rate_mean <= 0.60
        and 0.60 <= f.std_acc_mean <= 1.20
        and f.monotonicity_mean < 0.80
        and f.windowed_mean_sign_change < 0.57
        and f.windowed_mean_phase_resets < 6.1
        and f.windowed_mean_std_ddang < 1.15
    )

def detect_switching_boundary(f: DirectionalFeaturesV3) -> bool:
    return (
        f.monotonicity_mean > 0.88
        and 0.20 <= f.sign_change_rate_mean <= 0.45
        and 0.75 <= f.std_acc_mean <= 1.30
        and f.dominant_fraction_mean < 0.15
        and f.effective_modes_mean >= 19.0
    )

def detect_transient_boundary(f: DirectionalFeaturesV3) -> bool:
    return (
        f.monotonicity_mean > 0.90
        and 0.08 < f.sign_change_rate_mean < 0.30
        and f.std_acc_mean < 0.80
    )

def detect_noisy_scalar_like(f: DirectionalFeaturesV3) -> bool:
    return (
        f.sign_change_rate_mean > 0.30
        and f.std_acc_mean > 0.80
    )

def classify_vector_subclass_v3(f: DirectionalFeaturesV3) -> VectorSubclass:
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
