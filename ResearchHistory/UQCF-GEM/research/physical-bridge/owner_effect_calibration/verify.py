"""Exact matrix replay of the fixed-effect calibration criterion and its controls."""
import json
import sympy as sp


R = sp.Rational
P, U, V = 1, 2, 3
SOURCE_SIZE = 4
EYE = sp.eye(SOURCE_SIZE)
PROJECTOR_P = sp.diag(0, 1, 0, 0)
PROJECTOR_U = sp.diag(0, 0, 1, 0)
Q = EYE - PROJECTOR_U
RHO_PLUS = sp.diag(R(1, 5), R(1, 5), R(2, 5), R(1, 5))
RHO_MINUS = sp.diag(R(1, 5), R(1, 5), R(1, 5), R(2, 5))
DELTA = RHO_PLUS - RHO_MINUS
ZERO, ONE = sp.Matrix([1, 0]), sp.Matrix([0, 1])
H = sp.Matrix([sp.sqrt(R(3, 8)), sp.sqrt(R(5, 8))])
EFFECTS = {
    "overlapping_calibration": (sp.diag(R(7,10), R(3,10)), sp.diag(R(1,5), R(3,5))),
    "separated_calibration": (sp.diag(R(7,10), R(9,10)), sp.diag(R(1,10), R(3,10))),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def equal_matrix(a, b):
    return a.shape == b.shape and all(sp.simplify(x) == 0 for x in a - b)


def ket_projector(v):
    return v * v.H


def make_isometry(e_zero, e_removed):
    d = len(e_zero)
    w = sp.zeros(SOURCE_SIZE * d, SOURCE_SIZE)
    for source in range(SOURCE_SIZE):
        output = P if source == U else source
        vector = e_removed if source == U else e_zero
        for k in range(d):
            w[output * d + k, source] = vector[k]
    return w


def partial_trace(matrix, d):
    return sp.Matrix(SOURCE_SIZE, SOURCE_SIZE,
                     lambda i, j: sum(matrix[i*d+k, j*d+k] for k in range(d)))


def source_channel(matrix):
    return Q * matrix * Q + matrix[U, U] * PROJECTOR_P


def inspect_channel(w, d):
    require(equal_matrix(w.H * w, EYE), "Isometry is not orthonormal")
    for i in range(SOURCE_SIZE):
        for j in range(SOURCE_SIZE):
            unit = sp.zeros(SOURCE_SIZE)
            unit[i, j] = 1
            require(equal_matrix(partial_trace(w * unit * w.H, d), source_channel(unit)),
                    f"Full channel differs on matrix unit {(i, j)}")
    return SOURCE_SIZE ** 2


def effect(a, b, hidden_size):
    visible = sp.kronecker_product(PROJECTOR_P, a) + sp.kronecker_product(EYE-PROJECTOR_P, b)
    full = sp.kronecker_product(visible, sp.eye(hidden_size))
    require(all(0 <= v <= 1 for v in full.diagonal()), "Test effect positivity failed")
    require(full.is_diagonal(), "Fixture effect no longer has the stated diagonal form")
    return full


def frames():
    yield "minimal_basis", ZERO, ONE, 1
    yield "minimal_rotated", sp.Matrix([R(3,5),R(4,5)]), sp.Matrix([-R(4,5),R(3,5)]), 1
    for name, a, b in [
        ("hidden_11", ONE, ONE), ("hidden_00", ZERO, ZERO),
        ("hidden_blind", H, H), ("hidden_01", ZERO, ONE), ("hidden_10", ONE, ZERO),
    ]:
        yield name, sp.kronecker_product(b, ZERO), sp.kronecker_product(a, ONE), 2


def declared_interval(a, b):
    # Independent extremal calculation for the diagonal fixtures.
    return [sp.simplify((min(a.diagonal()) - max(b.diagonal()))/5),
            sp.simplify((max(a.diagonal()) - min(b.diagonal()))/5)]


def run():
    require(equal_matrix(DELTA, (PROJECTOR_U-sp.diag(0,0,0,1))/5), "Source pair changed")
    outputs = {}
    checked_units = 0
    full_output_states = {}
    for name, e_zero, e_removed, hidden_size in frames():
        d = len(e_zero)
        w = make_isometry(e_zero, e_removed)
        checked_units += inspect_channel(w, d)
        state_plus, state_minus = w * RHO_PLUS * w.H, w * RHO_MINUS * w.H
        full_output_states[name] = (state_plus, state_minus)
        blank = sp.zeros(d, 1)
        blank[0] = 1
        outputs[name] = {}
        for tag, (a, b) in EFFECTS.items():
            f = effect(a, b, hidden_size)
            direct = sp.simplify(sp.trace(f * state_plus) - sp.trace(f * state_minus))
            a_full, b_full = sp.kronecker_product(a,sp.eye(hidden_size)), sp.kronecker_product(b,sp.eye(hidden_size))
            blocks = sp.simplify(((e_removed.H*a_full*e_removed)[0] - (e_zero.H*b_full*e_zero)[0])/5)
            require(direct == blocks, "Density-matrix result differs from block expectations")
            pre_plus = sp.simplify(sp.trace(f * sp.kronecker_product(RHO_PLUS,ket_projector(blank))))
            pre_minus = sp.simplify(sp.trace(f * sp.kronecker_product(RHO_MINUS,ket_projector(blank))))
            require(pre_plus == pre_minus, "Test effect distinguishes before the event")
            if hidden_size == 2:
                lo, hi = declared_interval(a, b)
                require(lo <= direct <= hi, "Output falls outside the exact interval")
            outputs[name][tag] = {"response": str(direct), "pre_probability_both": str(pre_plus)}
    for name in ("minimal_basis", "minimal_rotated"):
        require(outputs[name]["overlapping_calibration"]["response"] == "1/50", "Qubit exception changed")
    require(outputs["hidden_blind"]["overlapping_calibration"]["response"] == "0", "Blind realization changed")
    intervals = {}
    for tag, (a, b) in EFFECTS.items():
        interval = declared_interval(a, b)
        actual = [R(row[tag]["response"]) for name,row in outputs.items() if name.startswith("hidden_")]
        require([min(actual),max(actual)] == interval, "Explicit realizations missed an interval endpoint")
        lo, hi = interval
        intervals[tag] = {"signed_interval": list(map(str, interval)),
                          "guaranteed_absolute_response": str(max(sp.S.Zero, lo, -hi))}
    require(intervals["overlapping_calibration"]["signed_interval"] == ["-3/50","1/10"], "Overlap interval changed")
    require(intervals["separated_calibration"]["signed_interval"] == ["2/25","4/25"], "Separated interval changed")

    bad_w = make_isometry(ZERO, ZERO)
    require(not equal_matrix(bad_w.H*bad_w, EYE), "Invalid frame passed isometry control")
    cross = sp.zeros(SOURCE_SIZE)
    cross[P, U] = 1
    require(not equal_matrix(partial_trace(bad_w*cross*bad_w.H,2),source_channel(cross)),
            "Invalid frame passed the retained-coherence channel control")
    plus, minus = full_output_states["hidden_blind"]
    substituted = sp.kronecker_product(PROJECTOR_P, sp.eye(4))
    require(sp.simplify(sp.trace(substituted*(plus-minus))) == R(1,5), "Substituted effect control changed")
    require(R(outputs["hidden_blind"]["overlapping_calibration"]["response"]) < R(1,50),
            "False dimension-independent guarantee was not rejected")
    return {"status":"PASS", "sympy":sp.__version__, "source_order":["o","p","u","v"],
            "frames":outputs, "intervals":intervals, "matrix_units_verified":checked_units,
            "controls":{"nonorthogonal_frame":"REJECTED","substituted_owner_effect":"REJECTED",
                        "qubit_bound_on_hidden_class":"REJECTED"},
            "scope":"fixed finite exact controls supporting the stated proof",
            "native_owner_access":"NOT_DERIVED"}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
