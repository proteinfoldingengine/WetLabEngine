import numpy as np


SEED = 1328
TRIALS = 256
SCALES = [0.2, 0.5, 2.0, 5.0, 11.0]


def _relative_error(actual, expected):
    den = max(float(np.linalg.norm(expected)), 1e-30)
    return float(np.linalg.norm(actual - expected) / den)


def _unit(x):
    n = float(np.linalg.norm(x))
    if n <= 1e-30:
        raise ValueError("zero candidate vector in audit")
    return x / n


def candidate_metadata():
    return {
        "genesis_measure_support": {
            "geometry_side_weight": 0,
            "source_side_weight": 1,
            "candidate_output_weight": 1,
            "calibrated_negative_weight_object_present": False,
            "type_embedding": "NOT_SELECTED_BY_GRADE_OR_MEASURE",
            "reason": "retained measure/support localizes a degree-one source amount but does not remove its positive scale or select a coframe tensor map",
        },
        "pgrl_bkm": {
            "geometry_side_weight": 0,
            "source_side_weight": 1,
            "candidate_output_weight": 1,
            "calibrated_negative_weight_object_present": False,
            "type_embedding": "STATE_TANGENT_DUALITY_ONLY",
            "reason": "BKM duals and norms inherit source amplitude; normalization removes amplitude and leaves projective information",
        },
        "resa_solder_coframe": {
            "geometry_side_weight": 0,
            "source_side_weight": 1,
            "candidate_output_weight": 1,
            "calibrated_negative_weight_object_present": False,
            "type_embedding": "CONDITIONAL_ON_SUPPLIED_SOLDER",
            "source_to_solder_lift_unique": False,
            "reason": "a supplied solder can map type but carries no inverse source scale, and upstream v13.11 shows the source-to-solder tangent is nonunique",
        },
        "qmar_response_covariance": {
            "geometry_side_weight": 0,
            "source_side_weight": 1,
            "candidate_output_weight": 1,
            "calibrated_negative_weight_object_present": False,
            "type_embedding": "GEOMETRIC_RESPONSE_NOT_STRESS_SOURCE",
            "reason": "QMAR is covariant and source-linear, so covariance constrains form but does not select an absolute coefficient",
        },
    }


def _candidate_maps(source, K, measure, maps):
    E, B, R, Q = maps
    return {
        "genesis_measure_support": measure * (E @ source),
        "pgrl_bkm": B @ (K @ source),
        "resa_solder_coframe": R @ source,
        "qmar_response_covariance": Q @ source,
    }


def run_audit():
    rng = np.random.default_rng(SEED)
    max_relative_linear_scaling_error = 0.0
    max_normalized_direction_drift = 0.0
    max_relative_bkm_quadratic_scaling_error = 0.0
    max_relative_inverse_weight_positive_control_error = 0.0
    minimum_baseline_candidate_norm = float("inf")

    for _ in range(TRIALS):
        source = rng.normal(size=5)
        A = rng.normal(size=(5, 5))
        K = A.T @ A + 0.5 * np.eye(5)
        measure = 0.5 + float(rng.random())
        maps = (
            rng.normal(size=(4, 5)),
            rng.normal(size=(5, 5)),
            rng.normal(size=(6, 5)),
            rng.normal(size=(7, 5)),
        )

        baseline = _candidate_maps(source, K, measure, maps)
        for vec in baseline.values():
            minimum_baseline_candidate_norm = min(
                minimum_baseline_candidate_norm, float(np.linalg.norm(vec))
            )

        q0 = float(source @ K @ source)
        for scale in SCALES:
            scaled = _candidate_maps(scale * source, K, measure, maps)
            for name, vec0 in baseline.items():
                veca = scaled[name]
                expected = scale * vec0
                max_relative_linear_scaling_error = max(
                    max_relative_linear_scaling_error,
                    _relative_error(veca, expected),
                )
                max_normalized_direction_drift = max(
                    max_normalized_direction_drift,
                    float(np.linalg.norm(_unit(veca) - _unit(vec0))),
                )

                # Positive control: an explicitly supplied object of weight -1
                # cancels the source weight.  This is deliberately an added
                # calibration, not something claimed to exist in the ontology.
                g0 = 1.7
                calibrated_actual = (g0 / scale) * veca
                calibrated_expected = g0 * vec0
                max_relative_inverse_weight_positive_control_error = max(
                    max_relative_inverse_weight_positive_control_error,
                    _relative_error(calibrated_actual, calibrated_expected),
                )

            qa = float((scale * source) @ K @ (scale * source))
            expected_q = (scale**2) * q0
            max_relative_bkm_quadratic_scaling_error = max(
                max_relative_bkm_quadratic_scaling_error,
                abs(qa - expected_q) / max(abs(expected_q), 1e-30),
            )

    metadata = candidate_metadata()
    verdicts = {
        name: "OBSTRUCTED"
        for name, item in metadata.items()
        if item["candidate_output_weight"] > 0
        and not item["calibrated_negative_weight_object_present"]
    }
    if set(verdicts) != set(metadata):
        raise AssertionError("candidate adjudication incomplete")

    return {
        "seed": SEED,
        "trials": TRIALS,
        "scales": list(SCALES),
        "candidate_count": len(metadata),
        "candidate_metadata": metadata,
        "candidate_verdicts": verdicts,
        "max_relative_linear_scaling_error": float(max_relative_linear_scaling_error),
        "max_normalized_direction_drift": float(max_normalized_direction_drift),
        "max_relative_bkm_quadratic_scaling_error": float(max_relative_bkm_quadratic_scaling_error),
        "max_relative_inverse_weight_positive_control_error": float(
            max_relative_inverse_weight_positive_control_error
        ),
        "minimum_baseline_candidate_norm": float(minimum_baseline_candidate_norm),
        "negative_weight_calibration_in_frozen_candidates": False,
        "scale_weight_theorem": (
            "weight-zero geometry contracted with a nonzero weight-one source remains weight one; "
            "removing the scale by normalization leaves only ray/projective information"
        ),
        "gate_outcome": "REQUIRES_NEW_AXIOM",
        "source_to_gr_coupling_branch": "STOPPED_PENDING_NEW_AXIOM_OR_INDEPENDENT_CALIBRATION",
    }
