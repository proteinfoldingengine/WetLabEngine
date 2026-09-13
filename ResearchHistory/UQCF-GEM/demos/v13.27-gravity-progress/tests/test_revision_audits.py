import numpy as np

from uqcf_demo.linalg import raw_orthogonal_polar, proper_orthogonal_polar, so3_angle_audit
from uqcf_demo.quantum import build_default_model, state_at_lambda
from uqcf_demo.geometry import geometry_snapshot


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
