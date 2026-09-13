import numpy as np

from uqcf_demo.linalg import raw_orthogonal_polar, proper_orthogonal_polar, so3_angle_audit
from uqcf_demo.quantum import build_default_model, state_at_lambda
from uqcf_demo.geometry import geometry_snapshot
from uqcf_demo.simulation import default_config, run_telemetry


def test_raw_orthogonal_polar_reports_reflection_before_so3_projection():
    C = np.diag([2.0, 1.0, -0.5])
    Q = raw_orthogonal_polar(C)
    assert np.allclose(Q.T @ Q, np.eye(3), atol=1e-12)
    assert np.linalg.det(Q) < 0

    O = proper_orthogonal_polar(C)
    assert np.linalg.det(O) > 0


def test_so3_angle_audit_exposes_preclip_argument_and_clip_excess():
    O = np.diag([-1.0, -1.0, 1.0])
    audit = so3_angle_audit(O)
    assert np.isclose(audit["raw_cos_argument"], -1.0)
    assert np.isclose(audit["clipped_cos_argument"], -1.0)
    assert np.isclose(audit["angle"], np.pi)
    assert audit["clip_excess"] == 0.0

    perturbed = 1.000000001 * np.eye(3)
    audit2 = so3_angle_audit(perturbed)
    assert audit2["raw_cos_argument"] > 1.0
    assert audit2["clipped_cos_argument"] == 1.0
    assert audit2["clip_excess"] > 0.0


def test_geometry_snapshot_records_raw_polar_determinant_and_preclip_holonomy():
    model = build_default_model()
    snap = geometry_snapshot(model, state_at_lambda(model, 0.0))
    assert snap["edges"]
    assert snap["cycles"]
    assert all("raw_polar_det" in edge for edge in snap["edges"])
    assert all("raw_cos_argument" in cyc for cyc in snap["cycles"])
    assert all("clip_excess" in cyc for cyc in snap["cycles"])


def test_canonical_telemetry_reports_transport_and_holonomy_audits():
    data = run_telemetry(default_config(frames=5))
    summary = data["summary"]
    assert 0 <= summary["raw_polar_reflection_count"] <= 5 * len(data["graph"]["edges"])
    assert 0.0 <= summary["raw_polar_reflection_fraction"] <= 1.0
    assert summary["min_holonomy_raw_cos_argument"] <= summary["max_holonomy_raw_cos_argument"]
    assert summary["holonomy_clip_event_count"] >= 0
    assert summary["max_holonomy_clip_excess"] >= 0.0
    assert summary["pi_holonomy_adjudication"] in {
        "NO_PI_EVENT",
        "GENUINE_PI_WITHIN_TOLERANCE_NO_CLIP",
        "CLIP_SATURATION_PRESENT",
    }
